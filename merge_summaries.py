import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def merge_summaries(summaries: str, dir_name: str, summarize_llm: str) -> str:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    current_date = datetime.now().strftime("%B %Y")
    concatenated_summaries = "\n\n--- Summary Chunk ---\n\n".join(summaries)

    prompt = f"""
        You are a skilled business analyst. You are given several partial summaries of a company's website. Your task is to merge them into a single, clean, and structured Markdown report.

        Please follow this exact section format using **Markdown syntax**:

        ## Company Description *(if available)*  
        Describe the company’s mission, purpose, and core values.

        ## Products & Services *(if available)*  
        List and briefly describe the company’s main offerings and what problems they solve.

        ## Leadership Team *(if available)*  
        List key leadership personnel with their name, title, and a brief bio if provided.

        ## Notable Customers or Company Mentions *(if available)*  
        Include other company names mentioned, and whether they are customers, partners, or otherwise affiliated.

        ## Recent News or Updates *(if available — current date is {current_date}*
        Summarize relevant blog posts, press releases, or updates.

        **Summary Chunks to Merge:**

        {concatenated_summaries}
       

        **Instructions:**
        - Merge all provided summaries into a single, well-structured report using the specified section format.
        - Consolidate all factual information without omitting any meaningful details.
        - Avoid redundancy: do not duplicate points, sentences, or sections across the report.
        - Do **not** fabricate, infer, or hallucinate any content that is not explicitly present in the input summaries.
        - Use valid **Markdown** (`##` headers, bullet points, or short paragraphs).
        - Leave a section blank if no content applies.
        - Be concise and accurate in your wording.
        - Return **only** the final Markdown-formatted report — do **not** include extra explanations, commentary, or system output.
        """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    final_summary = response.choices[0].message.content

    with open(f"{dir_name}/final_merged_summary_{summarize_llm}.md", "w", encoding="utf-8") as f:
        f.write(final_summary)

    print(final_summary)

    return final_summary


if __name__ == "__main__":
    root_dir = "results"
    company = "filament"
    new_dir = "Final Summary"
    summaries_dir = 'Summaries'
    files_path = os.path.join(root_dir, company, summaries_dir)
    dir_name = os.path.join(root_dir, company, new_dir)

    for model in sorted(os.listdir(files_path)):
        full_path = os.path.join(files_path, model)
        summaries = []
        for file_name in sorted(os.listdir(full_path)):

            file_path = os.path.join(full_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                summaries.append(
                    content)

        merge_summaries(summaries, dir_name, model)
