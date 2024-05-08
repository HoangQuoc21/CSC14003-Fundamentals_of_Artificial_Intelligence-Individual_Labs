import os
from pl_resolution_algorithm import pl_resolution

def main():
    # Define directory path
    input_directory_path = 'input/'
    output_directory_path = 'output/'

    # Define a string list to save input files
    file_list = []

    # Add files name to the list
    for filename in os.listdir(input_directory_path):
        # Check if the file is text file
        if filename.endswith('.txt'):
            # Add the file name to the list
            file_list.append(filename)

    # Loop through the files list
    for file_name in file_list:
        # Define input/ouput file path
        input_file_path = input_directory_path + file_name
        output_file_path = output_directory_path + file_name.replace('input', 'output')

        # Load data from input file
        with open(input_file_path, 'r') as fin:
            # Read alpha statement 
            alpha = fin.readline().strip()

            # Read the total number of clauses
            n = int(fin.readline().strip())

            # Define Knowledge Base
            kb = []

            # Read clauses and add in to knowledge base
            for i in range(n):
                clause = fin.readline().strip()
                kb.append(clause)

        
        # Run Pl_Resolution Algorithm
        resolver = pl_resolution(kb, alpha)
        resolver.pl_resolution()

        # Write answer to output file
        with open(output_file_path, 'w+') as f:
            resolver.print_output(f = f)
            
    # Create output directory if it does not already exist  
    if not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)
    
    # Print success message
    print('Output files are created successfully!')

if __name__ == '__main__':
    main()