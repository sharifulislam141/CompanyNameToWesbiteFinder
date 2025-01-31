import csv
import re
import time
import random
from duckduckgo_search import DDGS

input_file = "companies.txt"
output_file = "results.csv"

def extract_domain(url):
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    return match.group(1) if match else None

def normalize_name(name):
    return re.sub(r'\W+', '', name).lower()

with open(input_file, "r", encoding="utf-8") as file:
    companies = [line.strip() for line in file if line.strip()]

ddgs = DDGS()
results = []

try:
    for company in companies:
        print(f"Searching: {company}...")
        search_results = ddgs.text(company, max_results=10, backend="lite")
        normalized_company = normalize_name(company)
        
        for result in search_results:
            url = result.get("href", "")
            domain = extract_domain(url)
            if domain and normalized_company in normalize_name(domain):
                results.append((company, url))
                print(f"✅ Found: {company} -> {url}")
                break
        
        time.sleep(random.uniform(2, 5))

except KeyboardInterrupt:
    print("\n⏳ Ctrl+C detected! Saving progress before exit...")

except Exception as e:
    print(f"❌ Error occurred: {e}")

finally:
    if results:
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Website"])
            writer.writerows(results)
        print(f"\n📂 Saved {len(results)} results to {output_file}")
    else:
        print("\n⚠ No results found, nothing to save.")

    print("✅ Script exited safely.")
