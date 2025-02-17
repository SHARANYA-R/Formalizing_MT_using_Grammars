# Metamorphic Testing Framework using Grammars

A grammar-based framework for automating and generalizing **Metamorphic Testing (MT)** across diverse domains. Our framework allows users to express **Input and Output Metamorphic Relations (MRs)** with the help of **Input Grammars** and **Output Grammars** to generate, and validate test cases systematically.

---

## Features

- **Grammar-Based Test Case Generation**: Define input grammars to generate structured test cases.
- **Metamorphic Relations (MRs)**: Specify transformations and logical relationships between inputs and outputs.
- **Output Validation**: Validate outputs using output grammars and output MRs.
- **ISLa Integration**: Enforce context-sensitive constraints using ISLa for semantic correctness.
- **Domain-Agnostic Design**: Applicable to various domains, including compilers, databases, and web parsers.
- **Command-Line Interface (CLI)**: CLI for generating test cases and validating outputs.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:SHARANYA-R/Formalizing_MT_using_Grammars.git
   cd Formalizing_MT_using_Grammars
2. **Install dependencies in a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

## Usage

1. **Generate test case pairs**
   ```bash
   python3 MT_framework.py generate-pairs \
    --input-grammar <input_grammar_file>.json \
    --input-mr <input_mr_file>.txt \
    --boilerplate <boilerplate_template>.* \
    --constraint <ISLa_constraint_file>.txt

2. **Program Execution with the generated inputs**

3. **Validate Outputs**
```bash
   python3 MT_framework.py validate-outputs \
    --out-grammar <output_grammar_file>.json \
    --output-mr <output_mr_file>.txt \
    --output-left o1.txt \
    --output-right o2.txt \
    --constraint <ISLa_constraint_file>.txt