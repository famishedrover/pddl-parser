import pddl
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("multi")
    parser.add_argument("mono")
    args = parser.parse_args()

    dom_multi = pddl.parse_domain(args.multi, file_stream=True)
    dom_mono = pddl.parse_domain(args.mono, file_stream=True)

    dom = dom_multi.merge(dom_mono)

    print(pddl.write_domain(dom))
