import os
import yaml
import requests
import logging
from typing import Dict, Any, Optional

class HealthRiskAPIClient:
    def __init__(self, config_path: str = "configs/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.fda_config = self.config.get("data_sources", {}).get("openfda", {})
        self.ct_config = self.config.get("data_sources", {}).get("clinicaltrials", {})

    # Notice how this 'def' lines up with the 'def __init__' above it!
    def fetch_openfda_events(self, search_query: str, limit: int = 100) -> Dict[str, Any]:
        """Fetch adverse event data from the OpenFDA API."""
        base_url = self.fda_config.get("base_url", "https://api.fda.gov/drug/event.json")
        response = requests.get(base_url, params={"search": search_query, "limit": limit})
        return response.json()
        
    def fetch_clinical_trials(self, search_query: str, limit: int = 100) -> Dict[str, Any]:
        """Fetch clinical trial data from the ClinicalTrials.gov API."""
        base_url = self.ct_config.get("base_url", "https://clinicaltrials.gov/api/v2/studies")
        response = requests.get(base_url, params={"query.cond": search_query, "pageSize": limit, "format": "json"})
        return response.json()