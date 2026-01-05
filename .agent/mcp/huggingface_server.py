#!/usr/bin/env python3
"""
HuggingFace MCP Server
======================
Provides HuggingFace Hub API functionality through MCP protocol.

Tools:
- search_models: Search for models
- model_info: Get model details
- search_datasets: Search datasets
- dataset_info: Get dataset details
- download_model: Download a model
- download_dataset: Download a dataset

Requires: huggingface_hub package
"""

import json
import sys
from typing import Any

try:
    from huggingface_hub import HfApi, list_models, list_datasets, model_info, dataset_info
    from huggingface_hub import snapshot_download
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False


def check_hf():
    """Check if HuggingFace is available."""
    if not HF_AVAILABLE:
        return {"error": "huggingface_hub not installed. Run: pip install huggingface_hub"}
    return None


def search_models_fn(query: str = None, task: str = None, limit: int = 10) -> dict:
    """Search for models on HuggingFace Hub."""
    err = check_hf()
    if err:
        return err
    
    try:
        models = list(list_models(
            search=query,
            task=task,
            limit=limit,
            sort="downloads",
            direction=-1
        ))
        return {
            "models": [
                {
                    "id": m.id,
                    "downloads": getattr(m, 'downloads', 0),
                    "likes": getattr(m, 'likes', 0),
                    "task": getattr(m, 'pipeline_tag', None)
                }
                for m in models
            ]
        }
    except Exception as e:
        return {"error": str(e)}


def get_model_info(model_id: str) -> dict:
    """Get detailed model information."""
    err = check_hf()
    if err:
        return err
    
    try:
        info = model_info(model_id)
        return {
            "id": info.id,
            "author": info.author,
            "downloads": info.downloads,
            "likes": info.likes,
            "task": info.pipeline_tag,
            "tags": info.tags,
            "library": info.library_name,
            "created": str(info.created_at) if info.created_at else None,
            "modified": str(info.last_modified) if info.last_modified else None
        }
    except Exception as e:
        return {"error": str(e)}


def search_datasets_fn(query: str = None, task: str = None, limit: int = 10) -> dict:
    """Search for datasets on HuggingFace Hub."""
    err = check_hf()
    if err:
        return err
    
    try:
        datasets = list(list_datasets(
            search=query,
            limit=limit,
            sort="downloads",
            direction=-1
        ))
        return {
            "datasets": [
                {
                    "id": d.id,
                    "downloads": getattr(d, 'downloads', 0),
                    "likes": getattr(d, 'likes', 0)
                }
                for d in datasets
            ]
        }
    except Exception as e:
        return {"error": str(e)}


def get_dataset_info(dataset_id: str) -> dict:
    """Get detailed dataset information."""
    err = check_hf()
    if err:
        return err
    
    try:
        info = dataset_info(dataset_id)
        return {
            "id": info.id,
            "author": info.author,
            "downloads": info.downloads,
            "likes": info.likes,
            "tags": info.tags,
            "created": str(info.created_at) if info.created_at else None,
            "modified": str(info.last_modified) if info.last_modified else None
        }
    except Exception as e:
        return {"error": str(e)}


def download_model_fn(model_id: str, path: str = "./models") -> dict:
    """Download a model from HuggingFace Hub."""
    err = check_hf()
    if err:
        return err
    
    try:
        local_path = snapshot_download(
            repo_id=model_id,
            local_dir=f"{path}/{model_id.replace('/', '_')}",
            repo_type="model"
        )
        return {"path": local_path}
    except Exception as e:
        return {"error": str(e)}


def download_dataset_fn(dataset_id: str, path: str = "./datasets") -> dict:
    """Download a dataset from HuggingFace Hub."""
    err = check_hf()
    if err:
        return err
    
    try:
        local_path = snapshot_download(
            repo_id=dataset_id,
            local_dir=f"{path}/{dataset_id.replace('/', '_')}",
            repo_type="dataset"
        )
        return {"path": local_path}
    except Exception as e:
        return {"error": str(e)}


# MCP Server Protocol
TOOLS = {
    "hf_search_models": {
        "description": "Search for models on HuggingFace Hub",
        "parameters": {
            "query": {"type": "string", "description": "Search query"},
            "task": {"type": "string", "description": "Filter by task (text-classification, etc)"},
            "limit": {"type": "integer", "description": "Max results"}
        }
    },
    "hf_model_info": {
        "description": "Get detailed model information",
        "parameters": {
            "model_id": {"type": "string", "required": True, "description": "Model ID (e.g., bert-base-uncased)"}
        }
    },
    "hf_search_datasets": {
        "description": "Search for datasets on HuggingFace Hub",
        "parameters": {
            "query": {"type": "string"},
            "limit": {"type": "integer"}
        }
    },
    "hf_dataset_info": {
        "description": "Get detailed dataset information",
        "parameters": {
            "dataset_id": {"type": "string", "required": True}
        }
    },
    "hf_download_model": {
        "description": "Download a model",
        "parameters": {
            "model_id": {"type": "string", "required": True},
            "path": {"type": "string", "description": "Download path"}
        }
    },
    "hf_download_dataset": {
        "description": "Download a dataset",
        "parameters": {
            "dataset_id": {"type": "string", "required": True},
            "path": {"type": "string"}
        }
    }
}


def handle_request(request: dict) -> dict:
    """Handle incoming MCP request."""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "hf_search_models":
        return search_models_fn(params.get("query"), params.get("task"), params.get("limit", 10))
    elif method == "hf_model_info":
        return get_model_info(params["model_id"])
    elif method == "hf_search_datasets":
        return search_datasets_fn(params.get("query"), params.get("limit", 10))
    elif method == "hf_dataset_info":
        return get_dataset_info(params["dataset_id"])
    elif method == "hf_download_model":
        return download_model_fn(params["model_id"], params.get("path", "./models"))
    elif method == "hf_download_dataset":
        return download_dataset_fn(params["dataset_id"], params.get("path", "./datasets"))
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
