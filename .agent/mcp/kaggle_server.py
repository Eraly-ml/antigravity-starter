#!/usr/bin/env python3
"""
Kaggle MCP Server
=================
Provides Kaggle API functionality through MCP protocol.

Tools:
- list_competitions: List active competitions
- competition_info: Get competition details
- submit: Submit to competition
- list_datasets: Search datasets
- download_dataset: Download a dataset

Requires: kaggle package and ~/.kaggle/kaggle.json credentials
"""

import json
import os
import subprocess
import sys
from typing import Any


def run_kaggle_command(args: list[str]) -> dict[str, Any]:
    """Run kaggle CLI command and return parsed output."""
    try:
        result = subprocess.run(
            ["kaggle"] + args,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"output": result.stdout.strip()}
    except FileNotFoundError:
        return {"error": "kaggle CLI not found. Install with: pip install kaggle"}
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out"}


def list_competitions(category: str = None, sort_by: str = "latestDeadline") -> dict:
    """List active Kaggle competitions."""
    args = ["competitions", "list", "--csv"]
    if category:
        args.extend(["--category", category])
    if sort_by:
        args.extend(["--sort-by", sort_by])
    return run_kaggle_command(args)


def competition_info(competition: str) -> dict:
    """Get detailed competition information."""
    args = ["competitions", "list", "--csv", "-s", competition]
    result = run_kaggle_command(args)
    
    # Also get leaderboard info
    lb_args = ["competitions", "leaderboard", competition, "--csv", "--show"]
    lb_result = run_kaggle_command(lb_args)
    
    return {
        "competition": result,
        "leaderboard": lb_result
    }


def submit(competition: str, file_path: str, message: str = "") -> dict:
    """Submit to a competition."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    args = ["competitions", "submit", "-c", competition, "-f", file_path]
    if message:
        args.extend(["-m", message])
    return run_kaggle_command(args)


def list_datasets(search: str = None, sort_by: str = "hottest") -> dict:
    """Search Kaggle datasets."""
    args = ["datasets", "list", "--csv"]
    if search:
        args.extend(["-s", search])
    if sort_by:
        args.extend(["--sort-by", sort_by])
    return run_kaggle_command(args)


def download_dataset(dataset: str, path: str = "./data") -> dict:
    """Download a dataset."""
    os.makedirs(path, exist_ok=True)
    args = ["datasets", "download", "-d", dataset, "-p", path, "--unzip"]
    return run_kaggle_command(args)


def download_competition(competition: str, path: str = "./data") -> dict:
    """Download competition data."""
    os.makedirs(path, exist_ok=True)
    args = ["competitions", "download", "-c", competition, "-p", path]
    return run_kaggle_command(args)


def get_submissions(competition: str) -> dict:
    """Get submission history for a competition."""
    args = ["competitions", "submissions", "-c", competition, "--csv"]
    return run_kaggle_command(args)


# MCP Server Protocol
TOOLS = {
    "kaggle_list_competitions": {
        "description": "List active Kaggle competitions",
        "parameters": {
            "category": {"type": "string", "description": "Filter by category (featured, research, etc)"},
            "sort_by": {"type": "string", "description": "Sort by: latestDeadline, prize, etc"}
        }
    },
    "kaggle_competition_info": {
        "description": "Get competition details and leaderboard",
        "parameters": {
            "competition": {"type": "string", "description": "Competition ID/slug", "required": True}
        }
    },
    "kaggle_submit": {
        "description": "Submit to a Kaggle competition",
        "parameters": {
            "competition": {"type": "string", "required": True},
            "file_path": {"type": "string", "required": True},
            "message": {"type": "string", "description": "Submission message"}
        }
    },
    "kaggle_list_datasets": {
        "description": "Search Kaggle datasets",
        "parameters": {
            "search": {"type": "string"},
            "sort_by": {"type": "string"}
        }
    },
    "kaggle_download_dataset": {
        "description": "Download a dataset",
        "parameters": {
            "dataset": {"type": "string", "required": True, "description": "owner/dataset-name"},
            "path": {"type": "string", "description": "Download path"}
        }
    },
    "kaggle_download_competition": {
        "description": "Download competition data",
        "parameters": {
            "competition": {"type": "string", "required": True},
            "path": {"type": "string"}
        }
    },
    "kaggle_submissions": {
        "description": "Get submission history",
        "parameters": {
            "competition": {"type": "string", "required": True}
        }
    }
}


def handle_request(request: dict) -> dict:
    """Handle incoming MCP request."""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "kaggle_list_competitions":
        return list_competitions(params.get("category"), params.get("sort_by"))
    elif method == "kaggle_competition_info":
        return competition_info(params["competition"])
    elif method == "kaggle_submit":
        return submit(params["competition"], params["file_path"], params.get("message", ""))
    elif method == "kaggle_list_datasets":
        return list_datasets(params.get("search"), params.get("sort_by"))
    elif method == "kaggle_download_dataset":
        return download_dataset(params["dataset"], params.get("path", "./data"))
    elif method == "kaggle_download_competition":
        return download_competition(params["competition"], params.get("path", "./data"))
    elif method == "kaggle_submissions":
        return get_submissions(params["competition"])
    else:
        return {"error": f"Unknown method: {method}"}


def main():
    """MCP server main loop."""
    # Output available tools on startup
    print(json.dumps({"tools": TOOLS}), flush=True)
    
    # Process requests from stdin
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
