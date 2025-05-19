import asyncio
import os
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig


async def crawl_website(url, endpoint, company, dir_name):

    full_url = url + '/' + endpoint

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=full_url,
                                    config=CrawlerRunConfig(
                                        css_selector=[
                                            "*:not([id*='cky']):not([class*='cky']):not([id*='cookie']):not([class*='cookie'])"
                                        ]
                                    ))
        md_result = result.markdown

        with open(f"{dir_name}/{company}_{endpoint}.md", "w", encoding="utf-8") as f:
            f.write(md_result)

        return md_result

if __name__ == "__main__":

    endpoints = ['', 'features', 'why-syfter', 'resources',
                 'about-us', 'technical-information', 'contact']

    url = "https://filament.ai"
    company = "filament"
    dir_name = f"results/{company}/Scraped Data"

    for item in endpoints:

        markdown = asyncio.run(crawl_website(
            url, item, company, dir_name))
