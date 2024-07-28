def filter_short_lines(input_file, output_file, min_length=280):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if len(line) >= min_length:
                outfile.write(line + '\n')
            else:
                print(f"Removed line (shorter than {min_length} chars): {line}")

if __name__ == "__main__":
    input_json_file = 'theone.json'  # Update this path
    output_json_file = 'filtered_output.json'  # Update this path

    filter_short_lines(input_json_file, output_json_file)
