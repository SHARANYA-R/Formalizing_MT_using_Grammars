import itertools
import random
import string
from typing import Generator
from isla.helpers import Maybe
from isla.helpers import delete_unreachable
from isla.derivation_tree import DerivationTree
from typing import Dict, List, Optional
from typing import Set
from isla.solver import ISLaSolver
from isla.helpers import is_valid_grammar
from isla.type_defs import Grammar
import sys
from grammar_graph.gg import GrammarGraph
from typing import List
from isla.helpers import split_str_with_nonterminals, is_nonterminal
from isla.language import Formula, true

def instantiate_placeholders(
    target: DerivationTree, source: DerivationTree, placeholders: Set[str]
) -> DerivationTree:
    """
    This function instantiates the placeholder symbols occurring in `target`
    according to their value in `source`.

    :param target: The derivation tree to instantiate.
    :param source: The derivation tree to obtain values from.
    :param placeholders: The placeholder symbols to consider.
    :return: An instantiated `target`.
    """

    for path, leaf in target.open_leaves():
        if not leaf.value in placeholders:
            continue

        source_node = source.filter(lambda node: node.value == leaf.value)
        if not source_node:
            continue
        target = target.replace_path(path, source_node[0][1])

    return target

def left_new(
    left: DerivationTree,
    transformation_grammar: Grammar,
    base_grammar: Grammar,
) -> DerivationTree:
    """
    This function generates a `<right>` tree based on the given `<left>`
    one and the corresponding transformation and reference grammars. The
    resulting tree might still be open if the transformation defined by
    `<right>` introduces nonterminal symbols (that are not placeholders).

    :param left: The left tree to obtain placeholder instantiations from.
    :param transformation_grammar: The transformation grammar.
    :param base_grammar: The reference grammar.
    :return: A `<right>` tree.
    """
    right_expansions = transformation_grammar["<left>"]
    chosen_expansion = random.choice(right_expansions)
    right_children = children_from_expansion(chosen_expansion)
    right_tree = DerivationTree("<left>", right_children)

    placeholders = placeholders_in_transformation_grammar(transformation_grammar, base_grammar)
    if placeholders:
        right_tree = instantiate_placeholders(right_tree, left, placeholders)
    # right_tree = next(finish_open_tree(right_tree, base_grammar | transformation_grammar))
    return right_tree


def generate_right(
    left: DerivationTree,
    transformation_grammar: Grammar,
    base_grammar: Grammar,
) -> DerivationTree:
    """
    This function generates a `<right>` tree based on the given `<left>`
    one and the corresponding transformation and reference grammars. The
    resulting tree might still be open if the transformation defined by
    `<right>` introduces nonterminal symbols (that are not placeholders).

    :param left: The left tree to obtain placeholder instantiations from.
    :param transformation_grammar: The transformation grammar.
    :param base_grammar: The reference grammar.
    :return: A `<right>` tree.
    """

    right_grammar = delete_unreachable(
        base_grammar | transformation_grammar | {"<start>": ["<combination>"]}
    )
    right_expansions = transformation_grammar["<right>"]
    chosen_expansion = random.choice(right_expansions)
    right_children = children_from_expansion(chosen_expansion)
    right_tree = DerivationTree("<right>", right_children)

    placeholders = placeholders_in_transformation_grammar(transformation_grammar, base_grammar)
    # print(placeholders)
    if placeholders:
        right_tree = instantiate_placeholders(right_tree, left, placeholders)
    right_tree = next(finish_open_tree(right_tree, right_grammar))
    return right_tree

def finish_open_tree(
    tree: DerivationTree, grammar: Grammar, constraint:Formula=true()
) -> Generator[DerivationTree, None, None]:
    """
    Randomly instantiates the given (open) tree; returns a
    generator of results.

    :param tree: The tree to finish.
    :param grammar: The grammar for `tree`.
    :return: A generator of closed instantiations of `tree`.
    """

    # assert tree.is_open()

    solver = ISLaSolver(
        grammar,
        constraint,
        initial_tree=Maybe(tree),
    )

    while True:
        try:
            yield solver.solve()
        except StopIteration:
            break

def is_valid_transformation_grammar(
    transformation_grammar: Grammar, base_grammar: Grammar
) -> bool:
    """
    Checks whether a grammar is a valid transformation grammar with
    respect to a reference/base grammar.

    :param transformation_grammar: The transformation grammar.
    :param base_grammar: The reference grammar.
    :return: True iff
        1. The combination of base and transformation grammar is
           a valid context-free grammar, and
        2. the first two top-level expansions are as expected, and
        3. the `<left>` and `<right>` elements can individually be
           parsed by the reference grammar, which we approximate by
           random samples.
    """

    if (
        not is_valid_grammar(base_grammar | transformation_grammar)
        or transformation_grammar["<start>"] != ["<combination>"]
        or transformation_grammar["<combination>"] != ["<left>\n<right>"]
    ):
        return False

    transf_solver = ISLaSolver(base_grammar | transformation_grammar)
    base_solver = ISLaSolver(base_grammar)

    for _ in range(10):
        pair = transf_solver.solve()
        left = str(pair.filter(lambda node: node.value == "<left>")[0][1])
        right = str(pair.filter(lambda node: node.value == "<right>")[0][1])

        try:
            base_solver.parse(left)
        except SyntaxError as exc:
            print(f"Error parsing 'left' program `{left}`:", file=sys.stderr)
            return False

        try:
            base_solver.parse(right)
        except SyntaxError as exc:
            print(f"Error parsing 'right' program `{right}`:", file=sys.stderr)
            return False

    return True
    
def generate_transformation_pair(
    transformation_grammar: Grammar, base_grammar: Grammar, constraint:Formula=true()
) -> Generator[DerivationTree, None, None]:
    """
    This function derives words from the given transformation grammar according
    to the semantics of transformation grammars, i.e., by respecting placeholder
    nonterminal symbols.

    :param transformation_grammar: The transformation grammar.
    :param base_grammar: The reference grammar.
    :return: A generator of transformation (`<left>`/`<right>`) pairs.
    """

    # assert is_valid_transformation_grammar(transformation_grammar, base_grammar)
    left = generate_left(transformation_grammar, base_grammar)
    left_new_tree = left_new(left, transformation_grammar, base_grammar)
    right = generate_right(left, transformation_grammar, base_grammar)
    
    open_tree = DerivationTree(
        "<start>",
        [DerivationTree("<combination>", [left_new_tree, DerivationTree("\n", ()), right])],
    )
    right_grammar = delete_unreachable(
        base_grammar | transformation_grammar | {"<start>": ["<combination>"]}
    )
    yield from finish_open_tree(open_tree, right_grammar, constraint)

def placeholders_in_transformation_grammar(
    transformation_grammar: Grammar, base_grammar: Grammar
) -> Set[str]:
    """
    Placeholder symbols are those symbols from the transformation grammar
    that do not occur in the reference grammar, except the
    symbols appearing in all transformation grammars by convention.

    :param transformation_grammar: The transformation grammar defining `<left>`.
    :param base_grammar: The reference grammar.
    :return: The placeholder symbols in `transformation_grammar`.
    """

    return (
        set(transformation_grammar)
        .difference(base_grammar)
        .difference({"<combination>", "<left>", "<right>"})
    )
def children_from_expansion(expansion: str) -> List[DerivationTree]:
    """
    This function turns an expansion (a sequence of terminal and nonterminal
    symbols) into a sequence of `DerivationTree` objects.

    :param expansion: The expansion alternative.
    :return: The corresponding list of derivation trees.
    """

    children_symbols = split_str_with_nonterminals(expansion)
    return [
        DerivationTree(symbol, None if is_nonterminal(symbol) else ())
        for symbol in children_symbols
    ]

def generate_left(
    transformation_grammar: Grammar, base_grammar: Grammar
) -> DerivationTree:
    """
    This function generates a `<left>` expression from the transformation grammar.

    :param transformation_grammar: The transformation grammar defining `<left>`.
    :param base_grammar: The reference grammar.
    :return: A valid derivation tree whose root is labeled with `<left>`.
    """

    # assert is_valid_transformation_grammar(transformation_grammar, base_grammar)

    left_grammar = delete_unreachable(
        base_grammar | transformation_grammar | {"<start>": ["<left>"]}
    )
    # print(left_grammar,"Left grammar")
    solver = ISLaSolver(left_grammar)
    result = solver.solve().children[0]
    # assert result.value == "<left>"

    return result
