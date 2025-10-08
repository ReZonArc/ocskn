#!/usr/bin/env guile
!#
;
; planar-demo.scm -- Demonstration of planar graph constraints
;
; This example shows how to use the new planar graph constraints
; functionality to ensure generated networks maintain planarity.
; This is essential for natural language generation where word 
; order must be preserved.

(use-modules (opencog) (opencog generate))

(define demo-as (cog-new-atomspace))
(cog-set-atomspace! demo-as)

; Define some word nodes for our example sentence
(define words
   (list
      (ConceptNode "the")
      (ConceptNode "cat")
      (ConceptNode "sat")
      (ConceptNode "on")
      (ConceptNode "mat")))

; Define a simple dictionary with sections for each word
; Each section has connectors that define how words can link
(define dict
   (list
      ; "the" - determiner with right connector
      (Section
         (ConceptNode "the")
         (ConnectorSeq
            (Connector
               (ConceptNode "det")
               (ConnectorDir "+"))))
      
      ; "cat" - noun with left det connector, right verb connector  
      (Section
         (ConceptNode "cat")
         (ConnectorSeq
            (Connector
               (ConceptNode "det")
               (ConnectorDir "-"))
            (Connector
               (ConceptNode "subj")
               (ConnectorDir "+"))))
      
      ; "sat" - verb with left subject, right prep connector
      (Section
         (ConceptNode "sat") 
         (ConnectorSeq
            (Connector
               (ConceptNode "subj")
               (ConnectorDir "-"))
            (Connector
               (ConceptNode "prep")
               (ConnectorDir "+"))))
      
      ; "on" - preposition with left verb, right noun connector
      (Section
         (ConceptNode "on")
         (ConnectorSeq
            (Connector
               (ConceptNode "prep")
               (ConnectorDir "-"))
            (Connector
               (ConceptNode "obj")
               (ConnectorDir "+"))))
      
      ; "mat" - noun with left obj connector
      (Section
         (ConceptNode "mat")
         (ConnectorSeq
            (Connector
               (ConceptNode "obj")
               (ConnectorDir "-"))))))

; Create a dictionary object from our sections
(define my-dict (make-dictionary dict))

; Display the dictionary contents
(format #t "Created dictionary with ~a sections:\n" (length dict))
(for-each (lambda (sect) 
   (format #t "  ~a\n" sect)) dict)
(newline)

; Demonstrate basic planar constraint checking
(format #t "=== Planar Constraints Demo ===\n")
(format #t "Word sequence: ~a\n" (map cog-name words))

; In a real application, you would:
; 1. Create a PlanarCallback with the dictionary
; 2. Set the initial word sequence 
; 3. Use the Aggregate class with the PlanarCallback
; 4. Generate planar sentence structures

(format #t "\nThis demo shows the basic setup for planar generation.\n")
(format #t "The actual generation would be done in C++ using:\n")
(format #t "  - PlanarConstraints class for planarity checking\n")
(format #t "  - PlanarCallback class for planar-aware generation\n")  
(format #t "  - Integration with existing Aggregate generation system\n")
(newline)

; Example of what a planar sentence structure would look like:
; "the cat sat on mat" with links:
; the-cat (det), cat-sat (subj), sat-on (prep), on-mat (obj)
; These links don't cross when drawn above the sentence.

(format #t "Example planar sentence links:\n")
(format #t "  the --det--> cat\n")
(format #t "  cat --subj--> sat\n") 
(format #t "  sat --prep--> on\n")
(format #t "  on --obj--> mat\n")
(format #t "\nThese links form a planar graph when drawn above the words.\n")

; Clean up
(cog-set-atomspace! #f)