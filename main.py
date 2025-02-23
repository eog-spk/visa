from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI()

URL = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html"

def fetch_visa_bulletin():
    response = requests.get(URL)
    if response.status_code != 200:
        return {"error": "Failed to fetch the page"}

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        return {"error": "No tables found on the page"}

    visa_bulletin_data = []
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows[1:]:  # Skipping the header row
            columns = row.find_all("td")
            if len(columns) >= 3:
                category = columns[0].text.strip()
                final_action_date = columns[1].text.strip()
                filing_date = columns[2].text.strip()
                
                visa_bulletin_data.append({
                    "category": category,
                    "finalActionDate": final_action_date,
                    "filingDate": filing_date
                })
    
    return visa_bulletin_data

@app.get("/visa-bulletin")
def get_visa_bulletin():
    return fetch_visa_bulletin()

@app.get("/")
def home():
    return {"message": "Visa Bulletin API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
