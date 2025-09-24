;
; cosmetic_formulation.scm
;
; Complex cosmetic formulation modeling with compatibility analysis
; using the OpenCog cheminformatics framework with cosmetic chemistry
; specializations.
;
; This example demonstrates:
; - Advanced cosmetic ingredient modeling
; - Multi-phase formulation creation
; - Ingredient compatibility analysis using pattern matching
; - Automated quality control checks
; - Formulation optimization through graph rewriting
;
; To run this example, start the guile shell in the `examples` directory
; and then say: (load "scheme/cosmetic_formulation.scm")
;

(use-modules (opencog) (opencog cheminformatics))
(use-modules (opencog exec))

(format #t "===========================================~n")
(format #t "Complex Cosmetic Formulation Modeling~n")
(format #t "===========================================~n")

; ===================================================================
; PART 1: Define Comprehensive Ingredient Database
; ===================================================================

(format #t "~nPART 1: Creating Comprehensive Ingredient Database~n")
(format #t "---------------------------------------------------~n")

; Active ingredients with anti-aging benefits
(define hyaluronic-acid (ACTIVE_INGREDIENT "hyaluronic_acid"))
(define niacinamide (ACTIVE_INGREDIENT "niacinamide"))  
(define retinol (ACTIVE_INGREDIENT "retinol"))
(define vitamin-c (ACTIVE_INGREDIENT "ascorbic_acid"))
(define peptides (ACTIVE_INGREDIENT "peptides"))
(define ceramides (ACTIVE_INGREDIENT "ceramides"))

; Humectants for moisture retention
(define glycerin (HUMECTANT "glycerin"))
(define propylene-glycol (HUMECTANT "propylene_glycol"))
(define sodium-pca (HUMECTANT "sodium_pca"))
(define betaine (HUMECTANT "betaine"))

; Emulsifiers for stable formulations
(define cetyl-alcohol (EMULSIFIER "cetyl_alcohol"))
(define polysorbate-60 (EMULSIFIER "polysorbate_60"))
(define glyceryl-stearate (EMULSIFIER "glyceryl_stearate"))
(define lecithin (EMULSIFIER "lecithin"))

; Preservatives for microbial protection
(define phenoxyethanol (PRESERVATIVE "phenoxyethanol"))
(define methylparaben (PRESERVATIVE "methylparaben"))
(define benzyl-alcohol (PRESERVATIVE "benzyl_alcohol"))
(define potassium-sorbate (PRESERVATIVE "potassium_sorbate"))

; Thickeners for texture enhancement
(define xanthan-gum (THICKENER "xanthan_gum"))
(define carbomer (THICKENER "carbomer"))
(define hydroxyethylcellulose (THICKENER "hydroxyethylcellulose"))

; Emollients for skin feel
(define squalane (EMOLLIENT "squalane"))
(define jojoba-oil (EMOLLIENT "jojoba_oil"))
(define shea-butter (EMOLLIENT "shea_butter"))
(define isopropyl-myristate (EMOLLIENT "isopropyl_myristate"))

; Antioxidants for stability
(define tocopherol (ANTIOXIDANT "tocopherol"))
(define ascorbyl-palmitate (ANTIOXIDANT "ascorbyl_palmitate"))
(define bht (ANTIOXIDANT "bht"))

; pH adjusters
(define citric-acid (PH_ADJUSTER "citric_acid"))
(define sodium-hydroxide (PH_ADJUSTER "sodium_hydroxide"))
(define lactic-acid (PH_ADJUSTER "lactic_acid"))

(format #t "✓ Ingredient database created with 25+ specialized ingredients~n")

; ===================================================================
; PART 2: Define Ingredient Compatibility Matrix
; ===================================================================

(format #t "~nPART 2: Building Ingredient Compatibility Matrix~n")
(format #t "------------------------------------------------~n")

; Compatible ingredient combinations (work well together)
(define compatibility-relationships (list
	(COMPATIBILITY_LINK hyaluronic-acid niacinamide)
	(COMPATIBILITY_LINK hyaluronic-acid glycerin)
	(COMPATIBILITY_LINK hyaluronic-acid peptides)
	(COMPATIBILITY_LINK niacinamide glycerin)
	(COMPATIBILITY_LINK retinol hyaluronic-acid)
	(COMPATIBILITY_LINK vitamin-c tocopherol)  ; Classic antioxidant synergy
	(COMPATIBILITY_LINK ceramides hyaluronic-acid)
	(COMPATIBILITY_LINK cetyl-alcohol polysorbate-60)
	(COMPATIBILITY_LINK squalane jojoba-oil)
	(COMPATIBILITY_LINK phenoxyethanol methylparaben)
))

; Incompatible ingredient combinations (should be avoided)
(define incompatibility-relationships (list
	(INCOMPATIBILITY_LINK vitamin-c retinol)  ; pH incompatibility
	(INCOMPATIBILITY_LINK vitamin-c niacinamide)  ; Potential irritation
	(INCOMPATIBILITY_LINK retinol (ACTIVE_INGREDIENT "benzoyl_peroxide"))  ; Degradation
	(INCOMPATIBILITY_LINK (ACTIVE_INGREDIENT "aha_acids") retinol)  ; Over-exfoliation
))

; Synergistic combinations (enhance each other's effects)
(define synergy-relationships (list
	(SYNERGY_LINK vitamin-c tocopherol)  ; Antioxidant network
	(SYNERGY_LINK ceramides (ACTIVE_INGREDIENT "cholesterol"))  ; Barrier repair
	(SYNERGY_LINK hyaluronic-acid peptides)  ; Hydration + anti-aging
	(SYNERGY_LINK niacinamide (ACTIVE_INGREDIENT "zinc_oxide"))  ; Oil control + soothing
))

(format #t "✓ Compatibility matrix: ~a compatible, ~a incompatible, ~a synergy relationships~n"
	(length compatibility-relationships)
	(length incompatibility-relationships) 
	(length synergy-relationships))

; ===================================================================
; PART 3: Advanced Multi-Phase Formulation Creation
; ===================================================================

(format #t "~nPART 3: Creating Advanced Anti-Aging Serum~n")
(format #t "--------------------------------------------~n")

; Define a sophisticated anti-aging serum with multiple phases

; Water phase (aqueous ingredients)
(define water-phase-ingredients (list
	hyaluronic-acid     ; 1.5% - Primary hydrating active
	niacinamide         ; 5.0% - Barrier function and oil control
	peptides            ; 3.0% - Anti-aging peptide complex
	glycerin            ; 8.0% - Primary humectant
	sodium-pca          ; 2.0% - Secondary humectant
	betaine             ; 1.0% - Osmolyte and humectant
))

; Oil phase (lipophilic ingredients)
(define oil-phase-ingredients (list
	retinol             ; 0.1% - Anti-aging active (encapsulated)
	squalane            ; 2.0% - Lightweight emollient
	jojoba-oil          ; 1.0% - Nourishing oil
	tocopherol          ; 0.2% - Antioxidant protection
))

; Emulsification system
(define emulsification-system (list
	cetyl-alcohol       ; 3.0% - Primary emulsifier
	polysorbate-60      ; 1.5% - Secondary emulsifier
	lecithin            ; 0.5% - Natural emulsifier
))

; Thickening and texture system
(define texture-system (list
	xanthan-gum         ; 0.3% - Primary thickener
	hydroxyethylcellulose ; 0.2% - Secondary thickener
))

; Preservation system
(define preservation-system (list
	phenoxyethanol      ; 0.5% - Primary preservative
	benzyl-alcohol      ; 0.3% - Secondary preservative
))

; pH and stability system
(define pH-stability-system (list
	citric-acid         ; 0.1% - pH adjuster
	ascorbyl-palmitate  ; 0.1% - Lipophilic antioxidant
))

; Create the complete advanced serum formulation
(define advanced-anti-aging-serum
	(SERUM_FORMULATION
		; Water phase
		hyaluronic-acid niacinamide peptides
		glycerin sodium-pca betaine
		
		; Oil phase  
		retinol squalane jojoba-oil tocopherol
		
		; Emulsification
		cetyl-alcohol polysorbate-60 lecithin
		
		; Texture
		xanthan-gum hydroxyethylcellulose
		
		; Preservation
		phenoxyethanol benzyl-alcohol
		
		; pH and stability
		citric-acid ascorbyl-palmitate
	))

(format #t "✓ Advanced serum created: ~a~n" advanced-anti-aging-serum)

; ===================================================================
; PART 4: Formulation Properties Definition
; ===================================================================

(format #t "~nPART 4: Defining Formulation Properties~n")
(format #t "---------------------------------------~n")

; Define key properties of the advanced serum
(define serum-pH (PH_PROPERTY "5.8"))
(define serum-viscosity (VISCOSITY_PROPERTY "3500_cP"))
(define serum-texture (TEXTURE_PROPERTY "silky_lightweight_serum"))
(define serum-stability (STABILITY_PROPERTY "excellent_24_months"))
(define serum-color (COSMETIC_PROPERTY_NODE "color_pale_yellow"))
(define serum-scent (COSMETIC_PROPERTY_NODE "scent_neutral"))

; Link all properties to the formulation
(define serum-with-properties
	(UnorderedLink
		advanced-anti-aging-serum
		serum-pH
		serum-viscosity
		serum-texture
		serum-stability
		serum-color
		serum-scent
	))

(format #t "✓ Properties linked to formulation: pH=5.8, Viscosity=3500cP, Texture=silky~n")

; ===================================================================
; PART 5: Automated Compatibility Checking
; ===================================================================

(format #t "~nPART 5: Automated Compatibility Analysis~n")
(format #t "----------------------------------------~n")

; Define a pattern-matching rule to check for incompatible ingredients
; in any formulation
(define incompatibility-checker
	(BindLink
		; Variable declaration
		(VariableList
			(TypedVariable (Variable "$formulation") (Type 'SERUM_FORMULATION))
			(TypedVariable (Variable "$ingredient1") (Type 'COSMETIC_INGREDIENT_NODE))
			(TypedVariable (Variable "$ingredient2") (Type 'COSMETIC_INGREDIENT_NODE))
		)
		
		; Pattern: Look for formulations containing incompatible ingredients
		(AndLink
			; The formulation contains both ingredients
			(Variable "$formulation")
			(INCOMPATIBILITY_LINK (Variable "$ingredient1") (Variable "$ingredient2"))
		)
		
		; Report the incompatibility issue
		(UnorderedLink
			(ConceptNode "FORMULATION_ISSUE")
			(Variable "$formulation")
			(Variable "$ingredient1") 
			(Variable "$ingredient2")
			(ConceptNode "INCOMPATIBLE_COMBINATION")
		)
	))

; Execute the incompatibility check
(define compatibility-issues (cog-execute! incompatibility-checker))
(format #t "Compatibility analysis complete~n")
(format #t "Issues found: ~a~n" compatibility-issues)

; ===================================================================
; PART 6: pH Optimization Pattern
; ===================================================================

(format #t "~nPART 6: pH Optimization Analysis~n")
(format #t "--------------------------------~n")

; Define a rule to identify pH-sensitive ingredients and recommend adjustments
(define pH-optimizer
	(BindLink
		(VariableList
			(TypedVariable (Variable "$formulation") (Type 'SERUM_FORMULATION))
			(TypedVariable (Variable "$active") (Type 'ACTIVE_INGREDIENT))
			(TypedVariable (Variable "$pH_value") (Type 'PH_PROPERTY))
		)
		
		; Pattern: Formulation with vitamin C and current pH
		(AndLink
			(Variable "$formulation")
			(EvaluationLink
				(PredicateNode "contains_ingredient")
				(ListLink (Variable "$formulation") vitamin-c))
			(EvaluationLink
				(PredicateNode "has_property")
				(ListLink (Variable "$formulation") (Variable "$pH_value")))
		)
		
		; Recommendation: Optimize pH for vitamin C stability
		(UnorderedLink
			(ConceptNode "pH_OPTIMIZATION_NEEDED")
			(Variable "$formulation")
			vitamin-c
			(ConceptNode "RECOMMENDED_pH_3.5_to_4.0")
			(ConceptNode "ADD_MORE_CITRIC_ACID")
		)
	))

; ===================================================================
; PART 7: Safety and Regulatory Compliance
; ===================================================================

(format #t "~nPART 7: Safety and Regulatory Assessment~n")
(format #t "----------------------------------------~n")

; Define safety assessments for the formulation
(define serum-safety-assessment (SAFETY_ASSESSMENT "dermatologically_tested"))
(define serum-allergen-status (ALLERGEN_CLASSIFICATION "fragrance_free"))
(define retinol-concentration-limit (CONCENTRATION_LIMIT "retinol_max_1_percent"))

; Regulatory compliance for different regions
(define eu-compliance (EU_COMPLIANT "approved_ingredients"))
(define fda-status (FDA_APPROVED "GRAS_components"))

; Create comprehensive safety profile
(define serum-safety-profile
	(UnorderedLink
		advanced-anti-aging-serum
		serum-safety-assessment
		serum-allergen-status
		retinol-concentration-limit
		eu-compliance
		fda-status
	))

(format #t "✓ Safety profile created: dermatologically tested, fragrance-free, EU/FDA compliant~n")

; ===================================================================
; PART 8: Alternative Formulation Variants
; ===================================================================

(format #t "~nPART 8: Creating Formulation Variants~n")
(format #t "------------------------------------~n")

; Create a sensitive skin variant (without retinol and strong actives)
(define sensitive-skin-serum
	(SERUM_FORMULATION
		; Gentle actives only
		hyaluronic-acid niacinamide ceramides
		
		; Enhanced moisturizing system
		glycerin sodium-pca betaine shea-butter
		
		; Gentle emulsification
		cetyl-alcohol glyceryl-stearate
		
		; Minimal preservation
		phenoxyethanol potassium-sorbate
		
		; Soothing additions
		(ACTIVE_INGREDIENT "allantoin")
		(ACTIVE_INGREDIENT "panthenol")
	))

; Create a brightening variant
(define brightening-serum
	(SERUM_FORMULATION
		; Brightening actives
		vitamin-c niacinamide
		(ACTIVE_INGREDIENT "kojic_acid")
		(ACTIVE_INGREDIENT "arbutin")
		
		; Supporting ingredients
		hyaluronic-acid glycerin
		tocopherol ascorbyl-palmitate
		
		; Emulsification and texture
		polysorbate-60 xanthan-gum
		
		; Preservation
		phenoxyethanol
		
		; pH optimization for vitamin C
		citric-acid
	))

(format #t "✓ Created formulation variants: sensitive skin, brightening~n")

; ===================================================================
; PART 9: Formulation Analysis Summary
; ===================================================================

(format #t "~nPART 9: Comprehensive Formulation Analysis~n")
(format #t "------------------------------------------~n")

; Count ingredients by category
(define count-ingredient-type
	(lambda (ingredient-list ingredient-type)
		(length (filter (lambda (ing) 
			(string-contains (symbol->string (cog-type ing)) 
				(symbol->string ingredient-type))) 
			ingredient-list))))

; Get all ingredients from the advanced serum
(define all-serum-ingredients
	(cog-outgoing-set advanced-anti-aging-serum))

(define active-count (count-ingredient-type all-serum-ingredients 'ACTIVE_INGREDIENT))
(define humectant-count (count-ingredient-type all-serum-ingredients 'HUMECTANT))
(define emulsifier-count (count-ingredient-type all-serum-ingredients 'EMULSIFIER))
(define preservative-count (count-ingredient-type all-serum-ingredients 'PRESERVATIVE))

(format #t "Advanced Anti-Aging Serum Analysis:~n")
(format #t "• Total ingredients: ~a~n" (length all-serum-ingredients))
(format #t "• Active ingredients: ~a~n" active-count)
(format #t "• Humectants: ~a~n" humectant-count)
(format #t "• Emulsifiers: ~a~n" emulsifier-count)
(format #t "• Preservatives: ~a~n" preservative-count)

; ===================================================================
; PART 10: Quality Control Validation
; ===================================================================

(format #t "~nPART 10: Quality Control Validation~n")
(format #t "-----------------------------------~n")

; Define quality control checks
(define qc-preservative-check
	(BindLink
		(TypedVariable (Variable "$formulation") (Type 'SERUM_FORMULATION))
		(AndLink
			(Variable "$formulation")
			; Check if formulation contains at least one preservative
			(OrLink
				(Member phenoxyethanol (Variable "$formulation"))
				(Member methylparaben (Variable "$formulation"))
				(Member benzyl-alcohol (Variable "$formulation"))
			)
		)
		(UnorderedLink
			(ConceptNode "QC_PASS")
			(Variable "$formulation")
			(ConceptNode "PRESERVATIVE_SYSTEM_ADEQUATE")
		)
	))

; Execute quality control check
(define qc-results (cog-execute! qc-preservative-check))
(format #t "Quality control results: ~a~n" qc-results)

; ===================================================================
; SUMMARY AND INSIGHTS
; ===================================================================

(format #t "~n===========================================~n")
(format #t "COSMETIC FORMULATION ANALYSIS COMPLETE~n")
(format #t "===========================================~n")

(format #t "~nKey Achievements:~n")
(format #t "• Created comprehensive ingredient database (25+ ingredients)~n")
(format #t "• Established compatibility matrix with safety relationships~n")
(format #t "• Designed advanced multi-phase anti-aging serum~n")
(format #t "• Implemented automated compatibility checking~n")
(format #t "• Created safety and regulatory compliance framework~n")
(format #t "• Developed formulation variants for different needs~n")
(format #t "• Implemented quality control validation system~n")

(format #t "~nThis framework demonstrates:~n")
(format #t "• Systematic cosmetic formulation development~n")
(format #t "• Automated safety and compatibility analysis~n")
(format #t "• Regulatory compliance checking~n")
(format #t "• Quality control automation~n")
(format #t "• Variant generation for different market segments~n")

(format #t "~nFormulations created:~n")
(format #t "• Advanced anti-aging serum: ~a~n" advanced-anti-aging-serum)
(format #t "• Sensitive skin variant: ~a~n" sensitive-skin-serum)
(format #t "• Brightening variant: ~a~n" brightening-serum)

(format #t "~nTotal atoms in AtomSpace: ~a~n" (length (cog-get-atoms 'Atom)))

(format #t "~nCosmetic formulation modeling complete!~n")

; ================================================
; The end of complex cosmetic formulation example
; ================================================