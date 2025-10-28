import argparse

def process_vmem_file(input_file, place_zero):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    filtered_lines = []
    previous_address = None
    previous_data_length = 0

    for line in lines:
        if line.startswith('@'):
            current_address = int(line[1:], 16)
            if previous_address is not None and place_zero:
                gap = current_address - (previous_address + previous_data_length)
                if gap > 0:
                    zero_bytes = '00 ' * gap
                    filtered_lines.append(zero_bytes.strip() + '\n')
            previous_address = current_address
            previous_data_length = 0
        else:
            filtered_lines.append(line)
            previous_data_length += len(line.split())

    # Add @00000000 at the top
    filtered_lines.insert(0, '@00000000\n')

    for line in filtered_lines:
        print(line, end='')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a vmem file.')
    parser.add_argument('--file', '-f', type=str, help='The input vmem file')
    parser.add_argument('--place_zero', '-pz', action='store_true', help='Place zero bytes for gaps between addresses')

    args = parser.parse_args()
    process_vmem_file(args.file, args.place_zero)
