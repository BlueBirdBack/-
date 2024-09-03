"""Module for converting VTT and SRT files to plain text transcripts."""

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
