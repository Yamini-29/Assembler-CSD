import subprocess
import os

def assemble_asm_to_object(asm_file, obj_file):
    try:
        # Check if the input ASM file exists
        if not os.path.exists(asm_file):
            print(f"Error: {asm_file} not found.")
            return

        # Command to assemble the ASM file into an object file using NASM
        # The '-f elf32' flag is used for 32-bit assembly
        command = ['nasm', '-f', 'elf32', asm_file, '-o', obj_file]
        
        # Run the command and capture output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check for errors during the assembly process
        if result.returncode == 0:
            print(f"Successfully assembled {asm_file} into {obj_file}")
        else:
            print(f"Error assembling file: {result.stderr.decode()}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    asm_file = input("Enter the ASM file (e.g., 'Prog.asm'): ")
    obj_file = input("Enter the output object file (e.g., 'Prog.o'): ")

    assemble_asm_to_object(asm_file, obj_file)

if __name__ == "__main__":
    main()
