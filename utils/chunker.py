import re
import requests

def scrape_pubmed(url: str):
    """Fetch a PubMed article's abstract using NCBI's official API, given a PubMed URL."""
    match = re.search(r"(\d+)", url)
    if not match:
        print(f"Could not find a PMID (article number) in: {url}")
        return None

    pmid = match.group(1)
    api_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        f"?db=pubmed&id={pmid}&rettype=abstract&retmode=text"
    )

    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

    text = response.text.strip()
    if not text:
        print(f"No content returned for PMID {pmid}")
        return None

    return text
