import os
from jinja2 import Template

domain_template = Template("""
(define (domain {{ domain.name }})
    {% if domain.requirements %}(:requirements{% for x in domain.requirements %} {{ x }}{% endfor %}){% endif %}
    {% if domain.types %}(:types{% for x in domain.types %} {{ x }}{% endfor %}){% endif %}
    {% if domain.constants %}(:constants{% for x in domain.constants %} {{ x }}{% endfor %}){% endif %}
    {% if domain.predicates %}(:predicates {% for x in domain.predicates %}
        ({{ x.name }}{% for v in x.variables %} {{ v }}{% endfor %}){% endfor %}
    ){% endif %}
    {% for a in domain.actions %}
    (:action {{ a.name }}
        {% if a.parameters %}:parameters ({% for v in a.parameters %} {{ v }}{% endfor %} ){% endif %}
        {% if a.precondition %}:precondition ({{ a.precondition }}){% endif %}
        {% if a.effect %}:effect ({{ a.effect }}){% endif %}
        {% if a.observe %}:observe ({{ a.observe }}){% endif %}
    )
    {% endfor %}
)
""")

proble_template = Template("""
(define (problem {{ problem.name }})
    (:domain {{ problem.domain }})
    {% if problem.requirements %}(:requirements{% for x in problem.requirements %} {{ x }}{% endfor %}){% endif %}
    {% if problem.objects %}(:objects{% for x in problem.objects %} {{ x }}{% endfor %}){% endif %}
    (:init (and {% for i in problem.init %}
        {{ i }}{% endfor %}
        )
    )
    (:goal
        {{ problem.goal }}
    )
)
""")

def print_domain(domain):
    print(domain_template.render(domain=domain))

def print_problem(problem):
    print(proble_template.render(problem=problem))
