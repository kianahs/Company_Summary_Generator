from crawl import crawl_website
import asyncio
from clean import clean_scraped_text
from generate_summary import summarize
from merge_summaries import merge_summaries
import os
from openai import OpenAI


def get_client(free_plan: bool) -> tuple[str, OpenAI]:
    if free_plan:
        return (
            "llama3-70b-8192",
            OpenAI(
                api_key=os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1"
            )
        )
    else:
        return (
            "gpt-4.1-mini",
            OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )


async def main():

    endpoints = ['', 'features', 'why-syfter', 'resources',
                 'about-us', 'technical-information', 'contact']
    navbar = [
        "Home", "Features", "Why Syfter", "Resources",
        "About Us", "Technical Information", "Contact", "Book A Demo"
    ]
    url = "https://filament.ai"
    company = "filament"
    root_dir = 'Outputs'

    free_summarizer_llm = False
    free_merger_llm = False

    summarizer_llm_model, summarizer_client = get_client(free_summarizer_llm)
    merger_llm_model, merger_client = get_client(free_merger_llm)

    summaries = []

    for item in endpoints:

        markdown = await crawl_website(
            url=url,
            endpoint=item,
            company=company,
            dir_name=os.path.join(root_dir, company, "Scraped Data")
        )

        clean_text = clean_scraped_text(
            text=markdown, dir_name=os.path.join(
                root_dir, company, "Cleaned Scraped Data"), endpoint=item, navbar=navbar)

        summary = summarize(client=summarizer_client, llm_model=summarizer_llm_model, content=clean_text, endpoint=item, dir_name=os.path.join(
            root_dir, company, "Summaries", summarizer_llm_model))
        summaries.append(summary)

    merge_summaries(client=merger_client, llm_model=merger_llm_model, summaries=summaries, dir_name=os.path.join(
        root_dir, company, "Final Summary", merger_llm_model), summarize_llm=summarizer_llm_model)

if __name__ == "__main__":
    asyncio.run(main())
