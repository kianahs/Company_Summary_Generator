import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Tuple


def detect_nav_and_endpoints(base_url: str) -> Tuple[List[str], List[str]]:

    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {base_url}: {e}")
        return [], []

    soup = BeautifulSoup(response.text, "html.parser")

    nav_labels = set()
    endpoint_paths = set()
    endpoint_paths.add('')
    domain = urlparse(base_url).netloc

    for a_tag in soup.find_all("a", href=True):
        label = a_tag.get_text(strip=True)
        href = a_tag["href"].split("#")[0]

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if parsed.netloc != domain:
            continue

        path = parsed.path.strip("/")

        if path and len(path) < 50 and not path.endswith(('.pdf', '.jpg', '.png', '.zip')):
            endpoint_paths.add(path)

        if label and 2 < len(label) < 40 and all(c.isprintable() for c in label):
            nav_labels.add(label)

    return sorted(endpoint_paths), sorted(nav_labels)


if __name__ == "__main__":
    url = "https://filament.ai"
    endpoints, navbar = detect_nav_and_endpoints(url)

    print("Found Endpoints:\n", endpoints)

    print("Found Navbar Items:\n", navbar)
