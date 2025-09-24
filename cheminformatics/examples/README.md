# Examples

This directory contains examples of defining atoms, bonds, molecules
and reactions in [Atomese](https://wiki.opencog.org/w/Atomese)
using several different execution environments: 1) Scheme, 2) Python,
3) Python within Jupyter notebooks.  Recall that Atomese can be freely
mixed between scheme and python: under the covers, the data is always in
Atomese, and not in the programming language environment itself.
(See the examples in the core AtomSpace git repo for demos.)

## Python

Changedir to the `python` directory and use the Python 3 interpreter
to run scripts there:

```
$ python3 intro_example.py
```

This is the most basic demo: it shows how to create a single atom, a single
chemical bond, and a methane molecule.

### Cosmetic Chemistry Examples

The framework now includes specialized examples for cosmetic chemistry applications:

```
$ python3 cosmetic_intro_example.py
```

This introduction demonstrates basic cosmetic ingredient modeling, including:
- Creating cosmetic ingredients with functional classifications
- Basic formulation assembly (moisturizer example)
- Property assignment (pH, viscosity, texture)
- Different product category examples
- Safety and regulatory considerations

```
$ python3 cosmetic_chemistry_example.py
```

This advanced example shows sophisticated cosmetic formulation analysis:
- Complex multi-phase formulation design
- Ingredient compatibility and interaction analysis
- Automated quality control validation
- Intelligent ingredient substitution
- Regulatory compliance checking
- AI-powered optimization recommendations

If you run python virtualenv, and are experiencing issues with undefined
symbols, then try adding `/usr/local/lib/python3.11/dist-packages/`
to your `PYTHON_PATH` and adding `/usr/local/lib/opencog/` to your
`LD_LIBRARY_PATH`.

## Scheme

The scheme directory contains complex examples that demonstrate the power
of the AtomSpace query engine for chemical and cosmetic formulation analysis.

### Chemical Reaction Example

The original chemistry example uses the AtomSpace query engine to define 
a rewrite rule that performs an esterification reaction. Although written 
in scheme, it could also be re-written in python, by re-arranging the 
parenthesis. (This isn't hard, just tedious.)

Changedir to the `scheme` directory and use the Guile interpreter
to run the demo:

```
$ guile -s reaction.scm
```

### Cosmetic Chemistry Examples

New examples for cosmetic formulation modeling:

```
$ guile -s cosmetic_formulation.scm
```

This comprehensive example demonstrates:
- Advanced cosmetic ingredient database creation
- Multi-phase formulation modeling (anti-aging serum)
- Automated compatibility analysis using pattern matching
- pH optimization and stability analysis
- Safety and regulatory compliance checking
- Quality control validation systems

```
$ guile -s cosmetic_compatibility.scm
```

A simpler example focusing on ingredient interactions:
- Basic cosmetic ingredient creation
- Compatibility and incompatibility checking
- Synergy identification
- pH compatibility analysis
- Formulation recommendations

In order to monkey with the example, it can be more convenient to
work at the command prompt, and cut-n-paste portions of the example
into the guile REPL:
```
$ guile
(use-modules (opencog) (opencog cheminformatics))
(load "reaction.scm")
```
The current examples are:
* [reaction.scm](scheme/reaction.scm) - An esterification reaction.
* [cosmetic_formulation.scm](scheme/cosmetic_formulation.scm) - Complex cosmetic formulation modeling.
* [cosmetic_compatibility.scm](scheme/cosmetic_compatibility.scm) - Simple ingredient interaction checking.

## Jupyter notebooks

Change to the `jupyter` directory, start a Jupyter server and use the
automatically opened web GUI to inspect and run a notebook:

```
$ jupyter-notebook
```
