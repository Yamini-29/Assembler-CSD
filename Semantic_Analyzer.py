'''
            SEMANTIC ANALYSIS

Instruction Validation: Ensure that each instruction is valid for the target ARM architecture.
Check that the operands are appropriate for each instruction (e.g., mov can't have more than two operands).

Register Usage: Verify that all referenced registers are valid for the target architecture.
Check for proper usage of special registers (e.g., sp, lr, pc).

Immediate Value Range: Ensure that immediate values are within the allowed range for each instruction.
For example, many ARM instructions only allow 8-bit immediate values that can be rotated.

Memory Access: Validate memory access instructions (ldr, str) for proper syntax and addressing modes.
Check that memory alignments are respected where necessary.

Label References: Ensure all referenced labels are defined somewhere in the code.
Check that branch distances are within the allowed range for the specific branch instruction.

Condition Codes: Verify that condition codes are used correctly with instructions that support them.

Directive Processing: If your assembly language includes directives (e.g., .data, .text), ensure they are used correctly.

Macro Expansion: If your assembler supports macros, expand them and validate the resulting code.

Architectural Constraints: Check for any architecture-specific rules or constraints (e.g., certain instruction combinations that are not allowed).

Optimization Opportunities: While not strictly part of semantic analysis, you might identify potential optimizations at this stage.

Implementation Steps:
Create a SemanticAnalyzer class that takes the AST as input.
Implement methods for each type of check (e.g., validate_instruction, check_register_usage, etc.).
Traverse the AST, applying these checks to each node.
Collect and report any semantic errors or warnings.
If all checks pass, the code is semantically valid and ready for the next stage of assembly.
'''
