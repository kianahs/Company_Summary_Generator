from crawl import crawl_website
import asyncio
from clean import clean_scraped_text
from generate_summary import summarize
from merge_summaries import merge_summaries
from token_counter import count_tokens
from auto_detect import detect_nav_and_endpoints
import os
from openai import OpenAI
from RAG import execute_RAG_pipeline
import json
import argparse
from datetime import datetime


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


async def main(company, url, free_plan):

    MODEL_CONTEXT = {
        "llama3-70b-8192": 8192,
        "gpt-4.1-mini": 1_000_000
    }
    buffer_ratio = 0.75
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    endpoints, navbar = detect_nav_and_endpoints(url)
    print("Found Endpoints:\n", endpoints)

    print("Found Navbar Items:\n", navbar)
    root_dir = f"Output_{timestamp}"

    model_name, llm_client = get_client(
        free_plan)
    model_context_limit = int(
        MODEL_CONTEXT[model_name] * buffer_ratio)

    max_tokens = 0

    cleaned_texts = []
    faulty_endpoints = []
    for item in endpoints:
        try:
            markdown = await crawl_website(
                url=url,
                endpoint=item,
                company=company,
                dir_name=os.path.join(root_dir, company, "Scraped Data")
            )
        except Exception as e:
            print(f"Skipping endpoint '{item}' due to error")
            # endpoints.remove(item)
            faulty_endpoints.append(item)
            continue

        clean_text = clean_scraped_text(
            text=markdown, dir_name=os.path.join(root_dir, company, "Cleaned Scraped Data"), endpoint=item, navbar=navbar)
        cleaned_texts.append(clean_text)
        max_tokens = max(max_tokens, count_tokens(
            clean_text, model=model_name))
    endpoints = [item for item in endpoints if item not in faulty_endpoints]
    use_rag = max_tokens > model_context_limit
    print(
        f"Free plan: {free_plan}\nModel: {model_name}\nContext limit (Buffer ratio: {buffer_ratio}): {model_context_limit}\nMax tokens per call: {max_tokens}\nRAG? {use_rag}\n")

    if use_rag:
        execute_RAG_pipeline(dir_path=os.path.join(root_dir, company, "Cleaned Scraped Data"),
                             output_dir=os.path.join(
            root_dir, company, "Final Summary", "RAG"), free_plan=free_plan)

    else:
        summaries = []
        for i, clean_text in enumerate(cleaned_texts):

            summary = summarize(client=llm_client, llm_model=model_name, content=clean_text, endpoint=endpoints[i], dir_name=os.path.join(
                root_dir, company, "Summaries", model_name))
            summaries.append(summary)

        merge_summaries(client=llm_client, llm_model=model_name, summaries=summaries, dir_name=os.path.join(
            root_dir, company, "Final Summary", model_name), summarize_llm=model_name)


if __name__ == "__main__":
    asyncio.run(main(company="FilamentXYZ",
                url="https://filament.ai", free_plan=True))
