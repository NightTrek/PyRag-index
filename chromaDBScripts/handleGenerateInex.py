import sys
from createIndexFromFolder import generate_index_from_folder

def main():
    if len(sys.argv) < 2:
        print("Please provide the directory as a command-line argument.")
        sys.exit(1)
    directory = sys.argv[1]
    generate_index_from_folder(directory, directory)

if __name__ == '__main__':
    main()