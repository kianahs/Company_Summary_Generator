from crawl import crawl_website
import asyncio
from clean import clean_scraped_text
from generate_summary import summarize
from merge_summaries import merge_summaries
import os
from openai import OpenAI


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

    free_plan = True

    if free_plan:
        llm_model = "llama3-70b-8192"
        client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )
    else:
        llm_model = "gpt-4.1-mini"
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

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

        summary = summarize(client=client, llm_model=llm_model, content=clean_text, endpoint=item, dir_name=os.path.join(
            root_dir, company, "Summaries", llm_model))
        summaries.append(summary)

    merge_summaries(client=client, llm_model=llm_model, summaries=summaries, dir_name=os.path.join(
        root_dir, company, "Final Summary", llm_model), summarize_llm=llm_model)

if __name__ == "__main__":
    asyncio.run(main())
