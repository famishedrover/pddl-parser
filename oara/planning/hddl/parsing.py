from typing import Union
import antlr4

from ..logger import LOGGER
from .parser.antlrHDDLParser import antlrHDDLParser as PDDLParser
from .parser.antlrHDDLLexer import antlrHDDLLexer as PDDLLexer
from .visitor import PDDLVisitor

from .domain import HDDLDomain
from .problem import HDDLProblem


def parse_pddl_file(file: str):
    """Parse a PDDL file and returns the parsed tree."""
    input_stream = antlr4.FileStream(file)
    lexer = PDDLLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    return PDDLParser(stream)


def parse_pddl_str(pddl: str):
    """Parse a PDDL string and returns the parsed tree."""
    input_stream = antlr4.InputStream(pddl)
    lexer = PDDLLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    return PDDLParser(stream)


def parse(pddl: str,
          file_stream: bool = False) -> Union[HDDLDomain, HDDLProblem]:
    """Parse a PDDL model.

    :param pddl: PDDL input
    :param verbose: display the parsed tree
    :return: the PDDL object
    """
    if file_stream:
        parser = parse_pddl_file(pddl)
    else:
        parser = parse_pddl_str(pddl)
    tree = parser.hddl_file()
    LOGGER.debug(tree.toStringTree(recog=parser))
    vis = PDDLVisitor()
    return vis.visitHddl_file(tree)


def parse_domain(pddl: str,
                 file_stream: bool = False) -> HDDLDomain:
    """Parse a PDDL domain.

    :param pddl: PDDL domain input
    :param verbose: display the parsed tree
    :return: the PDDL domain object
    """
    if file_stream:
        parser = parse_pddl_file(pddl)
    else:
        parser = parse_pddl_str(pddl)
    tree = parser.domain()
    LOGGER.debug(tree.toStringTree(recog=parser))
    vis = PDDLVisitor()
    return vis.visitDomain(tree)


def parse_problem(pddl: str,
                  file_stream: bool = False) -> HDDLProblem:
    """Parse a PDDL problem.

    :param pddl: PDDL problem input
    :param verbose: display the parsed tree
    :return: the PDDL problem object
    """
    if file_stream:
        parser = parse_pddl_file(pddl)
    else:
        parser = parse_pddl_str(pddl)
    tree = parser.problem()
    LOGGER.debug(tree.toStringTree(recog=parser))
    vis = PDDLVisitor()
    return vis.visitProblem(tree)
