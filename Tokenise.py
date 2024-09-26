import re
import sys

def tokenize_asm(asm_code):
    tokens = []
    
    
    pattern = r'(\w+|[.,]|\s+|\S)'

    lines = asm_code.strip().splitlines()
    
    for line in lines:
    
        line = line.split(';')[0].strip()
        
    
        line_tokens = re.findall(pattern, line)
        
   
        line_tokens = [token for token in line_tokens if token.strip()]
        
        tokens.extend(line_tokens)
    
    return tokens

def read_asm_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

def main():
    input_filename = input("Enter the input filename (e.g., 'hello.asm'): ")
    
  
    asm_code = read_asm_file(input_filename)
    

    tokens = tokenize_asm(asm_code)
    

    print(tokens)

if __name__ == "__main__":
    main()
