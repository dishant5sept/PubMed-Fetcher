# PubMed Fetcher

## 📌 Project Overview
This project is a command-line tool that fetches research papers from PubMed based on a search query. The results are saved as a CSV file or displayed in the terminal.

---

## 🚀 Features
- Fetches paper IDs from PubMed using the **Entrez API**
- Saves the results in a **CSV file**
- Supports **debug mode** for troubleshooting

---

## 🛠️ Installation & Setup
### **1️⃣ Install Required Libraries**
The project requires the following Python packages:
- `requests` → For making API calls to PubMed
- `pandas` → For handling tabular data
- `typer` → For building the CLI

### **💻 Installing Dependencies**
#### **✅ In Jupyter Notebook:**
```python
!pip install requests pandas typer
```
_or_
```python
%pip install requests pandas typer
```

#### **✅ In VSCode or Mac Terminal:**
```sh
pip install requests pandas typer
```
_or_
```sh
python3 -m pip install requests pandas typer
```

#### **🚨 Fixing Pip Issues (If Any)**
If you see an error like:
```
A new release of pip is available: 24.2 -> 25.0.1
```
Then run:
```sh
python3 -m pip install --upgrade pip
```
Then retry installing dependencies.

---

## 🔧 How to Use
### **CLI Usage (Command Line / Terminal)**
Run the following command:
```sh
python cli.py get-papers "your query" --file output.csv --debug
```
Example:
```sh
python cli.py get-papers "machine learning" --file papers.csv --debug
```
This fetches PubMed papers related to "machine learning" and saves them in `papers.csv`.

### **Jupyter Notebook Usage**
Since running CLI-based scripts in Jupyter Notebook can be tricky, you can execute Python functions directly instead:
```python
from pubmed import fetch_papers

query = "machine learning"
papers = fetch_papers(query)
print(papers)
```

---

## 📜 Code Explanation
### **1️⃣ CLI Script: `cli.py`**
```python
import typer
from pubmed import fetch_papers
import pandas as pd
from typing import Optional

app = typer.Typer()

@app.command()
def get_papers(query: str, file: Optional[str] = None, debug: bool = False):
    """Fetch research papers based on a query and save as CSV."""
    papers = fetch_papers(query)

    if debug:
        typer.echo(f"Fetched {len(papers)} papers.")

    if not papers:
        typer.echo("No papers found.")
        return

    df = pd.DataFrame(papers)
    
    if file:
        df.to_csv(file, index=False)
        typer.echo(f"Saved results to {file}.")
    else:
        typer.echo(df.to_string())

if __name__ == "__main__":
    app()
```
### **2️⃣ PubMed API Script: `pubmed.py`**
```python
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
```

---

## ⚠️ Troubleshooting & Fixes
### **1️⃣ CLI Not Working in Jupyter?**
Instead of running:
```sh
python cli.py get-papers "your query"
```
Use:
```python
from pubmed import fetch_papers
print(fetch_papers("your query"))
```

### **2️⃣ "Could not find a version that satisfies the requirement install" Error?**
You likely ran an incorrect command:
```sh
pip install notebook install requests pandas typer
```
🚨 **Fix:** Remove "install" and use:
```sh
pip install requests pandas typer
```

### **3️⃣ Why I Switched from VSCode to Jupyter Notebook?**
I initially started with VSCode but faced issues:
- CLI-based approach required **manual terminal execution**
- Difficult to troubleshoot errors step-by-step
- Jupyter allowed **interactive debugging** and better **data inspection**

So, I switched to Jupyter Notebook to **test functions independently** before integrating into CLI.

---

## 🎯 Final Notes
- ✅ If using **CLI**, execute `cli.py`
- ✅ If using **Jupyter Notebook**, directly import `fetch_papers()`
- ✅ If errors occur, refer to **Troubleshooting** section

---

### **📌 Author: Dishant**
Happy Coding! 🚀
