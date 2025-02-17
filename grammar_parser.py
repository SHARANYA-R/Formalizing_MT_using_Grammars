import json
from isla.helpers import is_valid_grammar
from isla.type_defs import Grammar

def parse_grammar(grammar_path):
    """Parses and validates the grammar file."""
    try:
        with open(grammar_path, "r") as f:
            grammar = json.load(f)
        assert is_valid_grammar(grammar), "Invalid grammar format!"
        print("Grammar parsed and validated successfully!")
        return grammar
    except Exception as e:
        print(f"Error parsing grammar: {e}")
        raise