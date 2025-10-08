/*
 * opencog/generate/PlanarCallback.h
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

#ifndef _OPENCOG_PLANAR_CALLBACK_H
#define _OPENCOG_PLANAR_CALLBACK_H

#include <opencog/generate/GenerateCallback.h>
#include <opencog/generate/PlanarConstraints.h>
#include <opencog/generate/Dictionary.h>

namespace opencog
{
/** \addtogroup grp_generate
 *  @{
 */

/// Planar-aware generation callback. This callback extends the basic
/// generation functionality to ensure that generated graphs maintain
/// planarity constraints. This is essential for natural language 
/// generation where word order must be preserved and links shouldn't 
/// cross when drawn above the sentence.
///
/// The callback works by:
/// 1. Maintaining a linear sequence order for all generated points
/// 2. Checking planarity constraints before allowing new connections
/// 3. Providing fallback strategies when planar connections aren't possible
/// 4. Optimizing the sequence order to minimize crossings
///
/// This callback can wrap any other callback to add planarity constraints,
/// or can be used standalone with a dictionary of sections.
///
class PlanarCallback : public GenerateCallback
{
private:
	/// Underlying callback to delegate to (may be null)
	GenerateCallback* _base_callback;
	
	/// Dictionary of available sections (used if no base callback)
	Dictionary* _dict;
	
	/// Planarity constraint manager
	PlanarConstraints _constraints;
	
	/// Current sequence being built
	std::vector<Handle> _current_sequence;
	
	/// Whether to enforce strict planarity (reject non-planar) or
	/// allow non-planar with warnings
	bool _strict_planarity;
	
	/// Whether to automatically optimize sequence order
	bool _auto_optimize;
	
	/// Working atomspace for this callback
	AtomSpace* _work_as;

public:
	/// Constructor with base callback (decorator pattern)
	PlanarCallback(AtomSpace* as, GenerateCallback* base_callback = nullptr);
	
	/// Constructor with dictionary (standalone usage)
	PlanarCallback(AtomSpace* as, Dictionary* dict);
	
	virtual ~PlanarCallback();

	/// Set planarity enforcement mode
	void set_strict_planarity(bool strict) { _strict_planarity = strict; }
	bool get_strict_planarity() const { return _strict_planarity; }
	
	/// Set automatic sequence optimization
	void set_auto_optimize(bool optimize) { _auto_optimize = optimize; }
	bool get_auto_optimize() const { return _auto_optimize; }
	
	/// Set the initial sequence order (for language generation, this
	/// would be the word order)
	void set_initial_sequence(const std::vector<Handle>& sequence);
	
	/// Get current planarity constraints object (for advanced usage)
	PlanarConstraints& get_constraints() { return _constraints; }
	const PlanarConstraints& get_constraints() const { return _constraints; }

	// GenerateCallback interface implementation
	virtual void clear(AtomSpace* work_as) override;
	virtual void root_set(const HandleSet& points) override;
	virtual HandleSet next_root(void) override;
	virtual HandleSeq joints(const Handle& connector) override;
	virtual Handle select(const OdoFrame& frame,
	                      const Handle& from_sect, size_t offset,
	                      const Handle& to_con) override;
	virtual Handle make_link(const Handle& from_con, const Handle& to_con,
	                         const Handle& from_pnt, const Handle& to_pnt) override;

private:
	/// Extract points from a section (helper method)
	HandleSet extract_points_from_section(const Handle& section);
	
	/// Check if a potential connection would violate planarity
	bool is_connection_planar(const Handle& from_pnt, const Handle& to_pnt);
	
	/// Add points to the sequence if not already present
	void ensure_points_in_sequence(const HandleSet& points);
	
	/// Find the best position to insert a new point to minimize crossings
	size_t find_best_insertion_position(const Handle& point, 
	                                   const Handle& connected_point);
};

/** @}*/
} // namespace opencog

#endif // _OPENCOG_PLANAR_CALLBACK_H