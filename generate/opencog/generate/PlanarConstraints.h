/*
 * opencog/generate/PlanarConstraints.h
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

#ifndef _OPENCOG_PLANAR_CONSTRAINTS_H
#define _OPENCOG_PLANAR_CONSTRAINTS_H

#include <map>
#include <vector>
#include <opencog/atomspace/AtomSpace.h>

namespace opencog
{
/** \addtogroup grp_generate
 *  @{
 */

/// Planar graph constraints for network generation. This class implements
/// planarity checking and constraint enforcement to ensure generated networks
/// don't have crossing links when laid out in sequential (linear) order.
///
/// This is particularly important for natural language generation where
/// word order must be preserved and links shouldn't cross when drawn above
/// the sentence.
///
/// The planarity constraint works by:
/// 1. Maintaining an ordered sequence of points (nodes)
/// 2. Checking that any new link doesn't cross existing links
/// 3. Providing methods to enforce planarity during generation
///
class PlanarConstraints
{
private:
	AtomSpace* _as;
	
	/// Ordered sequence of points in the linear arrangement
	std::vector<Handle> _sequence;
	
	/// Map from atom handles to their position in the sequence
	std::map<Handle, size_t> _position_map;
	
	/// Set of links that have been established
	std::vector<std::pair<size_t, size_t>> _links;
	
	/// Check if two links cross in the linear order
	bool links_cross(size_t i1, size_t j1, size_t i2, size_t j2) const;
	
	/// Update internal position mapping
	void update_position_map();

public:
	PlanarConstraints(AtomSpace* as) : _as(as) {}
	virtual ~PlanarConstraints() {}

	/// Clear all constraints and start fresh
	void clear();
	
	/// Set the linear sequence order for planarity checking
	/// This establishes the order in which points should appear
	/// in the final linear arrangement (e.g., word order in sentences)
	void set_sequence(const std::vector<Handle>& sequence);
	
	/// Add a point to the end of the current sequence
	void append_point(const Handle& point);
	
	/// Check if a proposed link would violate planarity constraints
	/// Returns true if the link can be added without crossing existing links
	bool is_planar_link(const Handle& from_point, const Handle& to_point) const;
	
	/// Add a link to the constraint system
	/// Returns true if successfully added, false if it would violate planarity
	bool add_link(const Handle& from_point, const Handle& to_point);
	
	/// Remove a link from the constraint system
	void remove_link(const Handle& from_point, const Handle& to_point);
	
	/// Get the current sequence order
	const std::vector<Handle>& get_sequence() const { return _sequence; }
	
	/// Get position of a point in the sequence (-1 if not found)
	int get_position(const Handle& point) const;
	
	/// Check if the entire current graph is planar
	bool is_planar() const;
	
	/// Get all links that would need to be removed to make the graph planar
	std::vector<std::pair<Handle, Handle>> get_crossing_links() const;
	
	/// Optimize the sequence order to minimize crossings
	/// Uses a simple heuristic to reorder points to reduce link crossings
	void optimize_sequence();
	
	/// Statistics and debugging
	size_t get_link_count() const { return _links.size(); }
	size_t get_crossing_count() const;
	
	/// Debug: print current state
	void print_state() const;
};

/** @}*/
} // namespace opencog

#endif // _OPENCOG_PLANAR_CONSTRAINTS_H