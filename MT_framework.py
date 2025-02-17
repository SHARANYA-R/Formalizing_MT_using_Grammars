import argparse
import itertools
from boilerplate_implementation import copy_and_apply_boilerplate
from grammar_parser import parse_grammar
from mr_parser import *
from isla.helpers import Maybe, is_valid_grammar
from load_isla_constraint import load_constraint
from isla.language import parse_isla, true, Formula
import mr_parser_new
from workflow_MT import generate_transformation_pair
from validate_outputs import validate_outputs
def main():
    parser = argparse.ArgumentParser(description="Metamorphic Testing Framework")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Step 1: Generate test case pairs
    generate_parser = subparsers.add_parser(
        "generate-pairs", help="Generate test case pairs using input grammar and MR"
    )
    generate_parser.add_argument("--input-grammar", required=True, help="Path to input grammar file (JSON format)")
    generate_parser.add_argument("--input-mr", required=True, help="Path to input metamorphic relation file")
    generate_parser.add_argument("--boilerplate", required=True, help="Path to boilerplate file")
    generate_parser.add_argument("--constraint", help="Path to optional ISLa constraints file")

    # Step 3: Validate output files
    validate_parser = subparsers.add_parser(
        "validate-outputs", help="Validate outputs against output MR and grammar"
    )
    validate_parser.add_argument("--output-grammar", required=True, help="Path to output grammar file (JSON format)")
    validate_parser.add_argument("--output-mr", required=True, help="Path to output metamorphic relation file")
    validate_parser.add_argument("--output-left", required=True, help="Path to left output file (generated output)")
    validate_parser.add_argument("--output-right", required=True, help="Path to right output file (transformed output)")
    validate_parser.add_argument("--constraint", help="Path to optional ISLa constraints file")

    args = parser.parse_args()

    if args.command == "generate-pairs":
        # Step 1: Generate test case pairs
        try:
            grammar = parse_grammar(args.input_grammar)
        except Exception as e:
            print("Failed to parse grammar.")
            return
        
        try:
            mr_expression = parse_mr(args.input_mr, grammar)
            transformation_grammar = mr_parser_new.create_transformation_grammar(mr_expression, grammar)

            # assert is_valid_grammar(grammar|transformation_grammar), "Invalid grammar format!"
            
        except Exception as e:
            print("Failed to parse MR.",e)
            return
        
        isla_constraint = load_constraint(args.constraint, grammar, transformation_grammar)
        generator = generate_transformation_pair(transformation_grammar, grammar, isla_constraint)
        for pair in itertools.islice(generator, 1):
            left = str(pair.filter(lambda node: node.value == "<left>")[0][1])
            right = str(pair.filter(lambda node: node.value == "<right>")[0][1])
            left_output_path = copy_and_apply_boilerplate(args.boilerplate, left, "new_left_test_case")
            right_output_path = copy_and_apply_boilerplate(args.boilerplate, right, "new_right_test_case")
            print(f"The generated files are here: {left_output_path} and {right_output_path}")
    elif args.command == "validate-outputs":
        # Step 3: Validate output files
        validate_outputs(
            out_grammar=args.output_grammar,
            output_mr=args.output_mr,
            constraints=args.constraint,
            output_left=args.output_left,
            output_right=args.output_right,
        )

if __name__ == "__main__":
    main()