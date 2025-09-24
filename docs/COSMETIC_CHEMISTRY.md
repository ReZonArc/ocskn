# Cosmetic Chemistry Framework

## Overview

This document provides comprehensive documentation for the cosmetic chemistry specializations in the OpenCog cheminformatics framework. The system extends the base cheminformatics atom types to provide domain-specific support for cosmetic formulation modeling, ingredient analysis, and regulatory compliance.

## Table of Contents

1. [Atom Type Reference](#atom-type-reference)
2. [Common Cosmetic Ingredients](#common-cosmetic-ingredients)  
3. [Formulation Guidelines](#formulation-guidelines)
4. [Regulatory Compliance](#regulatory-compliance)
5. [Advanced Applications](#advanced-applications)
6. [Usage Examples](#usage-examples)

## Atom Type Reference

### Ingredient Categories

The framework provides specialized atom types for categorizing cosmetic ingredients by their functional properties:

#### ACTIVE_INGREDIENT
Active ingredients that provide the primary benefit or function of the cosmetic product.

**Examples:**
- Retinol (anti-aging)
- Hyaluronic acid (hydration)
- Niacinamide (skin barrier)
- Salicylic acid (exfoliation)

#### PRESERVATIVE  
Ingredients that prevent microbial growth and extend product shelf life.

**Examples:**
- Phenoxyethanol
- Methylparaben
- Benzyl alcohol
- Potassium sorbate

#### EMULSIFIER
Ingredients that allow oil and water phases to mix and remain stable.

**Examples:**
- Cetyl alcohol
- Polysorbate 60
- Glyceryl stearate
- Lecithin

#### HUMECTANT
Ingredients that attract and retain moisture from the environment.

**Examples:**
- Glycerin
- Propylene glycol
- Sodium hyaluronate
- Betaine

#### SURFACTANT
Surface-active agents used for cleansing, foaming, or emulsifying.

**Examples:**
- Sodium lauryl sulfate
- Cocamidopropyl betaine
- Decyl glucoside
- Cetrimonium chloride

#### THICKENER
Ingredients that increase viscosity and improve product texture.

**Examples:**
- Xanthan gum
- Carbomer
- Hydroxyethylcellulose
- Cetyl alcohol

#### EMOLLIENT
Ingredients that soften and smooth the skin by forming an occlusive layer.

**Examples:**
- Squalane
- Jojoba oil
- Isopropyl myristate
- Shea butter

#### ANTIOXIDANT
Ingredients that prevent oxidation and rancidity of oils and other components.

**Examples:**
- Vitamin E (tocopherol)
- Vitamin C (ascorbic acid)
- BHT (butylated hydroxytoluene)
- Green tea extract

#### UV_FILTER
Ingredients that absorb, reflect, or scatter UV radiation for sun protection.

**Examples:**
- Zinc oxide
- Titanium dioxide
- Avobenzone
- Octinoxate

#### FRAGRANCE
Ingredients that provide scent to cosmetic products.

**Examples:**
- Essential oils
- Synthetic fragrances
- Fragrance compounds
- Perfume oils

#### COLORANT
Ingredients that provide color to cosmetic products.

**Examples:**
- Iron oxides
- Titanium dioxide
- Mica
- Synthetic dyes

#### PH_ADJUSTER
Ingredients used to adjust and maintain optimal pH levels.

**Examples:**
- Citric acid
- Sodium hydroxide
- Lactic acid
- Triethanolamine

### Formulation Types

#### SKINCARE_FORMULATION
Base type for all skincare products including moisturizers, serums, cleansers, and treatments.

**Subtypes:**
- MOISTURIZER_FORMULATION
- CLEANSER_FORMULATION  
- SERUM_FORMULATION
- CREAM_FORMULATION
- LOTION_FORMULATION
- TONER_FORMULATION

#### HAIRCARE_FORMULATION
Products designed for hair care including shampoos, conditioners, and styling products.

#### MAKEUP_FORMULATION
Decorative cosmetics including foundations, lipsticks, eyeshadows, and mascaras.

#### FRAGRANCE_FORMULATION
Perfumes, colognes, and scented products.

#### SUNCARE_FORMULATION
Sun protection products with SPF ratings.

#### BODYCARE_FORMULATION
Body lotions, oils, scrubs, and other body care products.

### Property Types

Physical and chemical properties that can be measured and optimized:

- **PH_PROPERTY**: Acidity/alkalinity (typical range 4.5-7.0 for skin products)
- **VISCOSITY_PROPERTY**: Flow characteristics (measured in centipoise)
- **STABILITY_PROPERTY**: Product stability over time and conditions
- **TEXTURE_PROPERTY**: Sensory feel and application properties
- **SPF_PROPERTY**: Sun protection factor for UV filters
- **SOLUBILITY_PROPERTY**: Solubility in water, oil, or other solvents

### Interaction Types

Relationships between ingredients:

- **COMPATIBILITY_LINK**: Ingredients that work well together
- **INCOMPATIBILITY_LINK**: Ingredients that should not be combined
- **SYNERGY_LINK**: Ingredients that enhance each other's effects
- **ANTAGONISM_LINK**: Ingredients that counteract each other's effects

### Safety and Regulatory Types

- **SAFETY_ASSESSMENT**: Safety evaluation data
- **ALLERGEN_CLASSIFICATION**: Known allergen status
- **CONCENTRATION_LIMIT**: Maximum safe usage levels
- **REGULATORY_STATUS**: Approval status in different regions

## Common Cosmetic Ingredients

### Hydrating Ingredients
| Ingredient | Type | Function | Typical % |
|------------|------|----------|-----------|
| Hyaluronic Acid | ACTIVE_INGREDIENT | Moisture retention | 0.1-2.0% |
| Glycerin | HUMECTANT | Moisture attraction | 1-10% |
| Sodium PCA | HUMECTANT | Natural moisturizing factor | 0.2-2.0% |
| Ceramides | ACTIVE_INGREDIENT | Barrier repair | 0.1-5.0% |

### Anti-Aging Ingredients
| Ingredient | Type | Function | Typical % |
|------------|------|----------|-----------|
| Retinol | ACTIVE_INGREDIENT | Cell turnover | 0.01-1.0% |
| Niacinamide | ACTIVE_INGREDIENT | Barrier function | 2-10% |
| Peptides | ACTIVE_INGREDIENT | Collagen synthesis | 0.1-10% |
| Vitamin C | ACTIVE_INGREDIENT/ANTIOXIDANT | Antioxidation | 5-20% |

### Cleansing Ingredients
| Ingredient | Type | Function | Typical % |
|------------|------|----------|-----------|
| Sodium Lauryl Sulfate | SURFACTANT | Primary cleanser | 5-15% |
| Cocamidopropyl Betaine | SURFACTANT | Mild cleanser | 3-8% |
| Decyl Glucoside | SURFACTANT | Gentle cleanser | 5-20% |

## Formulation Guidelines

### pH Considerations

**Optimal pH Ranges:**
- Cleansers: 5.5 - 7.0
- Moisturizers: 5.0 - 6.5  
- Serums: 4.0 - 6.0
- Sunscreens: 6.0 - 8.0

**pH-Sensitive Ingredients:**
- Vitamin C (ascorbic acid): pH < 3.5
- AHA/BHA: pH 3.0 - 4.0
- Retinol: pH 5.5 - 6.0

### Stability Factors

**Temperature Stability:**
- Heat-sensitive: Retinol, Vitamin C, peptides
- Heat-stable: Ceramides, hyaluronic acid, glycerin

**Light Stability:**
- Photosensitive: Retinol, Vitamin C, essential oils
- Light-stable: Zinc oxide, titanium dioxide

**Oxidation Susceptibility:**
- High risk: Vitamin C, oils, retinol
- Low risk: Glycerin, hyaluronic acid, ceramides

### Incompatible Combinations

**Known Incompatibilities:**
- Vitamin C + Retinol (pH incompatibility)
- AHA/BHA + Retinol (over-exfoliation)
- Niacinamide + Vitamin C (potential irritation at high pH)
- Benzoyl Peroxide + Retinol (degradation)

**Safe Combinations:**
- Hyaluronic Acid + Niacinamide
- Ceramides + Cholesterol + Fatty acids
- Vitamin C + Vitamin E (antioxidant synergy)
- Peptides + Hyaluronic acid

## Regulatory Compliance

### FDA Guidelines (US)
- Color additives must be FDA-approved
- Sunscreen active ingredients regulated as OTC drugs
- GRAS (Generally Recognized as Safe) substances
- Labeling requirements (INCI names)

### EU Regulations
- EU Cosmetics Regulation (EC) No 1223/2009
- Restricted substances list (Annex II)
- Concentration limits (Annex III)
- CPNP (Cosmetic Product Notification Portal) registration

### Common Restrictions
| Ingredient | EU Limit | US Status | Notes |
|------------|----------|-----------|-------|
| Hydroquinone | Banned | 2% OTC | Skin lightening |
| Formaldehyde | 0.2% | 0.2% | Preservative |
| Parabens | Varies | Generally allowed | Some restrictions |
| Essential oils | Allergen labeling | Generally allowed | Above 0.01% |

## Advanced Applications

### Formulation Optimization

The framework enables systematic optimization of cosmetic formulations through:

1. **Ingredient Selection**: Automated compatibility checking
2. **Concentration Optimization**: Based on efficacy and safety data
3. **Stability Prediction**: Analysis of degradation pathways
4. **Sensory Optimization**: Texture and feel predictions

### Ingredient Substitution

Finding compatible alternatives for:
- Allergenic ingredients
- Restricted substances
- Cost optimization
- Sustainability improvements

### Property Modeling

Predicting formulation properties:
- Viscosity from thickener combinations
- SPF from UV filter blends
- pH from buffer systems
- Stability from antioxidant systems

### Quality Control

Automated checking for:
- Regulatory compliance
- Concentration limits
- Incompatible combinations
- Missing essential ingredients

## Usage Examples

### Basic Ingredient Definition

```python
# Define cosmetic ingredients with functional classifications
hyaluronic_acid = ACTIVE_INGREDIENT('hyaluronic_acid')
glycerin = HUMECTANT('glycerin')
phenoxyethanol = PRESERVATIVE('phenoxyethanol')
cetyl_alcohol = EMULSIFIER('cetyl_alcohol')
```

### Formulation Creation

```python
# Create a moisturizer formulation
moisturizer = SKINCARE_FORMULATION(
    hyaluronic_acid,    # 1% - Hydrating active
    cetyl_alcohol,      # 3% - Emulsifier
    glycerin,           # 5% - Humectant
    phenoxyethanol      # 0.5% - Preservative
)
```

### Compatibility Analysis

```python
# Define ingredient interactions
compatible = COMPATIBILITY_LINK(hyaluronic_acid, niacinamide)
incompatible = INCOMPATIBILITY_LINK(vitamin_c, retinol)
synergy = SYNERGY_LINK(vitamin_c, vitamin_e)
```

### Property Assignment

```python
# Assign properties to formulations
ph_value = PH_PROPERTY('5.5')
viscosity = VISCOSITY_PROPERTY('2000_cP')
texture = TEXTURE_PROPERTY('lightweight_cream')

moisturizer_properties = UNORDERED_LINK(
    moisturizer,
    ph_value,
    viscosity,
    texture
)
```

### Safety Assessment

```python
# Define safety and regulatory information
safety_data = SAFETY_ASSESSMENT('dermatologically_tested')
allergen_info = ALLERGEN_CLASSIFICATION('fragrance_free')
concentration = CONCENTRATION_LIMIT('retinol_0.1%_max')

product_safety = UNORDERED_LINK(
    moisturizer,
    safety_data,
    allergen_info,
    concentration
)
```

This framework provides a comprehensive foundation for computational cosmetic chemistry, enabling systematic analysis and optimization of cosmetic formulations through knowledge representation and reasoning within the OpenCog framework.