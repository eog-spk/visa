def fetch_visa_bulletin():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch the page"}

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the section containing the Visa Bulletin tables
    sections = soup.find_all("section", class_="tsg-rwd-table-container")
    
    if not sections:
        return {"error": "No Visa Bulletin data found"}

    visa_bulletin_data = []
    
    for section in sections:
        table = section.find("table")
        if not table:
            continue

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
    
    return visa_bulletin_data if visa_bulletin_data else {"error": "No valid data found"}

@app.get("/visa-bulletin")
def get_visa_bulletin():
    return fetch_visa_bulletin()

@app.get("/")
def home():
    return {"message": "Visa Bulletin API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
