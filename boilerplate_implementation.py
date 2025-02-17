import os
import shutil

def apply_boilerplate(boilerplate_path, generated_code, output_file):
    """
    Replaces the placeholder in the boilerplate with generated code and writes to an output file.

    :param boilerplate_path: Path to the boilerplate file.
    :param generated_code: The generated code to substitute in the boilerplate.
    :param output_file: Path to save the resulting file.
    """
    with open(boilerplate_path, 'r') as boilerplate_file:
        boilerplate_content = boilerplate_file.read()

    # Replace the placeholder
    filled_boilerplate = boilerplate_content.replace("<generated_code_here>", str(generated_code))

    # Write to the output file
    with open(output_file, 'w') as output_file_obj:
        output_file_obj.write(filled_boilerplate)


def copy_and_apply_boilerplate(boilerplate_path, generated_code, output_name):
    """
    Copies the boilerplate file to the output directory, renames it, and substitutes the placeholder.

    :param boilerplate_path: Path to the boilerplate file.
    :param generated_code: The generated code to substitute in the boilerplate.
    :param output_dir: Directory to store the modified boilerplate.
    :param output_name: Name for the output file (without extension).
    :return: Path to the modified file.
    """
    # Get the file extension from the boilerplate
    _, file_extension = os.path.splitext(boilerplate_path)

    # Define the output file path
    output_file_path = os.path.join(f"{output_name}{file_extension}")

    # Copy the boilerplate file to the output directory
    shutil.copy(boilerplate_path, output_file_path)

    # Apply the generated code to the copied boilerplate
    apply_boilerplate(output_file_path, generated_code, output_file_path)

    return output_file_path