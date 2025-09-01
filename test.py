import csv
import asyncio
import random
from crawl4ai import AsyncWebCrawler

INPUT_CSV = "WOLFPACK_DIGITAL_reviews.csv"
OUTPUT_CSV = "output.csv"

async def search_linkedin(row, crawler):
    name = row.get("FirstName", "") + " " + row.get("LastName", "")
    company = row.get("OrganisationName", "")
    
    if not name.strip():
        print("Skipping empty name")
        return row

    query = f"{name} site:linkedin.com {company}"
    print(f"\nSearching LinkedIn for: {name} ({company})")

    try:
        # Use `crawl` instead of `search`
        results = await crawler.crawl(query)
        linkedin_url = results[0]['link'] if results else "Not found"
        print(f"Found: {linkedin_url}")
        row['LinkedInProfile'] = linkedin_url
    except Exception as e:
        print(f"Error searching {name}: {e}")
        row['LinkedInProfile'] = "Error"

    delay = random.uniform(10, 20)
    print(f"Waiting for {delay:.2f} seconds...")
    await asyncio.sleep(delay)
    return row

async def main():
    # Use headless=False for less CAPTCHA risk
    crawler = AsyncWebCrawler(headless=False)

    # read input CSV
    rows = []
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    updated_rows = []
    for row in rows:
        updated_row = await search_linkedin(row, crawler)
        updated_rows.append(updated_row)

    # save results
    fieldnames = list(updated_rows[0].keys())
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"\n✅ LinkedIn search complete. Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    asyncio.run(main())
