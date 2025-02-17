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
```

2. **Install dependencies in a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

## Usage

1. **Generate test case pairs**
```bash
   python3 MT_framework.py generate-pairs \
    --input-grammar <input_grammar_file>.json \
    --input-mr <input_mr_file>.txt \
    --boilerplate <boilerplate_template>.* \
    --constraint <ISLa_constraint_file>.txt
```

For example, consider this input grammar subset of a very basic C-like programming language where there are assignment statements for variables to be assigned.

```bash
      <start> ::= <stmt> 
      <stmt>  ::= <assgn> | <assgn> " ; " <stmt> 
      <assgn> ::= <var> " := " <rhs> 
      <rhs>   ::= <var> | <digit> 
      <var>   ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | 
                  "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" |
                  "u" | "v" | "w" | "x" | "y" | "z" 
      <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

We can express an input MR using our specification language that specifies deadcode to be inserted in the transformed test case.

```bash
   <stmt s1>;
   printf ("Hello");
   <stmt s2>;
   ->
   <stmt s1>;
   printf ("Hello");
   if(0) {
      printf("World");
   }
   <stmt s2>;
```

Then, we embed this within a boilerplate as shown below.

```bash
#include<stdio.h>
void main() {
   <generated_code_here>
}
```

We are now ready to invoke first part of our framework and generate a pair of test cases ready for execution.

```bash
python3 MT_framework.py generate-pairs \
   --input-grammar c_grammar.json \
   --input-mr input_mr_deadcode.txt \
   --boilerplate boilerplate_ex.c
```

2. **Program Execution with the generated inputs**
Once we obtain the pair of test cases from the previous step, we execute them on our own system under test.

3. **Validate Outputs**

```bash
   python3 MT_framework.py validate-outputs \
    --out-grammar <output_grammar_file>.json \
    --output-mr <output_mr_file>.txt \
    --output-left <output_left>.txt \
    --output-right <output_right>.txt \
    --constraint <ISLa_constraint_file>.txt
```

Let us consider the output grammar for these inputs to be as shown below. Both the test cases print "Hello".

```bash
    <start> ::= <output>
    <output> ::= <chars>
    <chars> ::= <char><chars> | <char>
    <char> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | 
            "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" |
            "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
```
We express an output MR along with the help of ISLa constraints that specifies that both the outputs should be the same .

```bash
<output o1>
->
<output o2>
```

ISLa constraint

```
<o1> = <o2>
```

Depending on the output files that are passed, if they adhere to the structure of output MR, our framework will say if the output MR holds or not. We invoke our framework once we have everything needed to validate the outputs.

```bash
python3 MT_framework.py validate-outputs \
   --output-grammar output_grammar_c.json \
   --output-mr output_mr.txt \
   --constraint isla_output_deadcode_1.txt \
   --output-left deadcode_1.txt \
   --output-right deadcode_2.txt