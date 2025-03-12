from fastapi import FastAPI, Query, HTTPException
import pandas as pd

app = FastAPI()

def check(domain, csv_file="rows.csv"):
    try:
        df = pd.read_csv(csv_file, usecols=["Obfuscated Domain"])
        return domain in set(df["Obfuscated Domain"])
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File '{csv_file}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@app.get("/check-domain")
async def check_domain(domain: str = Query(..., description="The domain to check")):
    result = check(domain)
    return {"domain": domain, "exists": result}