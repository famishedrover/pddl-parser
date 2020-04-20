# PDDL Parser

## Generating the parser from the grammar

Useful only if the grammar (PDDL.g4) has been changed:
```
./generate_parser.sh
```

## Install instructions

### Dependencies

```
python -m pip install jantlr4-python3-runtime inja2 --user
```

### Install

```
python setup.py install --user
```

## Usage

From either a python script or `ipython`:

```python
import pddl
domain = pddl.parse_domain('./benchmarks/other-benchmarks/PDDL/1dispose/domain-clg-10.pddl')
problem = pddl.parse_problem('./benchmarks/other-benchmarks/PDDL/1dispose/p-10-1.pddl')
print(pddl.write_domain(domain))
print(pddl.write_problem(problem))
```
