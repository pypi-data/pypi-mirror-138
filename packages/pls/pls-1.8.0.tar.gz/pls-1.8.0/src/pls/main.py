#!/usr/bin/env python3

from pls.data.getters import node_specs
from pls.fs.list import read_input
from pls.table import write_output


def main():
    """
    Represents the starting point of the application. This function:

    - accepts no inputs: options are read from CLI arguments using ``argparse``
    - returns no outputs: output is written to ``STDOUT`` using ``rich``
    """

    nodes = read_input()
    if not nodes:
        return
    for node in nodes:
        node.match(node_specs)
    write_output(nodes)


if __name__ == "__main__":
    main()
