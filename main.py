import pandas as pd
from googlesearch import search
import time
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI()

# Function to perform Google search for LinkedIn URLs
def get_linkedin_link(company_name):
    try:
        search_query = f"{company_name} official LinkedIn page"
        for result in search(search_query, stop=1):
            if "linkedin.com/company" in result or "linkedin.com/in" in result:
                return result
        return "No LinkedIn URL found"
    except Exception as e:
        return f"Error: {e}"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploaded_{file.filename}"
    
    # Save uploaded file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load Excel file
    df = pd.read_excel(file_location)
    
    # Process each company name
    for index, row in df.iterrows():
        company_name = row.iloc[0]
        linkedin_link = get_linkedin_link(company_name)
        df.at[index, 'LinkedIn URL'] = linkedin_link
        time.sleep(2)

    output_file = "output.xlsx"
    df.to_excel(output_file, index=False)

    return FileResponse(output_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="output.xlsx")
