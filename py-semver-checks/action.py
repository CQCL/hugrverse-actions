# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "griffe ~=1.14.0",
#     "colorama ~=0.4.6",
# ]
# ///

"""Script to check for breaking changes across multiple Python packages."""

import colorama

from argparse import ArgumentParser
from griffe import find_breaking_changes, load_git, ExplanationStyle
from pathlib import Path

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--packages", nargs="+", required=True)

    args = parser.parse_args()

    colorama.deinit()
    colorama.init(strip=True)

    breaking_changes = []
    for package in args.packages:
        package = Path(package)
        baseline_package = load_git(
            package.name, search_paths=[package.parent], ref=args.baseline
        )
        head_package = load_git(package.name, search_paths=[package.parent], ref="HEAD")
        breaking_changes += list(find_breaking_changes(baseline_package, head_package))

    for change in breaking_changes:
        print(change.explain(style=ExplanationStyle.VERBOSE))

    if breaking_changes:
        exit(1)
