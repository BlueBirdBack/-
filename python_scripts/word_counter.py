"""A script to count words in a text file and count unique words sorted by frequency."""

import argparse
from collections import Counter
import re
from transcript_converters import vtt_to_transcript, srt_to_transcript


def process_file(file_path):
    """Process the file based on its extension."""
    if file_path.lower().endswith(".srt"):
        return srt_to_transcript(file_path)
    elif file_path.lower().endswith(".vtt"):
        return vtt_to_transcript(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


def count_words(file_path):
    """Count the number of words in the given file."""
    try:
        content = process_file(file_path)
        print(content)
        return len(content.split())
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except IOError:
        return f"Error: Unable to read file '{file_path}'."


def count_unique_words(file_path):
    """Count unique words in the given file and sort them by frequency."""
    try:
        content = process_file(file_path)
        words = re.findall(r"\b\w+\b", content.lower())
        word_counts = Counter(words)
        sorted_word_counts = word_counts.most_common()
        return sorted_word_counts
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except IOError:
        return f"Error: Unable to read file '{file_path}'."


def main():
    """Parse command-line arguments and run the word counter."""
    parser = argparse.ArgumentParser(
        description="Count words in a text file and count unique words sorted by frequency."
    )
    parser.add_argument("file_path", help="Path to the text file")
    args = parser.parse_args()

    total_words = count_words(args.file_path)
    if isinstance(total_words, int):
        print(f"Total words in '{args.file_path}': {total_words}")
    else:
        print(total_words)

    unique_word_counts = count_unique_words(args.file_path)
    if isinstance(unique_word_counts, list):
        print(f"\nWord frequencies in '{args.file_path}':")
        print(f"Total unique words: {len(unique_word_counts)}")
        for word, count in unique_word_counts:
            print(f"{word}: {count}")
    else:
        print(unique_word_counts)


if __name__ == "__main__":
    main()
