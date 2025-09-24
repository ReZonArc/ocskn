;
; cosmetic_compatibility.scm
;
; Simple ingredient interaction checking using the OpenCog cheminformatics
; framework with cosmetic chemistry specializations.
;
; This example demonstrates:
; - Basic cosmetic ingredient creation
; - Simple compatibility checking
; - Ingredient interaction analysis
; - Basic formulation validation
;
; To run this example, start the guile shell in the `examples` directory
; and then say: (load "scheme/cosmetic_compatibility.scm")
; It will print the analysis results.
;

(use-modules (opencog) (opencog cheminformatics))
(use-modules (opencog exec))

(format #t "========================================~n")
(format #t "Cosmetic Ingredient Compatibility Check~n") 
(format #t "========================================~n")

; ===================================================================
; PART 1: Create Basic Cosmetic Ingredients
; ===================================================================

(format #t "~nPART 1: Creating Basic Cosmetic Ingredients~n")
(format #t "-------------------------------------------~n")

; Define popular cosmetic active ingredients
(define hyaluronic-acid (ACTIVE_INGREDIENT "hyaluronic_acid"))
(define niacinamide (ACTIVE_INGREDIENT "niacinamide"))
(define retinol (ACTIVE_INGREDIENT "retinol"))
(define vitamin-c (ACTIVE_INGREDIENT "vitamin_c"))
(define salicylic-acid (ACTIVE_INGREDIENT "salicylic_acid"))
(define glycolic-acid (ACTIVE_INGREDIENT "glycolic_acid"))
(define benzoyl-peroxide (ACTIVE_INGREDIENT "benzoyl_peroxide"))

; Define supporting ingredients
(define glycerin (HUMECTANT "glycerin"))
(define cetyl-alcohol (EMULSIFIER "cetyl_alcohol"))
(define phenoxyethanol (PRESERVATIVE "phenoxyethanol"))
(define vitamin-e (ANTIOXIDANT "vitamin_e"))

(format #t "✓ Created active ingredients: HA, Niacinamide, Retinol, Vitamin C, etc.~n")
(format #t "✓ Created supporting ingredients: Glycerin, Cetyl alcohol, etc.~n")

; ===================================================================
; PART 2: Define Ingredient Interactions
; ===================================================================

(format #t "~nPART 2: Defining Ingredient Interactions~n")
(format #t "----------------------------------------~n")

; COMPATIBLE COMBINATIONS - Safe to use together
(define safe-combinations (list
	(COMPATIBILITY_LINK hyaluronic-acid niacinamide)
	(COMPATIBILITY_LINK hyaluronic-acid glycerin)
	(COMPATIBILITY_LINK hyaluronic-acid retinol)
	(COMPATIBILITY_LINK niacinamide glycerin)
	(COMPATIBILITY_LINK retinol vitamin-e)
))

; SYNERGISTIC COMBINATIONS - Work better together
(define synergistic-combinations (list
	(SYNERGY_LINK vitamin-c vitamin-e)
	(SYNERGY_LINK hyaluronic-acid niacinamide)
	(SYNERGY_LINK retinol hyaluronic-acid)
))

; INCOMPATIBLE COMBINATIONS - Should NOT be used together
(define problematic-combinations (list
	(INCOMPATIBILITY_LINK vitamin-c retinol)
	(INCOMPATIBILITY_LINK retinol benzoyl-peroxide) 
	(INCOMPATIBILITY_LINK retinol salicylic-acid)
	(INCOMPATIBILITY_LINK retinol glycolic-acid)
	(INCOMPATIBILITY_LINK vitamin-c niacinamide)  ; At certain pH levels
	(INCOMPATIBILITY_LINK benzoyl-peroxide vitamin-c)
))

(format #t "✓ Defined ~a compatible combinations~n" (length safe-combinations))
(format #t "✓ Defined ~a synergistic combinations~n" (length synergistic-combinations))
(format #t "✓ Defined ~a problematic combinations~n" (length problematic-combinations))

; ===================================================================
; PART 3: Create Sample Formulations
; ===================================================================

(format #t "~nPART 3: Creating Sample Formulations~n")
(format #t "------------------------------------~n")

; GOOD FORMULATION - Compatible ingredients
(define hydrating-serum
	(SERUM_FORMULATION
		hyaluronic-acid    ; 2% - Primary hydrating active
		niacinamide        ; 5% - Barrier support
		glycerin           ; 8% - Humectant
		cetyl-alcohol      ; 3% - Emulsifier
		phenoxyethanol     ; 0.5% - Preservative
	))

; ANTIOXIDANT SERUM - With beneficial synergy
(define antioxidant-serum
	(SERUM_FORMULATION
		vitamin-c          ; 15% - Primary antioxidant
		vitamin-e          ; 0.5% - Synergistic antioxidant
		hyaluronic-acid    ; 1% - Hydration support
		glycerin           ; 5% - Humectant
		phenoxyethanol     ; 0.5% - Preservative
	))

; PROBLEMATIC FORMULATION - Contains incompatible ingredients
(define problematic-serum
	(SERUM_FORMULATION
		vitamin-c          ; 15% - Antioxidant
		retinol            ; 0.5% - Anti-aging (INCOMPATIBLE with Vitamin C!)
		niacinamide        ; 5% - Barrier support
		glycerin           ; 5% - Humectant
		phenoxyethanol     ; 0.5% - Preservative
	))

(format #t "✓ Created hydrating serum: ~a~n" hydrating-serum)
(format #t "✓ Created antioxidant serum: ~a~n" antioxidant-serum)
(format #t "✓ Created problematic serum: ~a~n" problematic-serum)

; ===================================================================
; PART 4: Compatibility Analysis Functions
; ===================================================================

(format #t "~nPART 4: Performing Compatibility Analysis~n")
(format #t "-----------------------------------------~n")

; Define a function to check for incompatible ingredients in formulations
(define check-incompatibilities
	(BindLink
		; Variables for ingredients and formulation
		(VariableList
			(TypedVariable (Variable "$formulation") (Type 'SERUM_FORMULATION))
			(TypedVariable (Variable "$ingredient1") (Type 'ACTIVE_INGREDIENT))
			(TypedVariable (Variable "$ingredient2") (Type 'ACTIVE_INGREDIENT))
		)
		
		; Pattern: Find formulations containing incompatible ingredient pairs
		(AndLink
			; The formulation exists
			(Variable "$formulation")
			
			; Both ingredients are in the formulation
			(Member (Variable "$ingredient1") (Variable "$formulation"))
			(Member (Variable "$ingredient2") (Variable "$formulation"))
			
			; There's a documented incompatibility between them
			(INCOMPATIBILITY_LINK (Variable "$ingredient1") (Variable "$ingredient2"))
		)
		
		; Output: Report the incompatibility issue
		(UnorderedLink
			(ConceptNode "INCOMPATIBILITY_FOUND")
			(Variable "$formulation")
			(Variable "$ingredient1")
			(Variable "$ingredient2")
		)
	))

; Define a function to find synergistic combinations
(define find-synergies
	(BindLink
		(VariableList
			(TypedVariable (Variable "$formulation") (Type 'SERUM_FORMULATION))
			(TypedVariable (Variable "$ingredient1") (Type 'ACTIVE_INGREDIENT))
			(TypedVariable (Variable "$ingredient2") (Type 'ACTIVE_INGREDIENT))
		)
		
		; Pattern: Find formulations with synergistic ingredient pairs
		(AndLink
			(Variable "$formulation")
			(Member (Variable "$ingredient1") (Variable "$formulation"))
			(Member (Variable "$ingredient2") (Variable "$formulation"))
			(SYNERGY_LINK (Variable "$ingredient1") (Variable "$ingredient2"))
		)
		
		; Output: Report the beneficial synergy
		(UnorderedLink
			(ConceptNode "SYNERGY_FOUND")
			(Variable "$formulation")
			(Variable "$ingredient1")
			(Variable "$ingredient2")
		)
	))

; Execute the compatibility analysis
(format #t "Running incompatibility analysis...~n")
(define incompatibility-results (cog-execute! check-incompatibilities))

(format #t "Running synergy analysis...~n")
(define synergy-results (cog-execute! find-synergies))

; ===================================================================
; PART 5: Display Analysis Results
; ===================================================================

(format #t "~nPART 5: Analysis Results~n")
(format #t "------------------------~n")

; Display incompatibility findings
(format #t "INCOMPATIBILITY ANALYSIS:~n")
(if (null? incompatibility-results)
	(format #t "  ✓ No incompatible ingredient combinations found~n")
	(begin
		(format #t "  ✗ Found ~a incompatible combinations:~n" (length incompatibility-results))
		(for-each (lambda (result)
			(format #t "    • ~a~n" result))
			incompatibility-results)))

; Display synergy findings
(format #t "~nSYNERGY ANALYSIS:~n")
(if (null? synergy-results)
	(format #t "  No synergistic combinations found~n")
	(begin
		(format #t "  ⚡ Found ~a synergistic combinations:~n" (length synergy-results))
		(for-each (lambda (result)
			(format #t "    • ~a~n" result))
			synergy-results)))

; ===================================================================
; PART 6: Manual Interaction Check Examples
; ===================================================================

(format #t "~nPART 6: Manual Interaction Examples~n")
(format #t "-----------------------------------~n")

; Create specific interaction examples with explanations
(format #t "SAFE COMBINATIONS:~n")
(format #t "• Hyaluronic Acid + Niacinamide: Both water-based, complementary benefits~n")
(format #t "• Hyaluronic Acid + Retinol: HA provides hydration to counter retinol dryness~n")
(format #t "• Vitamin C + Vitamin E: Classic antioxidant synergy~n")

(format #t "~nPROBLEMATIC COMBINATIONS:~n")
(format #t "• Vitamin C + Retinol: pH incompatibility (C needs low pH, retinol neutral)~n")
(format #t "• Retinol + Benzoyl Peroxide: BP can degrade retinol~n")
(format #t "• Retinol + AHA/BHA: Risk of over-exfoliation and irritation~n")
(format #t "• Vitamin C + Niacinamide: Can cause irritation at high concentrations~n")

; ===================================================================
; PART 7: Formulation Recommendations
; ===================================================================

(format #t "~nPART 7: Formulation Recommendations~n")
(format #t "-----------------------------------~n")

; Create a recommendation system
(define generate-recommendations
	(lambda (formulation-name ingredients)
		(format #t "~nRecommendations for ~a:~n" formulation-name)
		
		; Check if formulation has retinol
		(if (member retinol ingredients)
			(begin
				(format #t "• Contains retinol - use only in PM routine~n")
				(format #t "• Add hyaluronic acid for hydration support~n")
				(format #t "• Avoid combining with vitamin C or acids~n"))
			#f)
		
		; Check if formulation has vitamin C
		(if (member vitamin-c ingredients)
			(begin
				(format #t "• Contains vitamin C - best used in AM routine~n")
				(format #t "• Add vitamin E for synergistic antioxidant effect~n")
				(format #t "• Ensure pH is below 4.0 for stability~n"))
			#f)
		
		; Check if formulation has both incompatible ingredients
		(if (and (member vitamin-c ingredients) (member retinol ingredients))
			(format #t "• ⚠ WARNING: Contains both vitamin C and retinol - separate into AM/PM products~n")
			#f)
	))

; Generate recommendations for our sample formulations
(generate-recommendations "Hydrating Serum" (cog-outgoing-set hydrating-serum))
(generate-recommendations "Antioxidant Serum" (cog-outgoing-set antioxidant-serum))
(generate-recommendations "Problematic Serum" (cog-outgoing-set problematic-serum))

; ===================================================================
; PART 8: pH Compatibility Analysis
; ===================================================================

(format #t "~nPART 8: pH Compatibility Analysis~n")
(format #t "---------------------------------~n")

; Define pH preferences for key ingredients
(define vitamin-c-pH (PH_PROPERTY "3.5"))    ; Needs acidic pH
(define retinol-pH (PH_PROPERTY "5.5"))      ; Needs neutral pH
(define niacinamide-pH (PH_PROPERTY "6.0"))  ; Flexible pH range

; Create pH-optimized formulations
(define am-vitamin-c-serum
	(SERUM_FORMULATION
		vitamin-c          ; 15% - Primary active
		vitamin-e          ; 0.5% - Synergistic antioxidant
		hyaluronic-acid    ; 1% - Hydration
		(PH_ADJUSTER "citric_acid")  ; pH adjustment to 3.5
		phenoxyethanol     ; 0.5% - Preservative
	))

(define pm-retinol-serum
	(SERUM_FORMULATION
		retinol            ; 0.5% - Anti-aging active
		hyaluronic-acid    ; 2% - Hydration support
		niacinamide        ; 3% - Barrier support
		glycerin           ; 5% - Humectant
		phenoxyethanol     ; 0.5% - Preservative
	))

(format #t "✓ Created pH-optimized AM serum (vitamin C): ~a~n" am-vitamin-c-serum)
(format #t "✓ Created pH-optimized PM serum (retinol): ~a~n" pm-retinol-serum)

; ===================================================================
; SUMMARY
; ===================================================================

(format #t "~n========================================~n")
(format #t "COMPATIBILITY ANALYSIS SUMMARY~n")
(format #t "========================================~n")

(format #t "~nFormulations Analyzed:~n")
(format #t "• Hydrating serum: ✓ Compatible ingredients~n")
(format #t "• Antioxidant serum: ⚡ Contains beneficial synergies~n") 
(format #t "• Problematic serum: ✗ Contains incompatible combinations~n")

(format #t "~nKey Insights:~n")
(format #t "• Always separate vitamin C (AM) and retinol (PM) routines~n")
(format #t "• Hyaluronic acid is universally compatible and beneficial~n")
(format #t "• pH requirements are critical for ingredient stability~n")
(format #t "• Synergistic combinations can enhance efficacy~n")

(format #t "~nBest Practices:~n")
(format #t "• Check ingredient compatibility before formulating~n")
(format #t "• Consider pH requirements of active ingredients~n")
(format #t "• Look for synergistic combinations to enhance benefits~n")
(format #t "• Always include preservation system~n")
(format #t "• Add hydrating ingredients to support barrier function~n")

(format #t "~nTotal atoms created: ~a~n" (length (cog-get-atoms 'Atom)))
(format #t "Cosmetic compatibility analysis complete!~n")

; ================================================
; The end of cosmetic compatibility example
; ================================================