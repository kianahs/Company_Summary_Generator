import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def summarize(content: str, endpoint: str, dir_name: str) -> str:

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    current_date = datetime.now().strftime("%B %Y")

    prompt = f"""
                You are a skilled business analyst. Your task is to extract and organize information from a company's website into a clear, structured report.

                Please generate a report using the following sections:

                ## Company Description *(if available)*
                Summarize the company’s core mission, purpose, values, and what they fundamentally stand for.

                ## Products & Services *(if available)*
                List and briefly describe the main products and/or services the company offers. Include what problems they solve or which industries they serve.

                ## Leadership Team *(if available)*
                Identify key individuals in leadership positions. For each, provide their name, title, and a brief background or bio.

                ## Notable Customers or Company Mentions *(if available)*
                Mention all other companies referenced on the site. Specify whether they are customers, partners, or otherwise associated.

                ## Recent News or Updates *(if available) -  current date is {current_date}*
                Summarize recent blog posts, press releases, or updates mentioned on the site.

                ### Website Content:
                {content}
             

                **Instructions:**
                - Format the output as a clean and well-structured **Markdown (.md)** report.
                - Use `##` headers to separate each major section.
                - Present content using bullet points or short, clear paragraphs for readability.
                - Avoid repeating the same information across multiple sections.
                - Do **not** fabricate, infer, or hallucinate any information not explicitly present in the input.
                - Be concise and factually accurate.
                - Include all relevant details found in the input that belong to each section.
                - If a section has no available information, leave it blank.
                - Return only the final Markdown-formatted report. Do not include explanations, comments, or system messages.

                """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    summary = response.choices[0].message.content

    with open(f"{dir_name}/{endpoint}_summary.md", "w", encoding="utf-8") as f:
        f.write(summary)

    print(summary)

    return summary


if __name__ == "__main__":

    root_dir = "results"
    company = "filament"
    new_dir = "Summaries"
    cleaned_scraped_dir = 'Cleaned scraped Data'
    files_path = os.path.join(root_dir, company, cleaned_scraped_dir)
    dir_name = os.path.join(root_dir, company, new_dir)

    for file_name in sorted(os.listdir(files_path)):

        file_path = os.path.join(files_path, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            summarize(content, os.path.splitext(file_name)[0], dir_name)
