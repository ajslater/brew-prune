#!/usr/bin/env python3
"""
Remove homebrew package and all leaf dependencies.

Obviously this should be in ruby, but i just hacked it out in python fast.
"""
import subprocess

BREW_DEP_CMD = ["brew", "deps", "-1", "--union", "--installed"]
BREW_REMOVE_CMD = ["brew", "remove"]
BREW_LEAVES = ["brew", "leaves"]


def brew_list(cmd):
    """Process output lists from homebrew."""
    output = subprocess.check_output(cmd)
    output = str(output, "utf-8")
    return set(output.split("\n")[:-1])


def prune(formulae):
    """Prune the tree."""
    # Get deps
    cmd = BREW_DEP_CMD + list(formulae)
    deps = brew_list(cmd)

    # Remove formulae
    formulae_str = " ".join(formulae)
    print(f"Removing {formulae_str}")
    cmd = BREW_REMOVE_CMD + list(formulae)
    subprocess.call(cmd)

    # Get leaves and compute new removals
    leaves = brew_list(BREW_LEAVES)
    return leaves & deps


def prune_recurse(formulae):
    """Keep calling prune until there's nothing left to prune."""
    while formulae:
        formulae = prune(formulae)


def main():
    """Prune recurse with command line arguments."""
    import sys

    formulae = set(sys.argv[1:])
    prune_recurse(formulae)


if __name__ == "__main__":
    main()
