#! /usr/bin/env python3
#
# cosmetic_intro_example.py
#
# Basic introduction to cosmetic chemistry atom types in the OpenCog 
# cheminformatics framework. This example demonstrates the fundamental
# concepts of cosmetic ingredient modeling and basic formulation creation.
#
# This example shows:
# - Creating cosmetic ingredients with functional classifications
# - Basic formulation assembly
# - Simple property assignment
# - Ingredient categorization
#
# --------------------------------------------------------------

# Import the AtomSpace, and the basic AtomSpace types
from opencog.atomspace import AtomSpace
from opencog.type_constructors import *

# Import all of the chemical element types, bond types, and cosmetic types
from opencog.cheminformatics import *

# Nothing works without a default AtomSpace, so create that first.
spa = AtomSpace()
set_default_atomspace(spa)

print("=" * 60)
print("Cosmetic Chemistry Introduction Example")
print("=" * 60)
print(f'AtomSpace initialized: {spa}')
print()

# ===================================================================
# PART 1: Basic Ingredient Creation
# ===================================================================

print("PART 1: Creating Basic Cosmetic Ingredients")
print("-" * 40)

# Create different types of cosmetic ingredients
# Each ingredient is classified by its primary function

# Active ingredients - provide primary benefits
hyaluronic_acid = ACTIVE_INGREDIENT('hyaluronic_acid')
niacinamide = ACTIVE_INGREDIENT('niacinamide')
retinol = ACTIVE_INGREDIENT('retinol')

print(f"Active ingredient: {hyaluronic_acid}")
print(f"Active ingredient: {niacinamide}")
print(f"Active ingredient: {retinol}")

# Functional ingredients - support formulation stability and feel
glycerin = HUMECTANT('glycerin')
cetyl_alcohol = EMULSIFIER('cetyl_alcohol')
phenoxyethanol = PRESERVATIVE('phenoxyethanol')
xanthan_gum = THICKENER('xanthan_gum')

print(f"Humectant: {glycerin}")
print(f"Emulsifier: {cetyl_alcohol}")
print(f"Preservative: {phenoxyethanol}")
print(f"Thickener: {xanthan_gum}")

# Sensory ingredients - improve user experience
squalane = EMOLLIENT('squalane')
fragrance_compound = FRAGRANCE('lavender_essential_oil')

print(f"Emollient: {squalane}")
print(f"Fragrance: {fragrance_compound}")
print()

# ===================================================================
# PART 2: Basic Formulation Creation
# ===================================================================

print("PART 2: Creating a Simple Moisturizer Formulation")
print("-" * 40)

# Create a basic moisturizer using the ingredients defined above
# This represents a water-in-oil emulsion with hydrating actives

basic_moisturizer = MOISTURIZER_FORMULATION(
    hyaluronic_acid,    # 1% - Primary hydrating active
    glycerin,           # 5% - Secondary humectant
    cetyl_alcohol,      # 3% - Emulsifier and texture enhancer
    squalane,           # 2% - Lightweight emollient
    phenoxyethanol,     # 0.5% - Preservative system
    xanthan_gum         # 0.2% - Thickener for viscosity
)

print(f"Basic moisturizer: {basic_moisturizer}")
print()

# ===================================================================
# PART 3: Property Assignment
# ===================================================================

print("PART 3: Assigning Properties to Formulations")
print("-" * 40)

# Define key properties of the moisturizer formulation
ph_level = PH_PROPERTY('5.5')
viscosity_value = VISCOSITY_PROPERTY('2000_cP')
texture_feel = TEXTURE_PROPERTY('lightweight_cream')
stability_rating = STABILITY_PROPERTY('excellent')

print(f"pH property: {ph_level}")
print(f"Viscosity property: {viscosity_value}")
print(f"Texture property: {texture_feel}")
print(f"Stability property: {stability_rating}")

# Link properties to the formulation
moisturizer_with_properties = UnorderedLink(
    basic_moisturizer,
    ph_level,
    viscosity_value,
    texture_feel,
    stability_rating
)

print(f"Moisturizer with properties: {moisturizer_with_properties}")
print()

# ===================================================================
# PART 4: Advanced Ingredient Types
# ===================================================================

print("PART 4: Specialized Cosmetic Ingredients")
print("-" * 40)

# UV protection ingredients
zinc_oxide = UV_FILTER('zinc_oxide')
titanium_dioxide = UV_FILTER('titanium_dioxide')

# Color cosmetics
iron_oxide_red = COLORANT('iron_oxide_red')
mica = COLORANT('mica')

# pH adjustment
citric_acid = PH_ADJUSTER('citric_acid')

# Antioxidants
vitamin_e = ANTIOXIDANT('tocopherol')
vitamin_c = ANTIOXIDANT('ascorbic_acid')

print(f"UV filters: {zinc_oxide}, {titanium_dioxide}")
print(f"Colorants: {iron_oxide_red}, {mica}")
print(f"pH adjuster: {citric_acid}")
print(f"Antioxidants: {vitamin_e}, {vitamin_c}")
print()

# ===================================================================
# PART 5: Creating Different Product Types
# ===================================================================

print("PART 5: Different Cosmetic Product Formulations")
print("-" * 40)

# Sunscreen formulation
sunscreen = SUNCARE_FORMULATION(
    zinc_oxide,         # 15% - Primary UV filter
    titanium_dioxide,   # 5% - Secondary UV filter
    cetyl_alcohol,      # Emulsifier
    glycerin,           # Humectant
    phenoxyethanol      # Preservative
)

# Hair care formulation
shampoo = HAIRCARE_FORMULATION(
    SodiumLaurylSulfate := SURFACTANT('sodium_lauryl_sulfate'),  # Primary cleanser
    CocoamidopropylBetaine := SURFACTANT('cocamidopropyl_betaine'),  # Secondary surfactant
    Panthenol := ACTIVE_INGREDIENT('panthenol'),  # Hair conditioning agent
    phenoxyethanol      # Preservative
)

# Makeup formulation
foundation = MAKEUP_FORMULATION(
    iron_oxide_red,     # Color pigment
    mica,               # Texture enhancer
    titanium_dioxide,   # Coverage and SPF
    squalane,           # Emollient base
    phenoxyethanol      # Preservative
)

print(f"Sunscreen: {sunscreen}")
print(f"Shampoo: {shampoo}")
print(f"Foundation: {foundation}")
print()

# ===================================================================
# PART 6: Safety and Regulatory Information
# ===================================================================

print("PART 6: Safety and Regulatory Considerations")
print("-" * 40)

# Safety assessments
safety_tested = SAFETY_ASSESSMENT('dermatologically_tested')
allergen_free = ALLERGEN_CLASSIFICATION('fragrance_free')
concentration_limit = CONCENTRATION_LIMIT('retinol_max_1_percent')

# Regulatory status
fda_status = FDA_APPROVED('GRAS_ingredient')
eu_status = EU_COMPLIANT('approved_for_cosmetic_use')

print(f"Safety assessment: {safety_tested}")
print(f"Allergen classification: {allergen_free}")
print(f"Concentration limit: {concentration_limit}")
print(f"FDA status: {fda_status}")
print(f"EU status: {eu_status}")
print()

# ===================================================================
# SUMMARY AND NEXT STEPS
# ===================================================================

print("SUMMARY")
print("-" * 40)
print("This introduction covered:")
print("• Basic cosmetic ingredient classification")
print("• Simple formulation creation")
print("• Property assignment to formulations")
print("• Different product category examples")
print("• Safety and regulatory considerations")
print()
print("Next steps:")
print("• Explore advanced formulation optimization")
print("• Learn about ingredient compatibility analysis")
print("• Study stability and pH interactions")
print("• Review regulatory compliance automation")
print()
print("See cosmetic_chemistry_example.py for advanced techniques!")

# Print final AtomSpace summary
print(f"Final AtomSpace contains {len(list(spa))} atoms")

# The end.
# That's all for the introduction!