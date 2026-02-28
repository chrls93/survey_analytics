import requests
import zipfile
import os
from pathlib import Path


class DataFetcher:
    def __init__(self, data_dir="data/downloaded"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def download_and_extract(self, url: str) -> None:
        """Download zip file and extract to data_dir."""
        filename = url.split("/")[-1]
        filepath = self.data_dir / filename
        
        # Download
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        # Extract
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(self.data_dir)
