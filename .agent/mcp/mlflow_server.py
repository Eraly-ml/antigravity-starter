#!/usr/bin/env python3
"""
MLflow MCP Server
=================
Provides MLflow experiment tracking functionality.

Tools:
- list_experiments: List all experiments
- list_runs: List runs in experiment
- log_metric: Log a metric
- log_params: Log parameters
- create_experiment: Create new experiment
- get_run: Get run details

Requires: mlflow package
"""

import json
import os
import sys
from typing import Any

try:
    import mlflow
    from mlflow.tracking import MlflowClient
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False


def check_mlflow():
    """Check if MLflow is available."""
    if not MLFLOW_AVAILABLE:
        return {"error": "mlflow not installed. Run: pip install mlflow"}
    return None


def get_client():
    """Get MLflow client."""
    return MlflowClient()


def list_experiments_fn() -> dict:
    """List all MLflow experiments."""
    err = check_mlflow()
    if err:
        return err
    
    try:
        client = get_client()
        experiments = client.search_experiments()
        return {
            "experiments": [
                {
                    "id": exp.experiment_id,
                    "name": exp.name,
                    "artifact_location": exp.artifact_location,
                    "lifecycle_stage": exp.lifecycle_stage
                }
                for exp in experiments
            ]
        }
    except Exception as e:
        return {"error": str(e)}


def list_runs_fn(experiment_id: str = None, experiment_name: str = None, max_results: int = 10) -> dict:
    """List runs in an experiment."""
    err = check_mlflow()
    if err:
        return err
    
    try:
        client = get_client()
        
        if experiment_name and not experiment_id:
            exp = client.get_experiment_by_name(experiment_name)
            if exp:
                experiment_id = exp.experiment_id
            else:
                return {"error": f"Experiment not found: {experiment_name}"}
        
        if not experiment_id:
            return {"error": "Either experiment_id or experiment_name required"}
        
        runs = client.search_runs(
            experiment_ids=[experiment_id],
            max_results=max_results,
            order_by=["start_time DESC"]
        )
        
        return {
            "runs": [
                {
                    "run_id": run.info.run_id,
                    "status": run.info.status,
                    "start_time": run.info.start_time,
                    "metrics": dict(run.data.metrics),
                    "params": dict(run.data.params)
                }
                for run in runs
            ]
        }
    except Exception as e:
        return {"error": str(e)}


def create_experiment_fn(name: str, artifact_location: str = None) -> dict:
    """Create a new experiment."""
    err = check_mlflow()
    if err:
        return err
    
    try:
        experiment_id = mlflow.create_experiment(name, artifact_location=artifact_location)
        return {"experiment_id": experiment_id, "name": name}
    except Exception as e:
        return {"error": str(e)}


def start_run_fn(experiment_name: str, run_name: str = None) -> dict:
    """Start a new run."""
    err = check_mlflow()
    if err:
        return err
    
    try:
        mlflow.set_experiment(experiment_name)
        run = mlflow.start_run(run_name=run_name)
        return {"run_id": run.info.run_id, "experiment_name": experiment_name}
    except Exception as e:
        return {"error": str(e)}


def log_metrics_fn(metrics: dict, run_id: str = None) -> dict:
    """Log metrics to a run."""
    err = check_mlflow()
    if err:
        return err
    
    try:
        client = get_client()
        if run_id:
            for key, value in metrics.items():
                client.log_metric(run_id, key, value)
        else:
            mlflow.log_metrics(metrics)
        return {"logged": metrics}
    except Exception as e:
        return {"error": str(e)}


def log_params_fn(params: dict, run_id: str = None) -> dict:
    """Log parameters to a run."""
    err = check_mlflow()
    if err:
        return err
    
    try:
        client = get_client()
        if run_id:
            for key, value in params.items():
                client.log_param(run_id, key, str(value))
        else:
            mlflow.log_params(params)
        return {"logged": params}
    except Exception as e:
        return {"error": str(e)}


def get_run_fn(run_id: str) -> dict:
    """Get run details."""
    err = check_mlflow()
    if err:
        return err
    
    try:
        client = get_client()
        run = client.get_run(run_id)
        return {
            "run_id": run.info.run_id,
            "experiment_id": run.info.experiment_id,
            "status": run.info.status,
            "start_time": run.info.start_time,
            "end_time": run.info.end_time,
            "metrics": dict(run.data.metrics),
            "params": dict(run.data.params),
            "tags": dict(run.data.tags)
        }
    except Exception as e:
        return {"error": str(e)}


# MCP Server Protocol
TOOLS = {
    "mlflow_list_experiments": {
        "description": "List all MLflow experiments",
        "parameters": {}
    },
    "mlflow_list_runs": {
        "description": "List runs in an experiment",
        "parameters": {
            "experiment_id": {"type": "string"},
            "experiment_name": {"type": "string"},
            "max_results": {"type": "integer"}
        }
    },
    "mlflow_create_experiment": {
        "description": "Create a new experiment",
        "parameters": {
            "name": {"type": "string", "required": True},
            "artifact_location": {"type": "string"}
        }
    },
    "mlflow_start_run": {
        "description": "Start a new tracking run",
        "parameters": {
            "experiment_name": {"type": "string", "required": True},
            "run_name": {"type": "string"}
        }
    },
    "mlflow_log_metrics": {
        "description": "Log metrics to current or specified run",
        "parameters": {
            "metrics": {"type": "object", "required": True, "description": "Dict of metric_name: value"},
            "run_id": {"type": "string"}
        }
    },
    "mlflow_log_params": {
        "description": "Log parameters to current or specified run",
        "parameters": {
            "params": {"type": "object", "required": True},
            "run_id": {"type": "string"}
        }
    },
    "mlflow_get_run": {
        "description": "Get run details",
        "parameters": {
            "run_id": {"type": "string", "required": True}
        }
    }
}


def handle_request(request: dict) -> dict:
    """Handle incoming MCP request."""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "mlflow_list_experiments":
        return list_experiments_fn()
    elif method == "mlflow_list_runs":
        return list_runs_fn(
            params.get("experiment_id"),
            params.get("experiment_name"),
            params.get("max_results", 10)
        )
    elif method == "mlflow_create_experiment":
        return create_experiment_fn(params["name"], params.get("artifact_location"))
    elif method == "mlflow_start_run":
        return start_run_fn(params["experiment_name"], params.get("run_name"))
    elif method == "mlflow_log_metrics":
        return log_metrics_fn(params["metrics"], params.get("run_id"))
    elif method == "mlflow_log_params":
        return log_params_fn(params["params"], params.get("run_id"))
    elif method == "mlflow_get_run":
        return get_run_fn(params["run_id"])
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
