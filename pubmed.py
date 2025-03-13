import requests
import xml.etree.ElementTree as ET
import typer
from typing import List, Dict

# PubMed API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_papers(query: str) -> List[Dict]:
    """Fetch full research paper details from PubMed based on a query."""
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Limit results to 10
    }
    
    response = requests.get(PUBMED_SEARCH_URL, params=search_params)

    if response.status_code != 200:
        typer.echo("Error: Failed to fetch data from PubMed.")
        return []

    data = response.json()
    ids = data.get("esearchresult", {}).get("idlist", [])

    if not ids:
        typer.echo("No papers found for the given query.")
        return []

    # Fetch full details using efetch
    details_params = {
        "db": "pubmed",
        "id": ",".join(ids),  # Join IDs as a comma-separated string
        "retmode": "xml"  # XML format for parsing details
    }
    details_response = requests.get(PUBMED_FETCH_URL, params=details_params)

    if details_response.status_code != 200:
        typer.echo("Error: Failed to fetch paper details.")
        return []

    # Parse XML response
    root = ET.fromstring(details_response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text if article.find(".//PMID") is not None else "N/A"
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
        abstract_elem = article.find(".//Abstract/AbstractText")
        abstract = abstract_elem.text if abstract_elem is not None else "N/A"

        # Extract authors
        authors_list = []
        for author in article.findall(".//Author"):
            lastname = author.find("LastName")
            forename = author.find("ForeName")
            if lastname is not None and forename is not None:
                authors_list.append(f"{forename.text} {lastname.text}")

        authors = ", ".join(authors_list) if authors_list else "N/A"

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Authors": authors,
            "Abstract": abstract
        })

    return papers