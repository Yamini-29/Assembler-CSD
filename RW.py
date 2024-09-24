def read_and_write_file(input_filename, output_filename):
    try:
        
        with open(input_filename, 'r') as input_file:
            
            lines = input_file.readlines()
        
        with open(output_filename, 'w') as output_file:
           
            for line in lines:
                output_file.write(line)
                
        print(f"Successfully written to {output_filename}")
    
    except FileNotFoundError:
        print(f"Error: {input_filename} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():

    input_filename = input("Enter the input filename (e.g., 'Prog.asm'): ")


    output_filename = input("Enter the output filename (e.g., 'Prog.o'): ")

    read_and_write_file(input_filename, output_filename)

if __name__ == "__main__":
    main()
