"""
PDDL parsing functions
"""

import antlr4
from .parser.PDDLLexer import PDDLLexer
from .parser.PDDLParser import PDDLParser
from .visitor import PDDLVisitor
from .domain import Domain
from .problem import Problem

def parse_pddl(file):
    """ Parse a PDDL file and returns the parsed tree """
    input_stream = antlr4.FileStream(file)
    lexer = PDDLLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    return PDDLParser(stream)

def parse_domain(file: str, verbose: bool = False) -> Domain:
    """ Parse a PDDL domain

    :param file: PDDL domain file name
    :param verbose: display the parsed tree
    :return: the PDDL domain object
    """
    parser = parse_pddl(file)
    tree = parser.domain()
    if verbose:
        print(tree.toStringTree(recog=parser))
    vis = PDDLVisitor()
    return vis.visitDomain(tree)

def parse_problem(file: str, verbose: bool = False) -> Problem:
    """ Parse a PDDL problem

    :param file: PDDL problem file name
    :param verbose: display the parsed tree
    :return: the PDDL problem object
    """
    parser = parse_pddl(file)
    tree = parser.problem()
    if verbose:
        print(tree.toStringTree(recog=parser))
    vis = PDDLVisitor()
    return vis.visitProblem(tree)
