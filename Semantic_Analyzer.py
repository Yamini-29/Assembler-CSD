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
class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.valid_registers = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'sp', 'lr', 'pc']
        self.instructions = ['mov', 'ldr', 'str', 'add', 'sub', 'cmp', 'b', 'bl', 'bx']  # Add more as necessary
        self.condition_codes = ['eq', 'ne', 'gt', 'lt', 'ge', 'le']
        self.labels = {}
        self.branches = []

    def analyze(self):
        self.collect_labels_and_branches()

        for node in self.ast:
            if node['type'] == 'instruction':
                self.validate_instruction(node)
            elif node['type'] == 'directive':
                self.validate_directive(node)
            elif node['type'] == 'label':
                self.validate_label(node)

        self.check_label_references()


        if not self.errors:
            print("Code is semantically valid!")
        else:
            print("Semantic Errors:")
            for error in self.errors:
                print(error)

    def collect_labels_and_branches(self):
        # Collect label positions and branch instructions
        address = 0
        for node in self.ast:
            if node['type'] == 'label':
                self.labels[node['label']] = address
            elif node['type'] == 'instruction' and node['instruction'] in ['b', 'bl']:
                self.branches.append({'instruction': node, 'address': address})
            address += 1  # Increment the address as if each instruction occupies one address space

    def validate_instruction(self, node):
        instruction = node['instruction']
        operands = node.get('operands', [])
        
        # Check if the instruction is valid
        if instruction not in self.instructions:
            self.errors.append(f"Invalid instruction: {instruction}")

        # Check operand count for specific instructions
        if instruction == 'mov' and len(operands) != 2:
            self.errors.append(f"Invalid operand count for 'mov': {len(operands)}")

        # Validate register usage
        for operand in operands:
            if operand in self.valid_registers:
                self.check_register_usage(operand)
            elif operand.isdigit():
                self.check_immediate_value(int(operand))
            elif instruction in ['b', 'bl']:
                # For branches, check if the operand is a label
                if operand not in self.labels:
                    self.errors.append(f"Undefined label: {operand}")

    def check_register_usage(self, register):
        if register not in self.valid_registers:
            self.errors.append(f"Invalid register: {register}")

    def check_immediate_value(self, value):
        if not (0 <= value <= 255):  # 8-bit immediate value range with rotation
            self.errors.append(f"Immediate value out of range: {value}. Consider loading it into a register using 'ldr'.")

    def validate_directive(self, node):
        directive = node['directive']
        if directive not in ['.data', '.text']:
            self.errors.append(f"Invalid directive: {directive}")

    def validate_label(self, node):
        label = node['label']
        if not label.isidentifier():
            self.errors.append(f"Invalid label name: {label}")

    def check_label_references(self):
        # Check if all branch distances are valid
        for branch in self.branches:
            instruction = branch['instruction']
            target_label = instruction['operands'][0]
            current_address = branch['address']

            if target_label in self.labels:
                target_address = self.labels[target_label]
                branch_distance = target_address - current_address

                # Assuming a valid branch distance range for simplicity
                if not (-2048 <= branch_distance <= 2047):
                    self.errors.append(f"Branch distance out of range for label {target_label}: {branch_distance}")
            else:
                self.errors.append(f"Undefined label in branch: {target_label}")

# Example usage with an AST
ast = [
    {'type': 'label', 'label': 'start'},
    {'type': 'instruction', 'instruction': 'mov', 'operands': ['r0', 'r1']},
    {'type': 'instruction', 'instruction': 'ldr', 'operands': ['r1', '100']},
    {'type': 'directive', 'directive': '.text'},
    {'type': 'label', 'label': 'main'},
    {'type': 'instruction', 'instruction': 'ldr', 'operands': ['r3', '=300']},
    {'type': 'instruction', 'instruction': 'add', 'operands': ['r2', 'r1', 'r3']},
    {'type': 'instruction', 'instruction': 'b', 'operands': ['main']}
]

analyzer = SemanticAnalyzer(ast)
analyzer.analyze()
