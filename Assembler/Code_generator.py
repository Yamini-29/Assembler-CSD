from typing import List, Dict, Union
from Parser import Label, Instruction
from Tokenize import tokenize
import Parser
from opcode_table import opcode_table
import Semantic_Analyzer.Semantic_Analyzer
from Semantic_Analyzer.Semantic_Analyzer import SemanticAnalyzer, SemanticError
class CodeGenerator:
    def __init__(self, ast: List[Union[Label, Instruction]], symbol_table: Dict[str, int]):
        self.ast=ast
        self.symbol_table=symbol_table
        self.machine_code=[]
    def generate_machine_code(self):
        for node in self.ast:
            if isinstance(node, Instruction):
                binary_instruction = self.encode_instruction(node)
                self.machine_code.append(binary_instruction)
        return self.machine_code
    
    def encode_instruction(self, instruction:Instruction)->int:
        opcode=opcode_table.get(instruction.mnemonic.upper())
        # print(instruction.mnemonic)
        if opcode is None:
            raise SemanticError(f"Unsupported mnemonic '{instruction.mnemonic}'")
        mnemonic = instruction.mnemonic.lower()
        #Encode operands assuming all instructions are 4 bytes long
        # Determine `itype` based on instruction category
        if mnemonic in {'ldr', 'str', 'mov'}:
            itype = 0b00  # Memory type
        elif mnemonic in {'add', 'sub', 'mul', 'div', 'and', 'or', 'eor', 'asl', 'asr'}:
            itype = 0b01  # Arithmetic type
        elif mnemonic in {'b', 'br', 'bl', 'beq', 'blt', 'bgt', 'cmp'}:
            itype = 0b10  # Branch type
        elif mnemonic == 'svc':
            itype = 0b11  # System Call type
        else:
            raise SemanticError(f"Unsupported instruction type for '{instruction.mnemonic}'")

        # Common register encoding for rd and rn if needed
        rd = self.encode_register(instruction.operands[0])
        rn = self.encode_register(instruction.operands[1]) if len(instruction.operands) > 1 else 0

        # Memory Type Encoding (LDR, STR, MOV)
        if itype == 0b00:
            if mnemonic == 'mov':
                # MOV rd, imm/register
                is_imm = 1 if instruction.operands[1].startswith('#') else 0
                if is_imm:
                    imm_val = self.encode_immediate(instruction.operands[1])
                    return (itype << 30) | (opcode << 24) | (rd << 20) | (is_imm << 15) | imm_val
                else:
                    rm = self.encode_register(instruction.operands[1])
                    return (itype << 30) | (opcode << 24) | (rd << 20) | rm
            else:
                # LDR/STR rd, [rn, #imm]
                is_imm = 1 if instruction.operands[2].startswith('#') else 0
                imm_val = self.encode_immediate(instruction.operands[2]) if is_imm else 0
                return (itype << 30) | (opcode << 24) | (rd << 20) | (rn << 16) | (is_imm << 15) | imm_val
        # Arithmetic Type Encoding (ADD, SUB, etc.)
        elif itype == 0b01:
            is_imm = 1 if instruction.operands[2].startswith('#') else 0
            if is_imm:
                imm_val = self.encode_immediate(instruction.operands[2])
                return (itype << 30) | (opcode << 24) | (rd << 20) | (rn << 16) | (is_imm << 15) | imm_val
            else:
                rm = self.encode_register(instruction.operands[2])
                return (itype << 30) | (opcode << 24) | (rd << 20) | (rn << 16) | rm
        # Branch Type Encoding (B, BR, BL, BEQ, BLT, BGT, CMP)
        elif itype == 0b10:
            # Branch encoding with immediate address or register
            if mnemonic in {'b', 'bl'}:
                addr = self.encode_immediate(instruction.operands[0])
                return (itype << 30) | (opcode << 24) | addr
            elif mnemonic in {'beq', 'blt', 'bgt', 'cmp'}:
                rm = self.encode_register(instruction.operands[1])
                return (itype << 30) | (opcode << 24) | (rd << 16) | rm
         # System Call Type Encoding (SVC)
        elif itype == 0b11:
            # SVC #imm
            imm_val = self.encode_immediate(instruction.operands[0])
            return (itype << 30) | (opcode << 24) | imm_val

        raise SemanticError(f"Encoding failed for '{instruction.mnemonic}'") 
        
    def encode_register(self, reg: str)-> int:
        #Assuming registers are named r0-r15
        if reg.startswith('r') and reg[1:].isdigit():
            reg_num = int(reg[1:])
            if 0<=reg_num<16:
                return reg_num
        raise SemanticError(f"Invalid register '{reg}'")

    def encode_immediate(self, imm: str) -> int:
        if imm.startswith('#'):
            try:
                return int(imm[1:],0)
            except ValueError:
                raise SemanticError(f"Invalid immediate value '{imm}'")
        raise SemanticError(f"Invalid immediate format '{imm}'")
    

if __name__ == "__main__":
    input_code = """
        mov r0, r1
        add r1, r2, r3
        cmp r0, r4
    """

    tokens = tokenize(input_code)
    parser = Parser.Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer(ast)
    errors = analyzer.analyze()
    
    symbol_table=analyzer.build_symbol_table()

    if errors:
        for error in errors:
            print(error)
    else:
        print("No semantic errors found.")
        code_generator = CodeGenerator(ast, symbol_table)
        machine_code = code_generator.generate_machine_code()

        # Output the machine code in hex format
        for code in machine_code:
            print(f"{code:08b}")

