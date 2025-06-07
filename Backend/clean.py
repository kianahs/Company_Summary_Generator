import re
import os
from typing import Optional


def clean_scraped_text(text: str, dir_name: str, endpoint: str, navbar: Optional[list[str]] = None) -> str:

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            text = ''.join(lines[i:])
            break

    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)

    if navbar:
        for elem in navbar:
            text = re.sub(fr"{elem}\s*", '', text)

    text = re.sub(r'\n\s*[*•?]+\s*\n', '\n', text)

    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()

    output_file = endpoint + "_cleaned.md"
    output_path = os.path.join(dir_name, output_file)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return text


if __name__ == "__main__":
    root_dir = "results"
    scraped_dir = "Scraped Data"
    company = 'filament'
    directory = os.path.join(root_dir, company, scraped_dir)
    new_dir = "Cleaned scraped Data"

    navbar = [
        "Home", "Features", "Why Syfter", "Resources",
        "About Us", "Technical Information", "Contact", "Book A Demo"
    ]

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        clean_text = clean_scraped_text(
            raw_text, os.path.join(root_dir, company, new_dir), os.path.splitext(file_name)[0], navbar)
