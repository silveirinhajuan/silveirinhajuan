import sys
import json
import argparse
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch contributions: HTTP {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    
    # Try finding the contribution items
    # Github updated the structure recently to use <tool-tip> or similar
    # But often still has ContributionCalendar-day
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date = td.get("data-date")
        level = td.get("data-level", "0")
        if date:
            count = 0
            tool_tip = td.get("aria-label") or ""
            if "contribution" in tool_tip:
                try:
                    count_str = tool_tip.split()[0]
                    if count_str == "No":
                        count = 0
                    else:
                        count = int(count_str.replace(",", ""))
                except ValueError:
                    count = 0
            days.append({
                "date": date,
                "level": int(level),
                "count": count
            })
            
    data = {
        "username": username,
        "total_days": len(days),
        "days": days
    }
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch public GitHub contribution graph data.")
    parser.add_argument("--username", required=True, help="GitHub username")
    parser.add_argument("--output", default="data/contributions.json", help="Output JSON path")
    args = parser.parse_args()
    
    contrib_data = fetch_contributions(args.username)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(contrib_data, f, indent=2)
    print(f"Saved contribution data for {args.username} to {args.output}")
