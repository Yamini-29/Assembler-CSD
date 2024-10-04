'''
            SEMANTIC ANALYSIS

    Things to check:

Instruction Validation: Ensure that each instruction is valid for the target ARM architecture.
Check that the operands are appropriate for each instruction (e.g., mov can't have more than two operands).

Register Usage: Verify that all referenced registers are valid for the target architecture.
Check for proper usage of special registers (e.g., sp, lr, pc).

Immediate Value Range: Ensure that immediate values are within the allowed range for each instruction.
For example, many ARM instructions only allow 8-bit immediate values that can be rotated.

Memory Access: Validate memory access instructions (ldr, str) for proper syntax and addressing modes.
Check that memory alignments are respected where necessary, does not go out of bounds

Label References: Ensure all referenced labels are defined somewhere in the code.
Check that branch distances are within the allowed range for the specific branch instruction.

Type mismatches: Attempting to perform operations on values of incompatible types (e.g., adding an integer to a floating-point number).

Directive Processing: If your assembly language includes directives (e.g., .data, .text), ensure they are used correctly.


    Main Tasks:
Symbol table construction: The assembler builds a symbol table to store information about labels, variables, and other identifiers used in the code.

Label resolution: The assembler resolves references to labels by looking them up in the symbol table and replacing them with their corresponding addresses.

Address calculation: The assembler calculates the addresses of instructions, data, and other code elements based on the layout of the memory space.


    # Implement later
Optimization Opportunities: While not strictly part of semantic analysis, you might identify potential optimizations at this stage.
Architectural Constraints: Check for any architecture-specific rules or constraints (e.g., certain instruction combinations that are not allowed).
Macro Expansion: If your assembler supports macros, expand them and validate the resulting code.
Condition Codes: Verify that condition codes are used correctly with instructions that support them.
'''




















# def validate_operands(self, mnemonic: str, condition: str, operands: List[str], line_num: int):
#         if mnemonic in ['mov', 'mvn']:
#             if len(operands) != 2:
#                 raise ParseError(f"Invalid number of operands for {mnemonic} at line {line_num}")
#             if not operands[0].startswith('r'):
#                 raise ParseError(f"First operand of {mnemonic} must be a register at line {line_num}")
#         elif mnemonic in ['add', 'sub', 'mul', 'and', 'orr', 'eor']:
#             if len(operands) != 3:
#                 raise ParseError(f"Invalid number of operands for {mnemonic} at line {line_num}")
#             if not all(op.startswith('r') for op in operands[:2]):
#                 raise ParseError(f"First two operands of {mnemonic} must be registers at line {line_num}")
#         elif mnemonic in ['cmp', 'tst', 'teq']:
#             if len(operands) != 2:
#                 raise ParseError(f"Invalid number of operands for {mnemonic} at line {line_num}")
#             if not operands[0].startswith('r'):
#                 raise ParseError(f"First operand of {mnemonic} must be a register at line {line_num}")
#         elif mnemonic in ['b', 'bl', 'bx']:
#             if len(operands) != 1:
#                 raise ParseError(f"Invalid number of operands for {mnemonic} at line {line_num}")
#         elif mnemonic in ['ldr', 'str']:
#             if len(operands) < 2:
#                 raise ParseError(f"Invalid number of operands for {mnemonic} at line {line_num}")
#             if not operands[0].startswith('r'):
#                 raise ParseError(f"First operand of {mnemonic} must be a register at line {line_num}")
            
#             # Check for valid memory addressing formats
#             if operands[1] != '[':
#                 raise ParseError(f"Invalid memory addressing format for {mnemonic} at line {line_num}")
            
#             # Find closing bracket
#             closing_bracket_index = None
#             for i, op in enumerate(operands[2:], start=2):
#                 if op in [']', ']!']:
#                     closing_bracket_index = i
#                     break
            
#             if closing_bracket_index is None:
#                 raise ParseError(f"Missing closing bracket in {mnemonic} at line {line_num}")
            
#             # Check contents between brackets
#             address_operands = operands[2:closing_bracket_index]
#             if len(address_operands) not in [1, 3]:
#                 raise ParseError(f"Invalid address format in {mnemonic} at line {line_num}")
            
#             if len(address_operands) == 3 and address_operands[1] != ',':
#                 raise ParseError(f"Invalid address format in {mnemonic} at line {line_num}")