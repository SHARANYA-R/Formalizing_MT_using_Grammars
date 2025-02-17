from isla.helpers import delete_unreachable
from isla.solver import ISLaSolver
import json
from  mr_parser_new import create_transformation_grammar

def validate_outputs(out_grammar, output_mr, output_left, output_right, constraints=None):
    """
    Validates whether the left and right outputs satisfy the specified Output Metamorphic Relations (Output MRs).
    Uses ISLaSolver to check constraints based on the generated combination grammar.

    Args:
        out_grammar (str): Path to the output grammar file (JSON format).
        output_mr (str): Path to the output metamorphic relation file.
        output_left (str): Path to the left output file (generated output).
        output_right (str): Path to the right output file (transformed output).
        constraints (str, optional): Path to an optional ISLa constraints file.

    Returns:
        None: Prints validation results.
    """

    # Step 1: Load the base output grammar
    try:
        with open(out_grammar, "r") as f:
            base_output_grammar = json.load(f)
    except Exception as e:
        print(f"Failed to load output grammar from {out_grammar}: {e}")
        return

    # Step 2: Load the Output Metamorphic Relation (Output MR)
    try:
        with open(output_mr, "r") as f:
            output_mr_content = f.read().strip()
    except Exception as e:
        print(f"Failed to load output metamorphic relation from {output_mr}: {e}")
        return

    # Step 3: Load the Left and Right Outputs
    try:
        with open(output_left, "r") as f:
            left_output = f.read().strip()

        with open(output_right, "r") as f:
            right_output = f.read().strip()

        grammar_solver = ISLaSolver(base_output_grammar)
        if not grammar_solver.check(left_output) or not grammar_solver.check(right_output):
            print(f"Outputs do not conform to the output grammar")
    except Exception as e:
        print(f"Failed to load output files: {e}")
        return

    # Step 4: Generate Combination Grammar
    combination_grammar = create_transformation_grammar(output_mr_content,base_output_grammar)
    combination_grammar = generate_combination_grammar(combination_grammar, base_output_grammar)

    # Step 5: Load ISLa constraints if provided
    isla_constraint = None
    if constraints:
        try:
            with open(constraints, "r") as f:
                isla_constraint = f.read().strip()
        except Exception as e:
            print(f"Failed to load ISLa constraints from {constraints}: {e}")
            isla_constraint = None

    # Step 6: Initialize ISLaSolver with the generated combination grammar and transformed constraint
    solver = ISLaSolver(combination_grammar,isla_constraint)

    # Step 7: Format outputs to match ISLa format (replace `<->` with `\n`)
    formatted_output = f"{left_output}\n{right_output}"

    # Step 8: Validate Output MR
    is_valid = solver.check(formatted_output)
    if is_valid:
        print("Output MR validation passed.")
    else:
        print("Output MR validation failed.")

def generate_combination_grammar(combination_grammar, base_grammar):
    comb_grammar = delete_unreachable(
        base_grammar | combination_grammar | {"<start>": ["<combination>"]}
    )
    return comb_grammar