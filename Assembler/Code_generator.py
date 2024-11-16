from typing import List, Dict, Union
from dataclasses import dataclass
from opcode_table import opcode_table

@dataclass
class Instruction:
    mnemonic: str
    operands: List[str]

@dataclass
class Label:
    name: str

class CodeGenerator:
    def __init__(self, ast: List[Union[Label, Instruction]], symbol_table: Dict[str, int]):
        self.ast = ast
        self.symbol_table = symbol_table
        self.machine_code = []

    def generate_machine_code(self) -> List[int]:
        """Generate machine code for the entire AST."""
        for node in self.ast:
            if isinstance(node, Instruction):
                binary_instruction = self.encode_instruction(node)
                self.machine_code.append(binary_instruction)
        return self.machine_code

    def encode_instruction(self, instruction: Instruction) -> int:
        """Encode a single instruction into its binary representation."""
        mnemonic = instruction.mnemonic.upper()
        if mnemonic not in opcode_table:
            raise ValueError(f"Unsupported mnemonic: {mnemonic}")

        opcode = opcode_table[mnemonic]
        operand_count = len(instruction.operands)
        
        # Initialize instruction fields
        itype = opcode >> 6  # Extract instruction type (bits 6-7)
        u_ctrl = opcode & 0x3F  # Extract control signals (bits 0-5)
        rd_addr = 0
        rm_addr = 0
        is_imm = 0
        value = 0

        # Branch instructions (B, BL, BLX, BX)
        if mnemonic in ['B', 'BL', 'BLX', 'BX', 'BEQ', 'BLT', 'BGT']:
            if operand_count != 1:
                raise ValueError(f"Branch instruction {mnemonic} expects 1 operand")
            if instruction.operands[0].startswith('#'):
                is_imm = 1
                value = self.encode_immediate(instruction.operands[0])
            elif instruction.operands[0] in self.symbol_table:
                value = self.symbol_table[instruction.operands[0]] & 0x7FFF
            else:
                raise ValueError(f"Invalid branch target: {instruction.operands[0]}")
        elif mnemonic == 'BR':
            if operand_count != 1:
                raise ValueError(f"Branch instruction {mnemonic} expects 1 operand")
            rm_addr = self.encode_register(instruction.operands[0])

        # System instructions (SWI, CLZ, MSR, MRS)
        elif mnemonic in ['SWI', 'CLZ', 'MSR', 'MRS']:
            if operand_count != 1:
                raise ValueError(f"{mnemonic} instruction expects 1 operand")
            if instruction.operands[0].startswith('#'):
                is_imm = 1
                value = self.encode_immediate(instruction.operands[0])
            else:
                rd_addr = self.encode_register(instruction.operands[0])

        # Compare instructions (CMP, CMN, TEQ, TST)
        elif mnemonic in ['CMP', 'CMN', 'TEQ', 'TST']:
            if operand_count != 2:
                raise ValueError(f"{mnemonic} instruction expects 2 operands")
            rd_addr = self.encode_register(instruction.operands[0])
            if instruction.operands[1].startswith('#'):
                is_imm = 1
                value = self.encode_immediate(instruction.operands[1])
            else:
                rm_addr = self.encode_register(instruction.operands[1])

        # Data movement (MOV, MVN)
        elif mnemonic in ['MOV', 'MVN']:
            if operand_count != 2:
                raise ValueError(f"{mnemonic} instruction expects 2 operands")
            rd_addr = self.encode_register(instruction.operands[0])
            if instruction.operands[1].startswith('#'):
                is_imm = 1
                value = self.encode_immediate(instruction.operands[1])
            else:
                rm_addr = self.encode_register(instruction.operands[1])

        # Memory operations (LDR, STR)
        elif mnemonic in ['LDR', 'STR']:
            if operand_count != 2:
                raise ValueError(f"{mnemonic} instruction expects 2 operands")
            rd_addr = self.encode_register(instruction.operands[0])
            if instruction.operands[1].startswith('#'):
                is_imm = 1
                value = self.encode_immediate(instruction.operands[1])
            else:
                rm_addr = self.encode_register(instruction.operands[1])

        # Basic arithmetic/logic (ADD, SUB, AND, ORR, etc.)
        elif mnemonic in ['ADD', 'SUB', 'MUL', 'DIV', 'AND', 'OR', 'EOR', 'ASL', 'ASR']:
            if operand_count != 2:
                raise ValueError(f"{mnemonic} instruction expects 2 operands")
            rd_addr = self.encode_register(instruction.operands[0])
            if instruction.operands[1].startswith('#'):
                is_imm = 1
                value = self.encode_immediate(instruction.operands[1])
            else:
                rm_addr = self.encode_register(instruction.operands[1])

        #System call
        elif mnemonic == 'SVC':
            if operand_count != 1:
                raise ValueError("SVC instruction expects 1 operand")
            if instruction.operands[0].startswith('#'):
                is_imm = 1
                value = self.encode_immediate(instruction.operands[0])
            else:
                raise ValueError("SVC operand must be immediate")
        
        else:
            raise ValueError(f"Unsupported instruction mnemonic: {mnemonic}")
        
        # Combine all fields into final instruction
        return (
            (itype << 30) |           # bits [30:31] for instruction type
            (u_ctrl << 24) |          # bits [24:29] for control signals
            (rd_addr << 20) |         # bits [20:23] for rd register address
            (rm_addr << 16) |         # bits [16:19] for rm register address
            (is_imm << 15) |          # bit [15] indicates if it's immediate
            (value & 0x7FFF)          # bits [0:14] for immediate value or address
        )

    def encode_register(self, reg: str) -> int:
        """Encode a register name to its binary representation."""
        if reg.startswith('r') and reg[1:].isdigit():
            reg_num = int(reg[1:])
            if 0 <= reg_num < 16:
                return reg_num
        raise ValueError(f"Invalid register: {reg}")

    def encode_immediate(self, imm: str) -> int:
        """Encode an immediate value to its binary representation."""
        if imm.startswith('#'):
            try:
                value = int(imm[1:], 0)
                if 0 <= value < 0x8000:  # 15-bit immediate value
                    return value
                raise ValueError(f"Immediate value out of range: {imm}")
            except ValueError:
                raise ValueError(f"Invalid immediate value: {imm}")
        raise ValueError(f"Invalid immediate format: {imm}")

def format_binary(num: int, width: int = 32) -> str:
    """Format a number as a binary string with given width."""
    return format(num, f'0{width}b')

if __name__ == "__main__":
    # Example usage with only 2-operand instructions
    test_program = [
        Instruction("ADD", ["r1", "r2"]),
        Instruction("MOV", ["r4", "#10"]),
        Instruction("CMP", ["r1", "r2"]),
        Instruction("B", ["#1000"]),
        Instruction("LDR", ["r1", "#100"]),
    ]
    
    symbol_table = {'loop': 0x100}
    code_gen = CodeGenerator(test_program, symbol_table)
    machine_code = code_gen.generate_machine_code()
    
    print("Generated Machine Code:")
    for i, code in enumerate(machine_code):
        print(f"Instruction {i}: {format_binary(code)}")
        # Print instruction breakdown
        itype = (code >> 30) & 0x3
        u_ctrl = (code >> 24) & 0x3F
        rd = (code >> 20) & 0xF
        rm = (code >> 16) & 0xF
        is_imm = (code >> 15) & 0x1
        value = code & 0x7FFF
        print(f"  Type: {itype:02b}, Control: {u_ctrl:06b}, Rd: {rd:04b}, Rm: {rm:04b}, Imm: {is_imm}, Value: {value:015b}")