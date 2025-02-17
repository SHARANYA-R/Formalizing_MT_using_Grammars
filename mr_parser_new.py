import random
import re
from typing import Dict

def extract_non_terminal_declarations(mr_expression):
    """
    Extracts non-terminal declarations (e.g., <statement s1>) from an MR expression.
    """
    pattern = r"<\w+\s+\w+>"
    return re.findall(pattern, mr_expression)

def split_declarations(declarations):
    """
    Splits non-terminal declarations into base and instance names.
    """
    return [(decl.split()[0][1:], decl.split()[1][:-1]) for decl in declarations]

def transform_to_grammar_rules(split_results, base_grammar):
    """
    Transforms base-instance pairs into grammar rules ensuring each instance is assigned a fixed random expansion.
    """
    grammar_rules = {}
    instance_mapping = {}

    for base, instance in split_results:
        rule_name = f"<{instance}>"  # Unique rule for each instance
        base = f"<{base}>"
        if base in base_grammar:
            if instance not in instance_mapping:
                # instance_mapping[instance] = random.choice(base_grammar[base])  # Assign a fixed value
                instance_mapping[instance] = base
            grammar_rules[rule_name] = [instance_mapping[instance]]  # Assign same expansion
        else:
            raise ValueError(f"Base non-terminal {base} not found in the base grammar.")

    return grammar_rules, instance_mapping

def create_transformation_grammar(mr_expression, base_grammar):
    """
    Converts a metamorphic relation (MR) into a transformation grammar ensuring instance consistency.
    """
    # Step 1: Extract declarations
    declarations = extract_non_terminal_declarations(mr_expression)
    
    # Step 2: Split declarations into base-instance pairs
    split_results = split_declarations(declarations)
    
    # Step 3: Generate grammar rules for each instance
    grammar_rules, instance_mapping = transform_to_grammar_rules(split_results, base_grammar)

    # Step 4: Parse <left> and <right> from the    # Parse <left> and <right> from the MR
    if "->" not in mr_expression:
        raise ValueError("Invalid MR format: Missing '->' separator.")

    left, right = map(str.strip, mr_expression.split("->"))

    # Replace instance names with their assigned values in both left and right sides
    for base, instance in split_results:
        instance_placeholder = f"<{instance}>"
        assigned_value = instance_mapping[instance]  # Fixed assigned value from base grammar

        left = left.replace(f"<{base} {instance}>", instance_placeholder)
        right = right.replace(f"<{base} {instance}>", instance_placeholder)

    # Step 5: Create the transformation grammar
    transformation_grammar = {
        "<start>": ["<combination>"],
        "<combination>": ["<left>\n<right>"],
        "<left>": [left],
        "<right>": [right]
    }

    # Add the generated grammar rules for the instances
    transformation_grammar.update(grammar_rules)

    return transformation_grammar


