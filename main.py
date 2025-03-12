from fastapi import FastAPI, Query, HTTPException
import pandas as pd
import re


app = FastAPI()

# Load the CSV file into memory when the application starts
try:
    df = pd.read_csv("rows_big.csv", usecols=["Obfuscated Domain"])
    domain_set = set(df["Obfuscated Domain"])  # Convert to a set for O(1) lookups
except FileNotFoundError:
    raise RuntimeError(f"File 'rows_big.csv' not found.")
except Exception as e:
    raise RuntimeError(f"Error loading CSV file: {e}")



def mix_checker(s):
    comma = "."
    swi = 0
    eflag = True
    
    for i in range(len(s)):
        if s[i] != comma:
            if eflag:
                if re.match(r'[^a-zA-Z]', s[i]):
                    swi += 1
                    eflag = False
            else:
                if re.match(r'[^0-9]', s[i]):
                    swi += 1
                    eflag = True
    
    # Calculate the ratio of switches to the length of the string (excluding commas)
    return (swi / (len(s) - 1)) > 0.2


@app.get("/check-domain")
async def check_domain(domain: str = Query(..., description="The domain to check")):
    # Remove the "www." prefix if it exists
    if domain.split(".")[0] == "www":
        domain = ".".join(domain.split(".")[1:])

    print(domain)  # Output: example.com

    # Check if the domain exists in the set
    result = domain in domain_set
    print("result: ", result)
    mixCheck = mix_checker(domain)
    print("mixCheck: ", mixCheck)

    return {"domain": domain, "isUntrusted": result or mixCheck}