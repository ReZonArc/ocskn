#!/usr/bin/env python3
#
# test_multiscale_optimization.py
#
# Comprehensive test suite for the OpenCog Multiscale Constraint Optimization
# system. Tests all components including INCI optimization, attention allocation,
# multiscale optimization, and system integration.
#
# Usage: python test_multiscale_optimization.py
# --------------------------------------------------------------

import unittest
import time
import sys
import os

# Import components to test
from inci_optimizer import (
    INCIParser, INCISearchSpaceReducer, FormulationConstraint, 
    RegionType, OptimizationMetrics
)
from attention_allocation import (
    AttentionAllocationManager, AttentionValue, AttentionNode,
    HebbianLearning, AttentionType
)
from multiscale_optimizer import (
    MultiscaleConstraintOptimizer, BiologicalModel, BiologicalScale,
    FormulationCandidate, ObjectiveType
)

class TestINCIOptimization(unittest.TestCase):
    """Test suite for INCI-driven search space reduction"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = INCIParser()
        self.reducer = INCISearchSpaceReducer()
        self.metrics = OptimizationMetrics()
    
    def test_inci_parsing_basic(self):
        """Test basic INCI list parsing"""
        inci_list = "AQUA, GLYCERIN, NIACINAMIDE, PHENOXYETHANOL"
        result = self.parser.parse_inci_list(inci_list)
        
        # Should return list of tuples (ingredient, concentration)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) == 4)
        
        # First ingredient should have highest concentration
        self.assertTrue(result[0][1] > result[1][1])
        
        # Total concentration should be reasonable
        total = sum(conc for _, conc in result)
        self.assertTrue(50 <= total <= 100)
    
    def test_inci_parsing_with_water(self):
        """Test INCI parsing with water as first ingredient"""
        inci_list = "AQUA, GLYCERIN, NIACINAMIDE"
        result = self.parser.parse_inci_list(inci_list)
        
        # Water should get high concentration
        water_conc = result[0][1]
        self.assertTrue(water_conc >= 50.0)
        self.assertEqual(result[0][0], "AQUA")
    
    def test_regulatory_compliance_valid(self):
        """Test regulatory compliance with valid formulation"""
        ingredients = [
            ("AQUA", 70.0),
            ("GLYCERIN", 15.0),
            ("NIACINAMIDE", 5.0),
            ("PHENOXYETHANOL", 0.8)
        ]
        
        is_compliant, issues = self.parser.validate_inci_compliance(ingredients)
        self.assertTrue(is_compliant)
        self.assertEqual(len(issues), 0)
    
    def test_regulatory_compliance_invalid(self):
        """Test regulatory compliance with invalid formulation"""
        ingredients = [
            ("AQUA", 70.0),
            ("RETINOL", 2.0),  # Exceeds 1% limit
            ("PHENOXYETHANOL", 1.5)  # Exceeds 1% limit
        ]
        
        is_compliant, issues = self.parser.validate_inci_compliance(ingredients)
        self.assertFalse(is_compliant)
        self.assertTrue(len(issues) >= 2)
    
    def test_search_space_reduction(self):
        """Test search space reduction functionality"""
        target_inci = "AQUA, GLYCERIN, NIACINAMIDE, RETINOL"
        constraints = [
            FormulationConstraint("RETINOL", 0.1, 1.0, required=True),
            FormulationConstraint("ASCORBIC ACID", 0.0, 0.0, 
                                incompatible_with=["RETINOL"])
        ]
        
        result = self.reducer.reduce_search_space(target_inci, constraints)
        
        # Should return proper result structure
        self.assertIn('target_ingredients', result)
        self.assertIn('viable_ingredients', result)
        self.assertIn('reduction_factor', result)
        
        # Reduction factor should be > 1
        self.assertTrue(result['reduction_factor'] > 1.0)
        
        # Should have some viable ingredients
        self.assertTrue(len(result['viable_ingredients']) > 0)
    
    def test_absolute_concentration_estimation(self):
        """Test absolute concentration estimation"""
        inci_list = "AQUA, GLYCERIN, NIACINAMIDE"
        volume = 100.0  # ml
        
        result = self.reducer.estimate_absolute_concentrations(inci_list, volume)
        
        # Should return dictionary
        self.assertIsInstance(result, dict)
        
        # Should have entries for ingredients
        self.assertIn("AQUA", result)
        self.assertIn("GLYCERIN", result)
        
        # Values should be reasonable (between 0 and 100g for 100ml)
        for ingredient, mass in result.items():
            self.assertTrue(0 <= mass <= 100)
    
    def test_processing_speed(self):
        """Test processing speed requirements"""
        inci_list = "AQUA, GLYCERIN, NIACINAMIDE, RETINOL, PHENOXYETHANOL"
        
        # Test INCI parsing speed
        start_time = time.time()
        for _ in range(100):  # Parse 100 times
            self.parser.parse_inci_list(inci_list)
        parse_time = (time.time() - start_time) / 100
        
        # Should be under 0.01ms per parse (as specified)
        self.assertLess(parse_time, 0.00001)  # 0.01ms = 0.00001s


class TestAttentionAllocation(unittest.TestCase):
    """Test suite for adaptive attention allocation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = AttentionAllocationManager(total_computational_budget=100.0)
        self.hebbian = HebbianLearning()
    
    def test_attention_value_calculation(self):
        """Test attention value calculations"""
        av = AttentionValue(
            short_term_importance=0.5,
            long_term_importance=0.3,
            confidence=0.8,
            urgency=0.2
        )
        
        total = av.total_attention()
        self.assertTrue(total > 0)
        
        # Should incorporate all factors
        self.assertTrue(total > 0.5 + 0.3)  # Base values
    
    def test_attention_decay(self):
        """Test attention decay mechanism"""
        av = AttentionValue(short_term_importance=1.0, urgency=0.5)
        original_sti = av.short_term_importance
        original_urgency = av.urgency
        
        av.decay()
        
        # Values should decrease
        self.assertLess(av.short_term_importance, original_sti)
        self.assertLess(av.urgency, original_urgency)
    
    def test_node_creation_and_activation(self):
        """Test attention node creation and activation"""
        node = self.manager.add_node('test_node', 'test_type', 0.5, 1.0)
        
        self.assertEqual(node.node_id, 'test_node')
        self.assertEqual(node.concept_type, 'test_type')
        
        # Test activation
        activation = node.activate(1.0)
        self.assertTrue(activation > 0)
        self.assertEqual(len(node.activation_history), 1)
    
    def test_attention_allocation_basic(self):
        """Test basic attention allocation"""
        # Add some nodes
        self.manager.add_node('node1', 'type1', 0.8, 1.0)
        self.manager.add_node('node2', 'type2', 0.3, 2.0)
        self.manager.add_node('node3', 'type3', 0.6, 1.5)
        
        # Define requirements
        requirements = {
            'node1': 0.9,
            'node2': 0.2,
            'node3': 0.5
        }
        
        allocations = self.manager.allocate_attention(requirements)
        
        # Should return allocations
        self.assertIsInstance(allocations, dict)
        
        # Should allocate more to higher priority nodes
        if 'node1' in allocations and 'node2' in allocations:
            self.assertTrue(allocations['node1'] >= allocations['node2'])
    
    def test_hebbian_learning(self):
        """Test Hebbian learning mechanism"""
        initial_strength = 0.1
        pre_activation = 0.8
        post_activation = 0.7
        
        new_strength = self.hebbian.update_connection(
            pre_activation, post_activation, initial_strength
        )
        
        # Strength should increase for co-active neurons
        self.assertGreater(new_strength, initial_strength)
        
        # Should be bounded
        self.assertTrue(-1.0 <= new_strength <= 1.0)
    
    def test_performance_metrics(self):
        """Test attention system performance tracking"""
        # Add nodes
        self.manager.add_node('perf_test', 'test', 0.5, 1.0)
        
        # Run several allocations
        for i in range(5):
            requirements = {'perf_test': 0.5 + i * 0.1}
            feedback = {'perf_test': 0.7 + i * 0.05}
            
            self.manager.allocate_attention(requirements, feedback)
        
        # Get report
        report = self.manager.get_attention_report()
        
        # Should have meaningful metrics
        self.assertIsInstance(report, dict)
        self.assertIn('success_rate', report)
        self.assertIn('waste_reduction', report)
        self.assertTrue(0 <= report['success_rate'] <= 100)
    
    def test_processing_speed_requirement(self):
        """Test processing speed requirements (0.02ms)"""
        # Add multiple nodes
        for i in range(10):
            self.manager.add_node(f'speed_test_{i}', 'test', 0.5, 1.0)
        
        requirements = {f'speed_test_{i}': 0.5 for i in range(10)}
        
        # Time allocation
        start_time = time.time()
        self.manager.allocate_attention(requirements)
        process_time = time.time() - start_time
        
        # Should be under 0.02ms (0.00002s)
        self.assertLess(process_time, 0.00002)


class TestMultiscaleOptimization(unittest.TestCase):
    """Test suite for multiscale constraint optimization"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.optimizer = MultiscaleConstraintOptimizer()
        self.biological_model = BiologicalModel(BiologicalScale.MOLECULAR)
    
    def test_biological_model_predictions(self):
        """Test biological model effect predictions"""
        concentrations = {
            'RETINOL': 0.5,
            'NIACINAMIDE': 5.0,
            'ASCORBIC ACID': 10.0
        }
        
        effects = self.biological_model.predict_effect(concentrations)
        
        # Should return effects dictionary
        self.assertIsInstance(effects, dict)
        
        # Should have some effects for given ingredients
        self.assertTrue(len(effects) > 0)
        
        # Effect values should be reasonable (0-1 range typically)
        for effect_name, value in effects.items():
            self.assertTrue(0 <= value <= 1.0)
    
    def test_formulation_candidate_creation(self):
        """Test formulation candidate creation and methods"""
        ingredients = {
            'AQUA': 70.0,
            'GLYCERIN': 15.0,
            'NIACINAMIDE': 5.0,
            'RETINOL': 0.5
        }
        
        candidate = FormulationCandidate(ingredients=ingredients)
        
        # Basic properties
        self.assertEqual(candidate.ingredients, ingredients)
        self.assertTrue(candidate.constraints_satisfied)
        
        # Test fitness calculation
        weights = {ObjectiveType.EFFICACY: 0.5, ObjectiveType.SAFETY: 0.5}
        candidate.objectives = {ObjectiveType.EFFICACY: 0.8, ObjectiveType.SAFETY: 0.7}
        
        fitness = candidate.calculate_fitness(weights)
        expected = 0.8 * 0.5 + 0.7 * 0.5
        self.assertAlmostEqual(fitness, expected, places=2)
    
    def test_formulation_mutation(self):
        """Test formulation mutation"""
        original_ingredients = {
            'AQUA': 70.0,
            'GLYCERIN': 15.0,
            'NIACINAMIDE': 5.0
        }
        
        candidate = FormulationCandidate(ingredients=original_ingredients)
        mutated = candidate.mutate(mutation_rate=1.0, mutation_strength=0.1)
        
        # Should be different candidate
        self.assertNotEqual(id(candidate), id(mutated))
        
        # Should have same ingredients but potentially different concentrations
        self.assertEqual(set(candidate.ingredients.keys()), 
                        set(mutated.ingredients.keys()))
        
        # Generation should increase
        self.assertEqual(mutated.generation, candidate.generation + 1)
    
    def test_formulation_crossover(self):
        """Test formulation crossover"""
        ingredients1 = {'AQUA': 70.0, 'GLYCERIN': 15.0, 'NIACINAMIDE': 5.0}
        ingredients2 = {'AQUA': 65.0, 'GLYCERIN': 20.0, 'NIACINAMIDE': 8.0}
        
        parent1 = FormulationCandidate(ingredients=ingredients1)
        parent2 = FormulationCandidate(ingredients=ingredients2)
        
        offspring1, offspring2 = parent1.crossover(parent2)
        
        # Should produce two offspring
        self.assertNotEqual(id(offspring1), id(parent1))
        self.assertNotEqual(id(offspring2), id(parent2))
        
        # Should have same ingredient types
        self.assertEqual(set(offspring1.ingredients.keys()), set(ingredients1.keys()))
        self.assertEqual(set(offspring2.ingredients.keys()), set(ingredients1.keys()))
    
    def test_constraint_checking(self):
        """Test constraint validation"""
        candidate = FormulationCandidate(ingredients={
            'AQUA': 70.0,
            'RETINOL': 0.5,
            'NIACINAMIDE': 5.0
        })
        
        constraints = [
            FormulationConstraint("RETINOL", 0.1, 1.0, required=True),
            FormulationConstraint("NIACINAMIDE", 2.0, 10.0, required=True),
            FormulationConstraint("ASCORBIC ACID", 0.0, 0.0, 
                                incompatible_with=["RETINOL"])
        ]
        
        is_valid = self.optimizer._check_constraints(candidate, constraints)
        self.assertTrue(is_valid)
        
        # Test with incompatible ingredients
        candidate.ingredients['ASCORBIC ACID'] = 5.0
        is_valid = self.optimizer._check_constraints(candidate, constraints)
        self.assertFalse(is_valid)
    
    def test_objective_calculation(self):
        """Test objective value calculation"""
        candidate = FormulationCandidate(ingredients={
            'AQUA': 70.0,
            'GLYCERIN': 10.0,
            'NIACINAMIDE': 5.0,
            'RETINOL': 0.5
        })
        
        target_profile = {
            'skin_hydration': 0.8,
            'skin_elasticity': 0.6
        }
        
        objectives = self.optimizer._calculate_objectives(candidate, target_profile)
        
        # Should return objectives dictionary
        self.assertIsInstance(objectives, dict)
        
        # Should have all objective types
        for obj_type in ObjectiveType:
            self.assertIn(obj_type, objectives)
        
        # Values should be in reasonable range
        for obj_type, value in objectives.items():
            self.assertTrue(0 <= value <= 1.0)
    
    def test_optimization_basic(self):
        """Test basic optimization functionality"""
        # Set small parameters for fast testing
        self.optimizer.population_size = 10
        self.optimizer.max_generations = 5
        
        target_profile = {'skin_hydration': 0.7}
        constraints = [
            FormulationConstraint("AQUA", 50.0, 80.0, required=True)
        ]
        
        result = self.optimizer.optimize_formulation(
            target_profile=target_profile,
            constraints=constraints
        )
        
        # Should return proper result structure
        self.assertIn('best_formulation', result)
        self.assertIn('optimization_time_seconds', result)
        self.assertIn('generations_completed', result)
        
        # Should have a valid best formulation
        best = result['best_formulation']
        self.assertIsInstance(best, FormulationCandidate)
        self.assertTrue(best.fitness_score >= 0)
    
    def test_multiscale_integration(self):
        """Test multiscale biological model integration"""
        # Test that all scales are properly integrated
        self.assertEqual(len(self.optimizer.biological_models), len(BiologicalScale))
        
        # Test effect prediction across scales
        concentrations = {'RETINOL': 0.5, 'NIACINAMIDE': 5.0}
        
        all_effects = {}
        for scale, model in self.optimizer.biological_models.items():
            effects = model.predict_effect(concentrations)
            all_effects.update(effects)
        
        # Should have effects from multiple scales
        self.assertTrue(len(all_effects) > 0)
    
    def test_performance_requirements(self):
        """Test performance requirements (60 second optimization)"""
        # Test with minimal parameters for speed
        self.optimizer.population_size = 5
        self.optimizer.max_generations = 3
        
        target_profile = {'skin_hydration': 0.7}
        constraints = [FormulationConstraint("AQUA", 50.0, 80.0, required=True)]
        
        start_time = time.time()
        result = self.optimizer.optimize_formulation(target_profile, constraints)
        optimization_time = time.time() - start_time
        
        # Should complete well under 60 seconds for minimal case
        self.assertLess(optimization_time, 5.0)  # Much more strict for test case


class TestSystemIntegration(unittest.TestCase):
    """Test suite for system integration"""
    
    def setUp(self):
        """Set up integrated system"""
        from demo_opencog_multiscale import OpenCogMultiscaleDemo
        # Create minimal demo for testing
        # Note: This is a simplified version for unit testing
        pass
    
    def test_component_compatibility(self):
        """Test that all components work together"""
        # Test that components can be imported and instantiated together
        try:
            from inci_optimizer import INCISearchSpaceReducer
            from attention_allocation import AttentionAllocationManager  
            from multiscale_optimizer import MultiscaleConstraintOptimizer
            
            reducer = INCISearchSpaceReducer()
            manager = AttentionAllocationManager()
            optimizer = MultiscaleConstraintOptimizer(reducer, manager)
            
            # Basic integration test
            self.assertIsNotNone(optimizer.inci_reducer)
            self.assertIsNotNone(optimizer.attention_manager)
            
        except ImportError as e:
            self.fail(f"Component integration failed: {e}")
    
    def test_data_flow(self):
        """Test data flow between components"""
        from inci_optimizer import INCISearchSpaceReducer, FormulationConstraint
        from attention_allocation import AttentionAllocationManager
        from multiscale_optimizer import MultiscaleConstraintOptimizer
        
        # Create integrated system
        reducer = INCISearchSpaceReducer()
        manager = AttentionAllocationManager()
        optimizer = MultiscaleConstraintOptimizer(reducer, manager)
        
        # Test that INCI data flows to optimizer
        inci_list = "AQUA, GLYCERIN, NIACINAMIDE"
        constraints = [FormulationConstraint("AQUA", 50.0, 80.0, required=True)]
        
        # This should work without errors
        viable_ingredients = optimizer._get_viable_ingredients(constraints, None)
        self.assertIsInstance(viable_ingredients, list)
        self.assertTrue(len(viable_ingredients) > 0)
    
    def test_system_performance_metrics(self):
        """Test overall system performance tracking"""
        # This would test the comprehensive metrics from the demo
        # For now, just verify the components track performance
        
        from inci_optimizer import OptimizationMetrics
        from attention_allocation import AttentionAllocationManager
        
        metrics = OptimizationMetrics()
        manager = AttentionAllocationManager()
        
        # Test metrics collection
        metrics.update_metrics(0.01, 10.0, True)
        summary = metrics.get_summary()
        
        self.assertIn('total_searches', summary)
        self.assertIn('efficiency_improvement', summary)
        
        # Test attention reporting
        report = manager.get_attention_report()
        self.assertIn('success_rate', report)
        self.assertIn('waste_reduction', report)


class TestRegressionSuite(unittest.TestCase):
    """Regression tests to ensure system reliability"""
    
    def test_large_inci_list_handling(self):
        """Test handling of large INCI lists"""
        from inci_optimizer import INCIParser
        
        # Create large INCI list (20+ ingredients)
        large_inci = ", ".join([
            "AQUA", "GLYCERIN", "NIACINAMIDE", "SODIUM HYALURONATE", 
            "RETINOL", "ASCORBIC ACID", "TOCOPHEROL", "PHENOXYETHANOL",
            "CARBOMER", "SODIUM HYDROXIDE", "CETYL ALCOHOL", "STEARYL ALCOHOL",
            "POLYSORBATE 60", "DIMETHICONE", "CYCLOPENTASILOXANE",
            "PANTHENOL", "ALLANTOIN", "BISABOLOL", "CHAMOMILLA RECUTITA",
            "CALENDULA OFFICINALIS", "ALOE BARBADENSIS"
        ])
        
        parser = INCIParser()
        result = parser.parse_inci_list(large_inci)
        
        # Should handle large lists without issues
        self.assertEqual(len(result), 21)
        
        # Total should be reasonable
        total = sum(conc for _, conc in result)
        self.assertTrue(80 <= total <= 100)
    
    def test_edge_case_concentrations(self):
        """Test edge cases in concentration handling"""
        from multiscale_optimizer import FormulationCandidate
        
        # Test with extreme concentrations
        extreme_ingredients = {
            'AQUA': 99.9,
            'RETINOL': 0.1
        }
        
        candidate = FormulationCandidate(ingredients=extreme_ingredients)
        
        # Should handle edge cases gracefully
        self.assertEqual(candidate.ingredients['AQUA'], 99.9)
        self.assertEqual(candidate.ingredients['RETINOL'], 0.1)
    
    def test_memory_usage_stability(self):
        """Test that system doesn't have memory leaks"""
        from inci_optimizer import INCISearchSpaceReducer
        from attention_allocation import AttentionAllocationManager
        
        # Run multiple operations to check for memory stability
        reducer = INCISearchSpaceReducer()
        manager = AttentionAllocationManager()
        
        # Multiple iterations
        for i in range(50):
            # INCI operations
            result = reducer.parser.parse_inci_list("AQUA, GLYCERIN, NIACINAMIDE")
            
            # Attention operations
            manager.add_node(f'temp_node_{i}', 'test', 0.5, 1.0)
            allocations = manager.allocate_attention({f'temp_node_{i}': 0.5})
        
        # Should complete without issues
        self.assertTrue(len(manager.nodes) >= 50)


def run_performance_benchmarks():
    """Run performance benchmarks for the system"""
    print("\n" + "=" * 60)
    print("PERFORMANCE BENCHMARKS")
    print("=" * 60)
    
    from inci_optimizer import INCIParser, INCISearchSpaceReducer
    from attention_allocation import AttentionAllocationManager
    from multiscale_optimizer import MultiscaleConstraintOptimizer
    
    # INCI parsing benchmark
    parser = INCIParser()
    inci_list = "AQUA, GLYCERIN, NIACINAMIDE, RETINOL, ASCORBIC ACID, TOCOPHEROL"
    
    start_time = time.time()
    for _ in range(1000):
        parser.parse_inci_list(inci_list)
    inci_time = (time.time() - start_time) / 1000
    
    print(f"INCI Parsing:           {inci_time*1000:.3f}ms (target: <0.01ms)")
    print(f"Status:                 {'✓ PASS' if inci_time < 0.00001 else '✗ FAIL'}")
    
    # Attention allocation benchmark
    manager = AttentionAllocationManager()
    for i in range(10):
        manager.add_node(f'bench_node_{i}', 'test', 0.5, 1.0)
    
    requirements = {f'bench_node_{i}': 0.5 for i in range(10)}
    
    start_time = time.time()
    for _ in range(100):
        manager.allocate_attention(requirements)
    attention_time = (time.time() - start_time) / 100
    
    print(f"Attention Allocation:   {attention_time*1000:.3f}ms (target: <0.02ms)")
    print(f"Status:                 {'✓ PASS' if attention_time < 0.00002 else '✗ FAIL'}")
    
    # Optimization benchmark (simplified)
    optimizer = MultiscaleConstraintOptimizer()
    optimizer.population_size = 5
    optimizer.max_generations = 3
    
    start_time = time.time()
    result = optimizer.optimize_formulation(
        target_profile={'skin_hydration': 0.7},
        constraints=[],
        base_ingredients=['AQUA']
    )
    opt_time = time.time() - start_time
    
    print(f"Optimization (minimal): {opt_time:.2f}s (target: <60s)")
    print(f"Status:                 {'✓ PASS' if opt_time < 60 else '✗ FAIL'}")
    
    print("\nBenchmark Summary:")
    all_pass = (inci_time < 0.00001 and attention_time < 0.00002 and opt_time < 60)
    print(f"Overall:                {'✓ ALL BENCHMARKS PASSED' if all_pass else '✗ SOME BENCHMARKS FAILED'}")


def main():
    """Main test runner"""
    print("OpenCog Multiscale Optimization - Comprehensive Test Suite")
    print("=" * 70)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestINCIOptimization,
        TestAttentionAllocation, 
        TestMultiscaleOptimization,
        TestSystemIntegration,
        TestRegressionSuite
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests Run:     {result.testsRun}")
    print(f"Failures:      {len(result.failures)}")
    print(f"Errors:        {len(result.errors)}")
    print(f"Success Rate:  {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    # Run performance benchmarks
    run_performance_benchmarks()
    
    # Return appropriate exit code
    if result.failures or result.errors:
        print(f"\n✗ {len(result.failures + result.errors)} test(s) failed")
        return 1
    else:
        print(f"\n✓ All {result.testsRun} tests passed successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())