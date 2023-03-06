"""
`query` command
"""

from typing import List
import click

from mindflow.core.query import run_query

@click.command()
@click.argument("document_paths", type=str, nargs=-1, required=True)
@click.argument("query", type=str, required=True)
# def query(document_paths: List[str], query: str, completion_model: bool, embedding_model: Model):
def query(document_paths: List[str], query: str):
    print(run_query(document_paths, query))