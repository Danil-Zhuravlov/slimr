import requests
from typing import Dict, Optional
import streamlit as st

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def upload_and_process_csv(self, file: str) -> Optional[Dict]:
        """
        Upload CSV file to the backend
        
        Args:
            file: File uploaded in Streamlit
            
        Returns:
            Dict with processed data or None if error
        """
        try:
            files = {'file': (file.name, file.getvalue(), 'text/csv')}
            response = requests.post(f"{self.base_url}/api/upload-csv", files=files)

            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error processing file: {response.text}")
                return None
        
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")
            return None
