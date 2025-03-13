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