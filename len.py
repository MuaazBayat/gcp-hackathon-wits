def add_comma_to_lines(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Strip any leading/trailing whitespace, then add a comma at the beginning
            modified_line = ',' + line.strip()
            # Write the modified line to the output file
            outfile.write(modified_line + '\n')

def main():
    input_filename = 'logfile.txt'  # Replace with your input file name
    output_filename = 'output.txt'  # Replace with your desired output file name

    print(f"Adding commas to lines from {input_filename} and writing to {output_filename}...")
    add_comma_to_lines(input_filename, output_filename)
    print(f"Process completed. Check the file: {output_filename}")

if __name__ == "__main__":
    main()