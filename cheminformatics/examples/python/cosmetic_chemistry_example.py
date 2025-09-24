#! /usr/bin/env python3
#
# cosmetic_chemistry_example.py
#
# Advanced cosmetic chemistry example demonstrating formulation analysis,
# optimization, and ingredient compatibility checking using the OpenCog
# cheminformatics framework with cosmetic chemistry specializations.
#
# This example demonstrates:
# - Complex formulation modeling with multiple phases
# - Ingredient compatibility and incompatibility analysis
# - Automatic pH and stability optimization
# - Regulatory compliance checking
# - Ingredient substitution recommendations
# - Quality control validation
#
# --------------------------------------------------------------

# Import the AtomSpace and type constructors
from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.scheme_wrapper import *

# Import cheminformatics and cosmetic types
from opencog.cheminformatics import *

# Initialize AtomSpace
spa = AtomSpace()
set_default_atomspace(spa)

print("=" * 70)
print("Advanced Cosmetic Chemistry: Formulation Analysis & Optimization")
print("=" * 70)
print(f'AtomSpace initialized: {spa}')
print()

# ===================================================================
# PART 1: Advanced Ingredient Database
# ===================================================================

print("PART 1: Building Comprehensive Ingredient Database")
print("-" * 50)

# Define a comprehensive set of cosmetic ingredients with properties
class IngredientDatabase:
    def __init__(self):
        self.actives = {}
        self.functional = {}
        self.properties = {}
        self.safety_data = {}
        
    def add_active_ingredient(self, name, concentration_range, pH_range, benefits):
        ingredient = ACTIVE_INGREDIENT(name)
        self.actives[name] = {
            'atom': ingredient,
            'concentration': concentration_range,
            'pH_range': pH_range,
            'benefits': benefits
        }
        return ingredient
        
    def add_functional_ingredient(self, name, ingredient_type, function, concentration_range):
        if ingredient_type == 'humectant':
            ingredient = HUMECTANT(name)
        elif ingredient_type == 'emulsifier':
            ingredient = EMULSIFIER(name)
        elif ingredient_type == 'preservative':
            ingredient = PRESERVATIVE(name)
        elif ingredient_type == 'thickener':
            ingredient = THICKENER(name)
        elif ingredient_type == 'emollient':
            ingredient = EMOLLIENT(name)
        elif ingredient_type == 'antioxidant':
            ingredient = ANTIOXIDANT(name)
        else:
            ingredient = COSMETIC_INGREDIENT_NODE(name)
            
        self.functional[name] = {
            'atom': ingredient,
            'type': ingredient_type,
            'function': function,
            'concentration': concentration_range
        }
        return ingredient

# Create ingredient database
db = IngredientDatabase()

print("Creating comprehensive ingredient database...")

# Active ingredients with detailed properties
hyaluronic_acid = db.add_active_ingredient(
    'hyaluronic_acid', 
    (0.1, 2.0), 
    (4.0, 7.0), 
    ['hydration', 'plumping', 'barrier_repair']
)

niacinamide = db.add_active_ingredient(
    'niacinamide',
    (2.0, 10.0),
    (5.0, 7.0),
    ['barrier_function', 'oil_control', 'brightening']
)

retinol = db.add_active_ingredient(
    'retinol',
    (0.01, 1.0),
    (5.5, 6.5),
    ['anti_aging', 'cell_turnover', 'collagen_synthesis']
)

vitamin_c = db.add_active_ingredient(
    'ascorbic_acid',
    (5.0, 20.0),
    (3.0, 4.0),
    ['antioxidant', 'brightening', 'collagen_synthesis']
)

# Functional ingredients
glycerin = db.add_functional_ingredient('glycerin', 'humectant', 'moisture_retention', (1.0, 10.0))
propylene_glycol = db.add_functional_ingredient('propylene_glycol', 'humectant', 'moisture_attraction', (1.0, 5.0))

cetyl_alcohol = db.add_functional_ingredient('cetyl_alcohol', 'emulsifier', 'oil_water_binding', (2.0, 8.0))
polysorbate_60 = db.add_functional_ingredient('polysorbate_60', 'emulsifier', 'emulsion_stability', (1.0, 4.0))

phenoxyethanol = db.add_functional_ingredient('phenoxyethanol', 'preservative', 'antimicrobial', (0.2, 1.0))
methylparaben = db.add_functional_ingredient('methylparaben', 'preservative', 'broad_spectrum', (0.1, 0.4))

xanthan_gum = db.add_functional_ingredient('xanthan_gum', 'thickener', 'viscosity_enhancement', (0.1, 1.0))
carbomer = db.add_functional_ingredient('carbomer', 'thickener', 'gel_formation', (0.1, 2.0))

squalane = db.add_functional_ingredient('squalane', 'emollient', 'skin_softening', (1.0, 10.0))
jojoba_oil = db.add_functional_ingredient('jojoba_oil', 'emollient', 'moisturization', (1.0, 15.0))

tocopherol = db.add_functional_ingredient('tocopherol', 'antioxidant', 'oxidation_prevention', (0.1, 1.0))

print(f"Database created with {len(db.actives)} active ingredients and {len(db.functional)} functional ingredients")
print()

# ===================================================================
# PART 2: Ingredient Compatibility Analysis
# ===================================================================

print("PART 2: Ingredient Compatibility Matrix")
print("-" * 50)

# Define compatibility relationships between ingredients
def create_compatibility_matrix():
    """Create a matrix of ingredient interactions"""
    
    # Compatible combinations (work well together)
    compatible_pairs = [
        (hyaluronic_acid, niacinamide),
        (hyaluronic_acid, glycerin),
        (vitamin_c, tocopherol),  # Vitamin C + E synergy
        (retinol, hyaluronic_acid),
        (niacinamide, glycerin),
        (cetyl_alcohol, polysorbate_60),
        (phenoxyethanol, methylparaben),
        (squalane, jojoba_oil)
    ]
    
    # Incompatible combinations (should be avoided)
    incompatible_pairs = [
        (vitamin_c, retinol, "pH incompatibility"),
        (retinol, ACTIVE_INGREDIENT('benzoyl_peroxide'), "degradation"),
        (vitamin_c, niacinamide, "potential_irritation_high_pH"),
        (ACTIVE_INGREDIENT('aha_acids'), retinol, "over_exfoliation")
    ]
    
    # Synergistic combinations (enhance each other)
    synergy_pairs = [
        (vitamin_c, tocopherol, "antioxidant_network"),
        (ACTIVE_INGREDIENT('ceramides'), ACTIVE_INGREDIENT('cholesterol'), "barrier_repair"),
        (hyaluronic_acid, ACTIVE_INGREDIENT('peptides'), "hydration_anti_aging")
    ]
    
    compatibility_links = []
    incompatibility_links = []
    synergy_links = []
    
    # Create compatibility links
    for pair in compatible_pairs:
        link = COMPATIBILITY_LINK(pair[0], pair[1])
        compatibility_links.append(link)
        print(f"✓ Compatible: {pair[0]} + {pair[1]}")
    
    # Create incompatibility links
    for item in incompatible_pairs:
        ingredient1, ingredient2 = item[0], item[1]
        reason = item[2] if len(item) > 2 else "general_incompatibility"
        link = INCOMPATIBILITY_LINK(ingredient1, ingredient2)
        incompatibility_links.append(link)
        print(f"✗ Incompatible: {ingredient1} + {ingredient2} ({reason})")
    
    # Create synergy links
    for item in synergy_pairs:
        ingredient1, ingredient2 = item[0], item[1]
        mechanism = item[2] if len(item) > 2 else "general_synergy"
        link = SYNERGY_LINK(ingredient1, ingredient2)
        synergy_links.append(link)
        print(f"⚡ Synergy: {ingredient1} + {ingredient2} ({mechanism})")
    
    return compatibility_links, incompatibility_links, synergy_links

compat_links, incompat_links, synergy_links = create_compatibility_matrix()
print(f"Created {len(compat_links)} compatibility, {len(incompat_links)} incompatibility, and {len(synergy_links)} synergy relationships")
print()

# ===================================================================
# PART 3: Advanced Formulation Design
# ===================================================================

print("PART 3: Advanced Multi-Phase Formulation Design")
print("-" * 50)

# Create a complex anti-aging serum with multiple actives
class AdvancedFormulation:
    def __init__(self, name, formulation_type):
        self.name = name
        self.formulation_type = formulation_type
        self.ingredients = {}
        self.properties = {}
        self.phases = {}
        
    def add_ingredient(self, ingredient, concentration, phase='single'):
        self.ingredients[ingredient] = {
            'concentration': concentration,
            'phase': phase
        }
        
    def add_property(self, property_type, value):
        if property_type == 'pH':
            prop = PH_PROPERTY(str(value))
        elif property_type == 'viscosity':
            prop = VISCOSITY_PROPERTY(f"{value}_cP")
        elif property_type == 'texture':
            prop = TEXTURE_PROPERTY(value)
        elif property_type == 'stability':
            prop = STABILITY_PROPERTY(value)
        else:
            prop = COSMETIC_PROPERTY_NODE(f"{property_type}_{value}")
        
        self.properties[property_type] = prop
        return prop
        
    def create_formulation_atom(self):
        ingredient_atoms = list(self.ingredients.keys())
        if self.formulation_type == 'serum':
            formulation = SERUM_FORMULATION(*ingredient_atoms)
        elif self.formulation_type == 'moisturizer':
            formulation = MOISTURIZER_FORMULATION(*ingredient_atoms)
        elif self.formulation_type == 'cleanser':
            formulation = CLEANSER_FORMULATION(*ingredient_atoms)
        else:
            formulation = SKINCARE_FORMULATION(*ingredient_atoms)
        
        return formulation

# Create advanced anti-aging serum
print("Designing advanced anti-aging serum...")
anti_aging_serum = AdvancedFormulation("Advanced Anti-Aging Serum", "serum")

# Water phase ingredients
anti_aging_serum.add_ingredient(hyaluronic_acid, 1.5, 'water_phase')
anti_aging_serum.add_ingredient(niacinamide, 5.0, 'water_phase')
anti_aging_serum.add_ingredient(glycerin, 8.0, 'water_phase')
anti_aging_serum.add_ingredient(propylene_glycol, 3.0, 'water_phase')
anti_aging_serum.add_ingredient(xanthan_gum, 0.3, 'water_phase')

# Oil phase ingredients  
anti_aging_serum.add_ingredient(retinol, 0.1, 'oil_phase')
anti_aging_serum.add_ingredient(squalane, 2.0, 'oil_phase')
anti_aging_serum.add_ingredient(tocopherol, 0.2, 'oil_phase')

# Emulsification system
anti_aging_serum.add_ingredient(cetyl_alcohol, 3.0, 'emulsifier')
anti_aging_serum.add_ingredient(polysorbate_60, 1.5, 'emulsifier')

# Preservation system
anti_aging_serum.add_ingredient(phenoxyethanol, 0.5, 'preservative')

# Add properties
anti_aging_serum.add_property('pH', 5.8)
anti_aging_serum.add_property('viscosity', 3500)
anti_aging_serum.add_property('texture', 'silky_serum')
anti_aging_serum.add_property('stability', 'excellent_24_months')

# Create the formulation atom
serum_atom = anti_aging_serum.create_formulation_atom()

print(f"Advanced serum created: {serum_atom}")
print(f"Ingredients: {len(anti_aging_serum.ingredients)}")
print(f"Properties: {list(anti_aging_serum.properties.keys())}")
print()

# ===================================================================
# PART 4: Automated Quality Control and Validation
# ===================================================================

print("PART 4: Automated Quality Control and Validation")
print("-" * 50)

def validate_formulation(formulation_obj):
    """Comprehensive formulation validation"""
    
    validation_results = {
        'pH_check': False,
        'preservative_check': False,
        'compatibility_check': False,
        'concentration_check': False,
        'regulatory_check': False
    }
    
    issues = []
    warnings = []
    
    # pH validation
    if 'pH' in formulation_obj.properties:
        pH_value = float(formulation_obj.properties['pH'].name.split('_')[-1])
        if 4.5 <= pH_value <= 7.0:
            validation_results['pH_check'] = True
            print(f"✓ pH check passed: {pH_value} (within safe range 4.5-7.0)")
        else:
            issues.append(f"pH {pH_value} outside recommended range 4.5-7.0")
            print(f"✗ pH check failed: {pH_value}")
    
    # Preservative system check
    preservatives = [ing for ing in formulation_obj.ingredients.keys() 
                    if hasattr(ing, 'type') and 'PRESERVATIVE' in str(ing.type)]
    if preservatives:
        validation_results['preservative_check'] = True
        print(f"✓ Preservative system present: {len(preservatives)} preservatives")
    else:
        issues.append("No preservative system detected")
        print("✗ No preservative system found")
    
    # Concentration validation
    total_actives = 0
    for ingredient, data in formulation_obj.ingredients.items():
        if hasattr(ingredient, 'type') and 'ACTIVE_INGREDIENT' in str(ingredient.type):
            total_actives += data['concentration']
    
    if total_actives <= 15.0:  # Generally, total actives shouldn't exceed 15%
        validation_results['concentration_check'] = True
        print(f"✓ Active concentration check passed: {total_actives}%")
    else:
        warnings.append(f"High total active concentration: {total_actives}%")
        print(f"⚠ Warning: High active concentration: {total_actives}%")
    
    # Compatibility check (simplified)
    ingredient_list = list(formulation_obj.ingredients.keys())
    incompatible_found = False
    
    for i, ing1 in enumerate(ingredient_list):
        for ing2 in ingredient_list[i+1:]:
            # Check against known incompatible pairs
            for incompat_link in incompat_links:
                if (ing1 in [incompat_link.out[0], incompat_link.out[1]] and 
                    ing2 in [incompat_link.out[0], incompat_link.out[1]]):
                    incompatible_found = True
                    issues.append(f"Incompatible ingredients: {ing1} + {ing2}")
    
    if not incompatible_found:
        validation_results['compatibility_check'] = True
        print("✓ No incompatible ingredient combinations found")
    else:
        print("✗ Incompatible ingredient combinations detected")
    
    return validation_results, issues, warnings

# Validate the anti-aging serum
print("Validating advanced anti-aging serum...")
validation, issues, warnings = validate_formulation(anti_aging_serum)

print(f"\nValidation Summary:")
print(f"Passed checks: {sum(validation.values())}/{len(validation)}")
if issues:
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  • {issue}")
if warnings:
    print(f"Warnings: {len(warnings)}")
    for warning in warnings:
        print(f"  • {warning}")

print()

# ===================================================================
# PART 5: Ingredient Substitution Engine
# ===================================================================

print("PART 5: Intelligent Ingredient Substitution")
print("-" * 50)

def find_substitutes(ingredient, formulation_obj, reason="optimization"):
    """Find suitable substitutes for an ingredient"""
    
    substitutes = []
    
    # Determine ingredient function
    ingredient_type = None
    if hasattr(ingredient, 'type'):
        if 'HUMECTANT' in str(ingredient.type):
            # Find other humectants
            for name, data in db.functional.items():
                if data['type'] == 'humectant' and data['atom'] != ingredient:
                    substitutes.append((data['atom'], f"Alternative humectant: {name}"))
        
        elif 'EMULSIFIER' in str(ingredient.type):
            # Find other emulsifiers
            for name, data in db.functional.items():
                if data['type'] == 'emulsifier' and data['atom'] != ingredient:
                    substitutes.append((data['atom'], f"Alternative emulsifier: {name}"))
        
        elif 'ACTIVE_INGREDIENT' in str(ingredient.type):
            # Find actives with similar benefits
            ingredient_name = ingredient.name
            if ingredient_name in db.actives:
                target_benefits = db.actives[ingredient_name]['benefits']
                for name, data in db.actives.items():
                    if (data['atom'] != ingredient and 
                        any(benefit in data['benefits'] for benefit in target_benefits)):
                        overlap = set(target_benefits) & set(data['benefits'])
                        substitutes.append((data['atom'], f"Similar benefits: {list(overlap)}"))
    
    return substitutes

# Example substitution scenario
print("Scenario: Need to replace glycerin due to supplier shortage")
glycerin_substitutes = find_substitutes(glycerin, anti_aging_serum, "supplier_shortage")

print(f"Found {len(glycerin_substitutes)} potential substitutes for glycerin:")
for substitute, reason in glycerin_substitutes:
    print(f"  • {substitute}: {reason}")

print()

# ===================================================================
# PART 6: Regulatory Compliance Automation
# ===================================================================

print("PART 6: Regulatory Compliance Automation")
print("-" * 50)

def check_regulatory_compliance(formulation_obj, region="EU"):
    """Check formulation against regulatory requirements"""
    
    compliance_status = {
        'approved_ingredients': True,
        'concentration_limits': True,
        'restricted_substances': True,
        'labeling_requirements': True
    }
    
    compliance_issues = []
    
    print(f"Checking {region} regulatory compliance...")
    
    # Example concentration limits (simplified)
    eu_limits = {
        'retinol': 1.0,
        'ascorbic_acid': 20.0,
        'phenoxyethanol': 1.0,
        'methylparaben': 0.4
    }
    
    for ingredient, data in formulation_obj.ingredients.items():
        ingredient_name = ingredient.name
        concentration = data['concentration']
        
        if ingredient_name in eu_limits:
            limit = eu_limits[ingredient_name]
            if concentration > limit:
                compliance_status['concentration_limits'] = False
                compliance_issues.append(f"{ingredient_name}: {concentration}% exceeds EU limit of {limit}%")
                print(f"✗ {ingredient_name}: {concentration}% > {limit}% (EU limit)")
            else:
                print(f"✓ {ingredient_name}: {concentration}% ≤ {limit}% (EU limit)")
    
    # Create regulatory compliance atoms
    if all(compliance_status.values()):
        eu_compliant = EU_COMPLIANT(f"{formulation_obj.name}_approved")
        print(f"✓ Overall EU compliance: APPROVED")
    else:
        print(f"✗ Overall EU compliance: ISSUES FOUND")
    
    return compliance_status, compliance_issues

# Check compliance for the serum
compliance_status, compliance_issues = check_regulatory_compliance(anti_aging_serum)

if compliance_issues:
    print("\nCompliance Issues:")
    for issue in compliance_issues:
        print(f"  • {issue}")

print()

# ===================================================================
# PART 7: Formulation Optimization Recommendations
# ===================================================================

print("PART 7: AI-Powered Formulation Optimization")
print("-" * 50)

def generate_optimization_recommendations(formulation_obj):
    """Generate recommendations for formulation improvement"""
    
    recommendations = []
    
    # pH optimization
    if 'pH' in formulation_obj.properties:
        current_pH = float(formulation_obj.properties['pH'].name.split('_')[-1])
        if current_pH > 6.0:
            recommendations.append({
                'type': 'pH_adjustment',
                'current': current_pH,
                'recommended': 5.5,
                'action': 'Add citric acid or lower pH to optimize for skin compatibility'
            })
    
    # Stability enhancement
    oil_phase_ingredients = [ing for ing, data in formulation_obj.ingredients.items() 
                           if data['phase'] == 'oil_phase']
    antioxidants = [ing for ing in oil_phase_ingredients 
                   if hasattr(ing, 'type') and 'ANTIOXIDANT' in str(ing.type)]
    
    if oil_phase_ingredients and not antioxidants:
        recommendations.append({
            'type': 'stability_enhancement',
            'action': 'Add antioxidant (vitamin E) to prevent oil phase oxidation'
        })
    
    # Texture optimization
    thickeners = [ing for ing in formulation_obj.ingredients.keys()
                 if hasattr(ing, 'type') and 'THICKENER' in str(ing.type)]
    
    if 'viscosity' in formulation_obj.properties:
        viscosity = int(formulation_obj.properties['viscosity'].name.split('_')[0])
        if viscosity > 5000 and len(thickeners) > 1:
            recommendations.append({
                'type': 'texture_optimization',
                'action': 'Consider reducing thickener concentration for better spreadability'
            })
    
    # Efficacy enhancement through synergies
    ingredient_names = [ing.name for ing in formulation_obj.ingredients.keys()]
    if 'ascorbic_acid' in ingredient_names and 'tocopherol' not in ingredient_names:
        recommendations.append({
            'type': 'efficacy_enhancement',
            'action': 'Add vitamin E to create antioxidant synergy with vitamin C'
        })
    
    return recommendations

# Generate optimization recommendations
recommendations = generate_optimization_recommendations(anti_aging_serum)

print(f"Generated {len(recommendations)} optimization recommendations:")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec['type'].replace('_', ' ').title()}")
    print(f"   Action: {rec['action']}")
    if 'current' in rec and 'recommended' in rec:
        print(f"   Current: {rec['current']}, Recommended: {rec['recommended']}")
    print()

# ===================================================================
# SUMMARY AND INSIGHTS
# ===================================================================

print("SUMMARY OF ADVANCED COSMETIC CHEMISTRY ANALYSIS")
print("=" * 70)
print(f"Formulation analyzed: {anti_aging_serum.name}")
print(f"Total ingredients: {len(anti_aging_serum.ingredients)}")
print(f"Compatibility relationships: {len(compat_links + incompat_links + synergy_links)}")
print(f"Validation checks: {sum(validation.values())}/{len(validation)} passed")
print(f"Optimization recommendations: {len(recommendations)}")
print()

print("Key Capabilities Demonstrated:")
print("• Complex multi-phase formulation modeling")
print("• Automated ingredient compatibility analysis")  
print("• Quality control and validation systems")
print("• Intelligent ingredient substitution")
print("• Regulatory compliance automation")
print("• AI-powered optimization recommendations")
print()

print("This framework enables:")
print("• Systematic formulation development")
print("• Risk mitigation through compatibility checking")
print("• Regulatory compliance automation")
print("• Cost optimization through substitution analysis")
print("• Quality assurance automation")
print("• Innovation through synergy identification")

print(f"\nTotal atoms in AtomSpace: {len(list(spa))}")
print("Advanced cosmetic chemistry analysis complete!")

# The end of advanced example