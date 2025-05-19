from crawl import crawl_website
import asyncio
from clean import clean_scraped_text
from generate_summary import summarize
from merge_summaries import merge_summaries
import os
from openai import OpenAI
from RAG import execute_RAG_pipeline
import json
import argparse


def get_config(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


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

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    args = parser.parse_args()

    config = get_config(args.config)
    pipeline = config["pipeline"]
    endpoints = config["endpoints"]
    navbar = config["navbar"]
    url = config["url"]
    company = config["company"]
    root_dir = config["root_dir"]

    if not pipeline["RAG"]["active"]:
        summarizer_llm_model, summarizer_client = get_client(
            pipeline["free_summarizer_llm"])
        merger_llm_model, merger_client = get_client(
            pipeline["free_merger_llm"])

    summaries = []

    for item in endpoints:

        markdown = await crawl_website(
            url=url,
            endpoint=item,
            company=company,
            dir_name=os.path.join(root_dir, company, "Scraped Data")
        )

        clean_text = clean_scraped_text(
            text=markdown, dir_name=os.path.join(root_dir, company, "Cleaned Scraped Data"), endpoint=item, navbar=navbar)
        if not pipeline["RAG"]["active"]:
            summary = summarize(client=summarizer_client, llm_model=summarizer_llm_model, content=clean_text, endpoint=item, dir_name=os.path.join(
                root_dir, company, "Summaries", summarizer_llm_model))
            summaries.append(summary)

    if not pipeline["RAG"]["active"]:
        merge_summaries(client=merger_client, llm_model=merger_llm_model, summaries=summaries, dir_name=os.path.join(
            root_dir, company, "Final Summary", merger_llm_model), summarize_llm=summarizer_llm_model)
    else:
        execute_RAG_pipeline(dir_path=os.path.join(root_dir, company, "Cleaned Scraped Data"),
                             output_dir=os.path.join(
            root_dir, company, "Final Summary", "RAG"), free_plan=pipeline["RAG"]["free_plan"])


if __name__ == "__main__":
    asyncio.run(main())


# async def main():

#     pipeline = {
#         "RAG": {
#             "active": True,
#             "free_plan": True
#         },
#         "free_summarizer_llm": True,
#         "free_merger_llm": True
#     }
#     endpoints = ['', 'features', 'why-syfter', 'resources',
#                  'about-us', 'technical-information', 'contact']
#     navbar = [
#         "Home", "Features", "Why Syfter", "Resources",
#         "About Us", "Technical Information", "Contact", "Book A Demo"
#     ]
#     url = "https://filament.ai"
#     company = "filament"
#     root_dir = 'Outputs'

#     if not pipeline["RAG"]["active"]:
#         summarizer_llm_model, summarizer_client = get_client(
#             pipeline["free_summarizer_llm"])
#         merger_llm_model, merger_client = get_client(
#             pipeline["free_merger_llm"])

#     summaries = []

#     for item in endpoints:

#         markdown = await crawl_website(
#             url=url,
#             endpoint=item,
#             company=company,
#             dir_name=os.path.join(root_dir, company, "Scraped Data")
#         )

#         clean_text = clean_scraped_text(
#             text=markdown, dir_name=os.path.join(root_dir, company, "Cleaned Scraped Data"), endpoint=item, navbar=navbar)
#         if not pipeline["RAG"]["active"]:
#             summary = summarize(client=summarizer_client, llm_model=summarizer_llm_model, content=clean_text, endpoint=item, dir_name=os.path.join(
#                 root_dir, company, "Summaries", summarizer_llm_model))
#             summaries.append(summary)

#     if not pipeline["RAG"]["active"]:
#         merge_summaries(client=merger_client, llm_model=merger_llm_model, summaries=summaries, dir_name=os.path.join(
#             root_dir, company, "Final Summary", merger_llm_model), summarize_llm=summarizer_llm_model)
#     else:
#         execute_RAG_pipeline(dir_path=os.path.join(root_dir, company, "Cleaned Scraped Data"),
#                              output_dir=os.path.join(
#             root_dir, company, "Final Summary", "RAG"), free_plan=pipeline["RAG"]["free_plan"])
