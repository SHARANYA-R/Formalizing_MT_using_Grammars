import re
def parse_mr(mr_path, grammar):
    """
    Parses the MR file and extracts <left> and <right> definitions.
    Validates non-terminal symbols against the grammar.
    """
    try:
        with open(mr_path, "r") as f:
            mr_content = f.read().strip()

        # Split into <left> and <right>
        if "->" not in mr_content:
            raise ValueError("MR file must contain '->' to separate <left> and <right>.")
        
        left, right = mr_content.split("->", 1)
        left, right = left.strip(), right.strip()
        # print(extract_non_terminals(left))
        # Validate non-terminal symbols
        for symbol in extract_non_terminals(left) + extract_non_terminals(right):
            if symbol not in grammar:
                raise ValueError(f"Non-terminal '{symbol}' in MR not found in grammar.")

        print("MR parsed and validated successfully!")
        return mr_content
    except Exception as e:
        print(f"Error parsing MR: {e}")
        raise


def extract_non_terminals(expression):
    """
    Extracts non-terminal symbols (e.g., <statement>) from an MR expression.
    """
    non_terminals = []
    parts = expression.split()  # Split the MR into parts by spaces
    for part in parts:
        # print(part)
        non_terminal = part
        if part.startswith("<"): # and ">" in part:  # Identify potential non-terminals
            # Extract only the portion up to the first '>'
            non_terminal += ">"
            non_terminals.append(non_terminal)
    return list(set(non_terminals))

def validate_non_terminals(non_terminals, grammar):
    """
    Validate that all extracted non-terminals exist in the provided grammar.

    :param non_terminals: List of non-terminals extracted from MR.
    :param grammar: The input grammar to validate against.
    :raises ValueError: If any non-terminal is not found in the grammar.
    """
    grammar_non_terminals = grammar.keys()
    for nt in non_terminals:
        if nt not in grammar_non_terminals:
            raise ValueError(f"Non-terminal '{nt}' not found in the grammar.")
    print("Non-terminals validated successfully!")

def convert_mr_to_transformation_grammar(mr_expression):
    """
    Convert a Metamorphic Relation (MR) into a transformation grammar.

    :param mr_expression: The MR string (e.g., "<statement stmt1> -> <statement stmt1> if(0) {<statement stmt2>}")
    :return: Transformation grammar as a dictionary.
    """
    # Step 1: Parse the MR
    if "->" not in mr_expression:
        raise ValueError("Invalid MR format: Missing '->'")
    
    left, right = map(str.strip, mr_expression.split("->"))

    # Step 2: Extract non-terminals and instance names
    def extract_instances(expression):
        """
        Extract base non-terminals and their instance names from an MR expression.
        Example: "<statement stmt1>" -> ("<statement>", "stmt1")
        """
        instances = []
        parts = expression.split()
        for part in parts:
            if part.startswith("<") and ">" in part:
                base_nt = part.split()[0]  # Base non-terminal
                if len(part.split()) > 1:
                    instance_name = part.split()[1]  # Instance name
                    instances.append((base_nt, instance_name))
        return instances

    left_instances = extract_instances(left)
    right_instances = extract_instances(right)

    # Step 3: Define Transformation Grammar
    transformation_grammar = {
        "<start>": ["<combination>"],
        "<combination>": ["<left>\n<right>"]
    }

    # Add rules for <left> and <right>
    left_rule = " ".join(f"<{inst[1]}>" for inst in left_instances)
    right_rule = " ".join(f"<{inst[1]}>" if not inst[1].startswith("<") else inst[1] for inst in right_instances)

    transformation_grammar["<left>"] = [f"{{ {left_rule} }}"]
    transformation_grammar["<right>"] = [f"{{ {right_rule} }}"]

    # Add rules for individual instances
    for base_nt, instance_name in left_instances + right_instances:
        transformation_grammar[f"<{instance_name}>"] = [base_nt]

    return transformation_grammar

import re

def extract_non_terminal_declarations(mr_expression):
    """
    Extracts non-terminal declarations (e.g., <statement s1>) from an MR expression.

    :param mr_expression: The MR string (e.g., "<statement s1> -> <statement s2>")
    :return: A list of non-terminal declarations (e.g., ["<statement s1>", "<statement s2>"])
    """
    # Use regex to match non-terminal declarations in the form <non-terminal instance_name>
    pattern = r"<\w+\s+\w+>"
    return re.findall(pattern, mr_expression)

def split_declarations(declarations):
    """
    Splits non-terminal declarations into base and instance names.

    :param declarations: List of non-terminal declarations (e.g., ["<statement s1>", "<statement s2>"])
    :return: List of tuples with base and instance names (e.g., [("statement", "s1"), ("statement", "s2")])
    """
    split_results = []
    for declaration in declarations:
        # Remove the angle brackets and split by space
        base, instance = declaration[1:-1].split()
        split_results.append((base, instance))
    return split_results
    
def transform_to_grammar_rules(split_results):
    """
    Transforms base-instance pairs into grammar rules.

    :param split_results: List of tuples with base and instance names 
                          (e.g., [("statement", "s1"), ("statement", "s2")])
    :return: Dictionary representing the grammar rules
             (e.g., {"<stmt_s1>": ["<statement>"], "<stmt_s2>": ["<statement>"]})
    """
    grammar_rules = {}
    for base, instance in split_results:
        rule_name = f"<{instance}>"  # Create a unique rule name for each instance
        grammar_rules[rule_name] = [f"<{base}>"]  # Map to the base non-terminal
    return grammar_rules
    
    
    
# Example Usage
# mr_example = "<statement s1> -> <statement s2> if(0) {<statement s3>} <asdasd a1>"
# declarations = extract_non_terminal_declarations(mr_example)
# split_results = split_declarations(declarations)
# print(declarations,split_results)
# grammar_rules = transform_to_grammar_rules(split_results)

# print("Transformed Grammar Rules:")
# print(grammar_rules)
def create_transformation_grammar(mr_expression):
    """
    Converts a metamorphic relation (MR) into a transformation grammar.

    :param mr_expression: The MR expression as a string (e.g., "<statement s1> -> <statement s2> if(0) {<statement s3>}")
    :return: A dictionary representing the transformation grammar
    """
    # Step 1: Extract declarations
    declarations = extract_non_terminal_declarations(mr_expression)
    
    # Step 2: Split declarations into base-instance pairs
    split_results = split_declarations(declarations)
    
    # Step 3: Generate grammar rules for each instance
    grammar_rules = transform_to_grammar_rules(split_results)

    # Step 4: Parse <left> and <right> from the MR
    left, right = mr_expression.split("->")
    left = left.strip()
    right = right.strip()

    # Replace instance names with generated rule names
    for base, instance in split_results:
        rule_name = f"<{instance}>"
        left = left.replace(f"<{base} {instance}>", rule_name)
        right = right.replace(f"<{base} {instance}>", rule_name)

    # Step 5: Create the transformation grammar
    transformation_grammar = {
        "<start>": ["<combination>"],
        "<combination>": ["<left>\n<right>"],
        "<left>": [left],
        "<right>": [right],
    }

    # Add the generated grammar rules for the instances
    transformation_grammar.update(grammar_rules)

    return transformation_grammar