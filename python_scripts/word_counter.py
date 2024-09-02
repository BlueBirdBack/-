"""A script to count words in a text file."""

import argparse


def count_words(file_path):
    """Count the number of words in the given file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return len(content.split())
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except IOError:
        return f"Error: Unable to read file '{file_path}'."


def main():
    """Parse command-line arguments and run the word counter."""
    parser = argparse.ArgumentParser(description="Count words in a text file.")
    parser.add_argument("file_path", help="Path to the text file")
    args = parser.parse_args()

    result = count_words(args.file_path)
    if isinstance(result, int):
        print(f"Total words in '{args.file_path}': {result}")
    else:
        print(result)


if __name__ == "__main__":
    main()
