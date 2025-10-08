/*
 * opencog/generate/PlanarCallback.cc
 *
 * Copyright (C) 2025 OpenCog Collection Contributors
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License v3 as
 * published by the Free Software Foundation and including the exceptions
 * at http://opencog.org/wiki/Licenses
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program; if not, write to:
 * Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#include <opencog/generate/PlanarCallback.h>
#include <opencog/atoms/core/FindUtils.h>
#include <opencog/atoms/base/Handle.h>
#include <opencog/util/Logger.h>

using namespace opencog;

PlanarCallback::PlanarCallback(AtomSpace* as, GenerateCallback* base_callback)
	: GenerateCallback(as), _base_callback(base_callback), _dict(nullptr),
	  _constraints(as), _strict_planarity(true), _auto_optimize(true),
	  _work_as(nullptr)
{
}

PlanarCallback::PlanarCallback(AtomSpace* as, Dictionary* dict)
	: GenerateCallback(as), _base_callback(nullptr), _dict(dict),
	  _constraints(as), _strict_planarity(true), _auto_optimize(true),
	  _work_as(nullptr)
{
}

PlanarCallback::~PlanarCallback()
{
	// Don't delete _base_callback or _dict - we don't own them
}

void PlanarCallback::set_initial_sequence(const std::vector<Handle>& sequence)
{
	_current_sequence = sequence;
	_constraints.set_sequence(sequence);
}

void PlanarCallback::clear(AtomSpace* work_as)
{
	_work_as = work_as;
	_constraints.clear();
	_current_sequence.clear();
	
	if (_base_callback) {
		_base_callback->clear(work_as);
	}
}

void PlanarCallback::root_set(const HandleSet& points)
{
	// Add root points to our sequence if not already present
	ensure_points_in_sequence(points);
	
	if (_base_callback) {
		_base_callback->root_set(points);
	}
}

HandleSet PlanarCallback::next_root(void)
{
	if (_base_callback) {
		return _base_callback->next_root();
	}
	
	// Default implementation: return empty set to indicate no more roots
	return HandleSet();
}

HandleSeq PlanarCallback::joints(const Handle& connector)
{
	if (_base_callback) {
		return _base_callback->joints(connector);
	}
	
	// Default implementation: return empty sequence
	return HandleSeq();
}

Handle PlanarCallback::select(const OdoFrame& frame,
                              const Handle& from_sect, size_t offset,
                              const Handle& to_con)
{
	Handle selected;
	
	if (_base_callback) {
		selected = _base_callback->select(frame, from_sect, offset, to_con);
	} else if (_dict) {
		// Simple dictionary-based selection
		// This is a basic implementation - could be made more sophisticated
		HandleSeq matching_sections = _dict->sections(to_con);
		if (!matching_sections.empty()) {
			selected = matching_sections[0]; // Take first match
		}
	}
	
	if (selected != Handle::UNDEFINED) {
		// Check if this selection would violate planarity constraints
		HandleSet from_points = extract_points_from_section(from_sect);
		HandleSet to_points = extract_points_from_section(selected);
		
		// Ensure all points are in our sequence
		ensure_points_in_sequence(from_points);
		ensure_points_in_sequence(to_points);
		
		// For now, check planarity based on the first points
		// In a more sophisticated implementation, we'd check all possible connections
		if (!from_points.empty() && !to_points.empty()) {
			Handle from_pnt = *from_points.begin();
			Handle to_pnt = *to_points.begin();
			
			if (!is_connection_planar(from_pnt, to_pnt)) {
				if (_strict_planarity) {
					logger().debug("PlanarCallback: Rejecting selection due to planarity constraint");
					return Handle::UNDEFINED; // Reject non-planar connection
				} else {
					logger().warn("PlanarCallback: Allowing non-planar connection");
				}
			}
		}
	}
	
	return selected;
}

Handle PlanarCallback::make_link(const Handle& from_con, const Handle& to_con,
                                 const Handle& from_pnt, const Handle& to_pnt)
{
	// Check planarity before creating the link
	if (!is_connection_planar(from_pnt, to_pnt)) {
		if (_strict_planarity) {
			logger().warn("PlanarCallback: Cannot create non-planar link");
			return Handle::UNDEFINED;
		} else {
			logger().warn("PlanarCallback: Creating non-planar link");
		}
	}
	
	// Add the link to our constraints
	if (!_constraints.add_link(from_pnt, to_pnt)) {
		logger().warn("PlanarCallback: Failed to add link to planarity constraints");
	}
	
	// Create the actual link using base callback or default implementation
	Handle link;
	if (_base_callback) {
		link = _base_callback->make_link(from_con, to_con, from_pnt, to_pnt);
	} else {
		// Default implementation: create an EvaluationLink
		link = _work_as->add_link(EVALUATION_LINK, from_con, to_con);
	}
	
	// Optimize sequence if auto-optimization is enabled
	if (_auto_optimize && _constraints.get_crossing_count() > 0) {
		_constraints.optimize_sequence();
		// Update our current sequence to match the optimized version
		_current_sequence = _constraints.get_sequence();
	}
	
	return link;
}

HandleSet PlanarCallback::extract_points_from_section(const Handle& section)
{
	HandleSet points;
	
	if (section == Handle::UNDEFINED) {
		return points;
	}
	
	// Extract points from a Section
	// Section format: (Section (Atom "point") (ConnectorSeq ...))
	if (section->get_type() == SECTION_LINK) {
		const HandleSeq& outgoing = section->getOutgoingSet();
		if (!outgoing.empty()) {
			points.insert(outgoing[0]); // First element is the point
		}
	} else {
		// If it's not a Section, treat it as a point itself
		points.insert(section);
	}
	
	return points;
}

bool PlanarCallback::is_connection_planar(const Handle& from_pnt, const Handle& to_pnt)
{
	return _constraints.is_planar_link(from_pnt, to_pnt);
}

void PlanarCallback::ensure_points_in_sequence(const HandleSet& points)
{
	for (const Handle& point : points) {
		if (_constraints.get_position(point) == -1) {
			// Point not in sequence, add it
			if (_current_sequence.empty()) {
				// First point, just add it
				_current_sequence.push_back(point);
				_constraints.append_point(point);
			} else {
				// Find best insertion position
				// For now, just append to the end
				// TODO: Implement find_best_insertion_position
				_current_sequence.push_back(point);
				_constraints.append_point(point);
			}
		}
	}
}

size_t PlanarCallback::find_best_insertion_position(const Handle& point,
                                                   const Handle& connected_point)
{
	// Simple heuristic: insert next to the connected point
	int connected_pos = _constraints.get_position(connected_point);
	if (connected_pos >= 0) {
		// Try to insert adjacent to the connected point
		return static_cast<size_t>(connected_pos) + 1;
	}
	
	// Default: append to end
	return _current_sequence.size();
}