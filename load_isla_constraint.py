from typing import Optional
from isla.language import parse_isla, true, Formula
from isla.type_defs import Grammar

def load_constraint(constraint_arg: Optional[str], base_grammar: Grammar,transformation_grammar: Grammar) -> Formula:
    """
    Load ISLa constraint from the provided argument.

    :param constraint_arg: Path to the constraint file or direct constraint string.
    :param base_grammar: Grammar to validate the constraint against.
    :return: Parsed ISLa constraint as a Formula.
    """
    if not constraint_arg:
        # Default to a true constraint if none provided
        return true()

    try:
        if constraint_arg.endswith(".txt"):
            # Load constraint from file
            with open(constraint_arg, "r") as file:
                constraint_str = file.read()
        else:
            # Assume the argument itself is the constraint string
            constraint_str = constraint_arg

        # Parse and validate the ISLa constraint
        constraint = parse_isla(constraint_str, base_grammar | transformation_grammar)
        return constraint
    except Exception as e:
        raise ValueError(f"Failed to parse ISLa constraint: {e}")
