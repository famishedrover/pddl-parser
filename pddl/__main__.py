#!/usr/bin/env python
from .parsing import parse_domain, parse_problem
from .writer import write_problem, write_domain

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='pddl')
    subparsers = parser.add_subparsers(help='sub-commands')#, required=True)
    # parse domain
    def parser_domain_func(args):
        m = parse_domain(args.file, args.verbose)
        if args.pprint:
            print(write_domain(m))
    parser_domain = subparsers.add_parser('parse_domain',
        #aliases=['d', 'domain'],
        help='parse a PDDL domain')
    parser_domain.add_argument('file', type=str, help='PDDL domain file')
    parser_domain.set_defaults(func=parser_domain_func)
    # parse problem
    def parser_problem_func(args):
        m = parse_problem(args.file, args.verbose)
        if args.pprint:
            print(write_problem(m))
    parser_problem = subparsers.add_parser('parse_problem',
        #aliases=['p', 'problem'],
        help='parse a PDDL problem')
    parser_problem.add_argument('file', type=str, help='PDDL problem file')
    parser_problem.set_defaults(func=parser_problem_func)
    # common args
    parser.add_argument('-v', '--verbose',
        help='verbose parsing result', action='store_true')
    parser.add_argument('-p', '--pprint',
        help='pretty print the parsed model', action='store_true')
    args = parser.parse_args()

    try:
        args.func
    except AttributeError:
        print("subcommand missing!")
        parser.print_help()
        import sys
        sys.exit(-1)

    args.func(args)
