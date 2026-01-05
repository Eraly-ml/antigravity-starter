#!/usr/bin/env python3
"""
arXiv MCP Server
================
Provides arXiv paper search and download functionality.

Tools:
- search_papers: Search for papers
- paper_info: Get paper details
- download_paper: Download PDF

Requires: arxiv package (pip install arxiv)
"""

import json
import os
import sys
from typing import Any

try:
    import arxiv
    ARXIV_AVAILABLE = True
except ImportError:
    ARXIV_AVAILABLE = False


def check_arxiv():
    """Check if arxiv is available."""
    if not ARXIV_AVAILABLE:
        return {"error": "arxiv not installed. Run: pip install arxiv"}
    return None


def search_papers(query: str, max_results: int = 10, sort_by: str = "relevance") -> dict:
    """Search for papers on arXiv."""
    err = check_arxiv()
    if err:
        return err
    
    try:
        sort_criterion = {
            "relevance": arxiv.SortCriterion.Relevance,
            "date": arxiv.SortCriterion.SubmittedDate,
            "updated": arxiv.SortCriterion.LastUpdatedDate
        }.get(sort_by, arxiv.SortCriterion.Relevance)
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criterion
        )
        
        papers = []
        for result in search.results():
            papers.append({
                "id": result.entry_id.split("/")[-1],
                "title": result.title,
                "authors": [a.name for a in result.authors[:3]],
                "published": str(result.published.date()) if result.published else None,
                "categories": result.categories,
                "summary": result.summary[:500] + "..." if len(result.summary) > 500 else result.summary,
                "pdf_url": result.pdf_url
            })
        
        return {"papers": papers}
    except Exception as e:
        return {"error": str(e)}


def get_paper_info(paper_id: str) -> dict:
    """Get detailed paper information."""
    err = check_arxiv()
    if err:
        return err
    
    try:
        # Handle both formats: 2301.12345 or full URL
        if "arxiv.org" in paper_id:
            paper_id = paper_id.split("/")[-1]
        
        search = arxiv.Search(id_list=[paper_id])
        results = list(search.results())
        
        if not results:
            return {"error": f"Paper not found: {paper_id}"}
        
        result = results[0]
        return {
            "id": result.entry_id.split("/")[-1],
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "published": str(result.published.date()) if result.published else None,
            "updated": str(result.updated.date()) if result.updated else None,
            "categories": result.categories,
            "primary_category": result.primary_category,
            "summary": result.summary,
            "comment": result.comment,
            "pdf_url": result.pdf_url,
            "doi": result.doi
        }
    except Exception as e:
        return {"error": str(e)}


def download_paper(paper_id: str, path: str = "./papers") -> dict:
    """Download paper PDF."""
    err = check_arxiv()
    if err:
        return err
    
    try:
        if "arxiv.org" in paper_id:
            paper_id = paper_id.split("/")[-1]
        
        search = arxiv.Search(id_list=[paper_id])
        results = list(search.results())
        
        if not results:
            return {"error": f"Paper not found: {paper_id}"}
        
        result = results[0]
        os.makedirs(path, exist_ok=True)
        
        # Clean filename
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in result.title)[:50]
        filename = f"{paper_id}_{safe_title}.pdf"
        filepath = os.path.join(path, filename)
        
        result.download_pdf(dirpath=path, filename=filename)
        
        return {"path": filepath, "title": result.title}
    except Exception as e:
        return {"error": str(e)}


# MCP Server Protocol
TOOLS = {
    "arxiv_search": {
        "description": "Search for papers on arXiv",
        "parameters": {
            "query": {"type": "string", "required": True, "description": "Search query"},
            "max_results": {"type": "integer", "description": "Max results (default 10)"},
            "sort_by": {"type": "string", "description": "relevance, date, or updated"}
        }
    },
    "arxiv_paper_info": {
        "description": "Get detailed paper information",
        "parameters": {
            "paper_id": {"type": "string", "required": True, "description": "arXiv ID (e.g., 2301.12345)"}
        }
    },
    "arxiv_download": {
        "description": "Download paper PDF",
        "parameters": {
            "paper_id": {"type": "string", "required": True},
            "path": {"type": "string", "description": "Download directory"}
        }
    }
}


def handle_request(request: dict) -> dict:
    """Handle incoming MCP request."""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "arxiv_search":
        return search_papers(
            params["query"],
            params.get("max_results", 10),
            params.get("sort_by", "relevance")
        )
    elif method == "arxiv_paper_info":
        return get_paper_info(params["paper_id"])
    elif method == "arxiv_download":
        return download_paper(params["paper_id"], params.get("path", "./papers"))
    else:
        return {"error": f"Unknown method: {method}"}


def main():
    """MCP server main loop."""
    print(json.dumps({"tools": TOOLS}), flush=True)
    
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON"}), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)


if __name__ == "__main__":
    main()
