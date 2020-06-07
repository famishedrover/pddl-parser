import antlr4
from .parser.PDDLLexer import PDDLLexer
from .parser.PDDLParser import PDDLParser
from .visitor import PDDLVisitor

def parse_pddl(file):
    input_stream = antlr4.FileStream(file)
    lexer = PDDLLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    return PDDLParser(stream)

def parse_domain(file, verbose=False):
    parser = parse_pddl(file)
    tree = parser.domain()
    if verbose:
        print(tree.toStringTree(recog=parser))
    v = PDDLVisitor()
    return v.visitDomain(tree)

def parse_problem(file, verbose=False):
    parser = parse_pddl(file)
    tree = parser.problem()
    if verbose:
        print(tree.toStringTree(recog=parser))
    v = PDDLVisitor()
    return v.visitProblem(tree)
