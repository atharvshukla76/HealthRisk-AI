import os, json, sys
from datetime import datetime
from api_client import HealthRiskAPIClient
def main():
    client = HealthRiskAPIClient("configs/config.yaml")
    timestamp = datetime.now().strftime("%Y%m%d")
    os.makedirs("data/raw", exist_ok=True)

        # 1. Fetch FDA Data
    fda_data = client.fetch_openfda_events(search_query = "patient.drug.medicinalproduct:ASPIRIN", limit = 500)
    with open(f"data/raw/fda_{timestamp}.json", "w") as f:
        json.dump(fda_data, f)

      # 2. Fetch ClinicalTrials Data
    ct_data = client.fetch_clinical_trials(search_query = "heart failure", limit = 100)  
    with open(f"data/raw/ct_{timestamp}.json", "w") as f:
        json.dump(ct_data, f)

if __name__ == "__main__":
    main()