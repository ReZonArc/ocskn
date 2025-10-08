/*
 * opencog/generate/PlanarConstraints.cc
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

#include <algorithm>
#include <iostream>
#include <opencog/generate/PlanarConstraints.h>
#include <opencog/util/Logger.h>

using namespace opencog;

void PlanarConstraints::clear()
{
	_sequence.clear();
	_position_map.clear();
	_links.clear();
}

void PlanarConstraints::set_sequence(const std::vector<Handle>& sequence)
{
	_sequence = sequence;
	update_position_map();
	_links.clear(); // Clear existing links since sequence changed
}

void PlanarConstraints::append_point(const Handle& point)
{
	_sequence.push_back(point);
	_position_map[point] = _sequence.size() - 1;
}

void PlanarConstraints::update_position_map()
{
	_position_map.clear();
	for (size_t i = 0; i < _sequence.size(); i++) {
		_position_map[_sequence[i]] = i;
	}
}

bool PlanarConstraints::links_cross(size_t i1, size_t j1, size_t i2, size_t j2) const
{
	// Ensure i1 < j1 and i2 < j2 (normalize link direction)
	if (i1 > j1) std::swap(i1, j1);
	if (i2 > j2) std::swap(i2, j2);
	
	// Links cross if one link's endpoints are on different sides of the other link
	// Link (i1,j1) crosses link (i2,j2) if:
	// i1 < i2 < j1 < j2  OR  i2 < i1 < j2 < j1
	return (i1 < i2 && i2 < j1 && j1 < j2) || (i2 < i1 && i1 < j2 && j2 < j1);
}

bool PlanarConstraints::is_planar_link(const Handle& from_point, const Handle& to_point) const
{
	// Check if both points are in the sequence
	auto from_it = _position_map.find(from_point);
	auto to_it = _position_map.find(to_point);
	
	if (from_it == _position_map.end() || to_it == _position_map.end()) {
		logger().warn("PlanarConstraints::is_planar_link: Point not found in sequence");
		return false;
	}
	
	size_t from_pos = from_it->second;
	size_t to_pos = to_it->second;
	
	// Check against all existing links
	for (const auto& link : _links) {
		if (links_cross(from_pos, to_pos, link.first, link.second)) {
			return false;
		}
	}
	
	return true;
}

bool PlanarConstraints::add_link(const Handle& from_point, const Handle& to_point)
{
	if (!is_planar_link(from_point, to_point)) {
		return false;
	}
	
	auto from_it = _position_map.find(from_point);
	auto to_it = _position_map.find(to_point);
	
	if (from_it == _position_map.end() || to_it == _position_map.end()) {
		return false;
	}
	
	_links.push_back(std::make_pair(from_it->second, to_it->second));
	return true;
}

void PlanarConstraints::remove_link(const Handle& from_point, const Handle& to_point)
{
	auto from_it = _position_map.find(from_point);
	auto to_it = _position_map.find(to_point);
	
	if (from_it == _position_map.end() || to_it == _position_map.end()) {
		return;
	}
	
	size_t from_pos = from_it->second;
	size_t to_pos = to_it->second;
	
	// Remove all matching links (there should be at most one, but be safe)
	_links.erase(
		std::remove_if(_links.begin(), _links.end(),
			[from_pos, to_pos](const std::pair<size_t, size_t>& link) {
				return (link.first == from_pos && link.second == to_pos) ||
				       (link.first == to_pos && link.second == from_pos);
			}),
		_links.end());
}

int PlanarConstraints::get_position(const Handle& point) const
{
	auto it = _position_map.find(point);
	return (it != _position_map.end()) ? static_cast<int>(it->second) : -1;
}

bool PlanarConstraints::is_planar() const
{
	// Check if any pair of links crosses
	for (size_t i = 0; i < _links.size(); i++) {
		for (size_t j = i + 1; j < _links.size(); j++) {
			if (links_cross(_links[i].first, _links[i].second,
			                _links[j].first, _links[j].second)) {
				return false;
			}
		}
	}
	return true;
}

std::vector<std::pair<Handle, Handle>> PlanarConstraints::get_crossing_links() const
{
	std::vector<std::pair<Handle, Handle>> crossing_links;
	
	for (size_t i = 0; i < _links.size(); i++) {
		for (size_t j = i + 1; j < _links.size(); j++) {
			if (links_cross(_links[i].first, _links[i].second,
			                _links[j].first, _links[j].second)) {
				// Add both links that are crossing
				crossing_links.push_back(std::make_pair(
					_sequence[_links[i].first], _sequence[_links[i].second]));
				crossing_links.push_back(std::make_pair(
					_sequence[_links[j].first], _sequence[_links[j].second]));
			}
		}
	}
	
	// Remove duplicates
	std::sort(crossing_links.begin(), crossing_links.end());
	crossing_links.erase(std::unique(crossing_links.begin(), crossing_links.end()),
	                     crossing_links.end());
	
	return crossing_links;
}

void PlanarConstraints::optimize_sequence()
{
	// Simple greedy optimization: try to minimize crossings by local swaps
	// This is a heuristic approach - optimal planar arrangement is NP-hard
	
	bool improved = true;
	size_t max_iterations = _sequence.size() * _sequence.size();
	size_t iteration = 0;
	
	while (improved && iteration < max_iterations) {
		improved = false;
		iteration++;
		
		size_t current_crossings = get_crossing_count();
		
		// Try swapping adjacent elements
		for (size_t i = 0; i < _sequence.size() - 1; i++) {
			// Swap elements at positions i and i+1
			std::swap(_sequence[i], _sequence[i + 1]);
			update_position_map();
			
			size_t new_crossings = get_crossing_count();
			
			if (new_crossings < current_crossings) {
				// Keep the swap
				current_crossings = new_crossings;
				improved = true;
			} else {
				// Revert the swap
				std::swap(_sequence[i], _sequence[i + 1]);
				update_position_map();
			}
		}
	}
	
	logger().debug("PlanarConstraints::optimize_sequence completed after %zu iterations", iteration);
}

size_t PlanarConstraints::get_crossing_count() const
{
	size_t count = 0;
	for (size_t i = 0; i < _links.size(); i++) {
		for (size_t j = i + 1; j < _links.size(); j++) {
			if (links_cross(_links[i].first, _links[i].second,
			                _links[j].first, _links[j].second)) {
				count++;
			}
		}
	}
	return count;
}

void PlanarConstraints::print_state() const
{
	std::cout << "=== Planar Constraints State ===" << std::endl;
	std::cout << "Sequence (" << _sequence.size() << " points): ";
	for (size_t i = 0; i < _sequence.size(); i++) {
		std::cout << _sequence[i] << " ";
	}
	std::cout << std::endl;
	
	std::cout << "Links (" << _links.size() << "): ";
	for (const auto& link : _links) {
		std::cout << "(" << link.first << "," << link.second << ") ";
	}
	std::cout << std::endl;
	
	std::cout << "Crossing count: " << get_crossing_count() << std::endl;
	std::cout << "Is planar: " << (is_planar() ? "YES" : "NO") << std::endl;
	std::cout << "================================" << std::endl;
}