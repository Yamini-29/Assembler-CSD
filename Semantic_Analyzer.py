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
