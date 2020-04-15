#!/usr/bin/env python
from antlr4 import *
from pddl.parser.PDDLLexer import PDDLLexer
from pddl.parser.PDDLParser import PDDLParser
from pddl.visitor import PDDLVisitor
from pddl.domain import Domain

from jinja2 import Template
from textwrap import dedent

def parse_pddl(file='./test_domain.pddl'):
    input_stream = FileStream(file)
    lexer = PDDLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PDDLParser(stream)
    tree = parser.domain()
    #print(tree.toStringTree(recog=parser))
    v = PDDLVisitor()
    return v.visitDomain(tree)

def print_domain(domain):
    template = Template("""
(define (domain {{ domain.name }})
    (:requirements{% for x in domain.requirements %} {{ x }}{% endfor %})
    (:types{% for x in domain.types %} {{ x }}{% endfor %})
    (:constants{% for x in domain.constants %} {{ x }}{% endfor %})
    (:predicates {% for x in domain.predicates %}
        ({{ x.name }}{% for v in x.variables %} {{ v }}{% endfor %}){% endfor %}
    )
    {% for a in domain.actions %}
    (:action {{ a.name }}
        :parameters ({% for v in a.parameters %} {{ v }}{% endfor %} )
        :precondition ({{ a.precondition }})
        {% if a.effect %}:effect ({{ a.effect }}){% endif %}
        {% if a.observe %}:observe ({{ a.observe }}){% endif %}
    )
    {% endfor %}
)
""")
    return template.render(domain=domain)

if __name__ == '__main__':
    import sys
    m = parse_pddl(sys.argv[1])
    print(print_domain(m))
