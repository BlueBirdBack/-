"""A script to count words in a text file and count unique words sorted by frequency."""

import argparse
from collections import Counter
import re


def vtt_to_transcript(vtt_file_path):
    """Convert a VTT file to a plain text transcript."""
    with open(vtt_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Remove header
    content = re.sub(r"WEBVTT\nKind:.*\nLanguage:.*\n", "", content)

    # Remove timestamps and positioning info
    content = re.sub(
        r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n", "", content
    )
    content = re.sub(
        r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*$",
        "",
        content,
        flags=re.MULTILINE,
    )

    # Remove inline timestamp tags
    content = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d{3}>", "", content)

    # Remove lines that are just timestamps
    content = re.sub(
        r"^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*$",
        "",
        content,
        flags=re.MULTILINE,
    )

    # Remove empty lines
    content = re.sub(r"^\s*$\n", "", content, flags=re.MULTILINE)

    # Remove HTML-like tags
    content = re.sub(r"<[^>]+>", "", content)

    # Remove consecutive duplicate lines
    lines = content.split("\n")
    unique_lines = []
    previous_line = None
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and stripped_line != previous_line:
            unique_lines.append(stripped_line)
        previous_line = stripped_line

    transcript = " ".join(unique_lines)

    return transcript


def srt_to_transcript(srt_file_path):
    """Convert an SRT file to a plain text transcript."""
    with open(srt_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Remove SRT index numbers
    content = re.sub(r"^\d+$", "", content, flags=re.MULTILINE)

    # Remove timestamps
    content = re.sub(
        r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}",
        "",
        content,
        flags=re.MULTILINE,
    )

    # Remove empty lines and HTML-like tags
    content = re.sub(r"^\s*$\n", "", content, flags=re.MULTILINE)
    content = re.sub(r"<[^>]+>", "", content)

    # Join lines and remove extra whitespace
    transcript = " ".join(line.strip() for line in content.split("\n") if line.strip())

    return transcript


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
        print(f"Total unique words: {len(unique_word_counts)}")  # Add this line
        for word, count in unique_word_counts:
            print(f"{word}: {count}")
    else:
        print(unique_word_counts)


if __name__ == "__main__":
    main()
