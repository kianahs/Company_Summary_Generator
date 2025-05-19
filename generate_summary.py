import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def summarize(content, endpoint, dir_name):

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    prompt = f"""
              You are a business analyst. Based on the website content below, generate a structured company summary with the following sections:
              1. Company Description : What is the company’s core mission, purpose, and values?
              2. Products & Services : What does the company offer? What problems do they solve?
              3. Leadership Team (if available): Who are the key individuals in leadership positions? Provide brief bios where possible.
              4. Notable Customers or Mentions: List the company names mentioned on a company website. mention if they are if they are a customer, partner etc
              5. Recent News: What updates, blog posts, or press releases are highlighted on the site?

              --- WEBSITE CONTENT START ---
              {content}
              --- WEBSITE CONTENT END ---

              Be concise and informative. Use bullet points where appropriate. 
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
