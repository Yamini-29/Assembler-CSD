opcode_table= {
    'ADD': '0000',  # Addition
    'SUB': '0001',  # Subtraction
    'MUL': '0010',  # Multiplication
    'SDIV': '0011', # Signed Division
    'UDIV': '0100', # Unsigned Division

    'AND': '0101',  # Bitwise AND
    'ORR': '0110',  # Bitwise OR
    'EOR': '0111',  # Bitwise XOR
    'MVN': '1000',  # Bitwise NOT

    'LSL': '1001',  # Logical Shift Left
    'LSR': '1010',  # Logical Shift Right

    'LDR': '1011',  # Load Register
    'STR': '1100',  # Store Register

    'CMP': '1101',  # Compare
    'TST': '1110',  # Test

    'B': '1111',     # Unconditional Branch
    'BEQ': '00001',  # Branch if Equal
    'BNE': '00010',  # Branch if Not Equal
    'BGT': '00011',  # Branch if Greater Than
    'BLT': '00100',  # Branch if Less Than

    'MOV': '00101',  # Move
    'PUSH': '00110', # Push to Stack
    'POP': '00111',  # Pop from Stack
}


