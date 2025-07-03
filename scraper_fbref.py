
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_fbref_matches(league_url, output_path="matches.csv"):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(league_url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    table = soup.find("table", {"id": "sched_ks_3232_1"})

    if table is None:
        print("No se encontró la tabla de partidos en la página.")
        return

    rows = table.find_all("tr")
    data = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 10:
            date = row.find("th").text.strip()
            home_team = cells[0].text.strip()
            away_team = cells[1].text.strip()
            score = cells[2].text.strip()
            if score and "-" in score:
                home_goals, away_goals = score.split("-")
                data.append({
                    "MatchDate": date,
                    "HomeTeam": home_team,
                    "AwayTeam": away_team,
                    "FTHome": int(home_goals),
                    "FTAway": int(away_goals),
                    "HomeShots": None,
                    "AwayShots": None,
                    "HomeTarget": None,
                    "AwayTarget": None,
                    "HomeCorners": None,
                    "AwayCorners": None,
                    "HomeYellow": None,
                    "AwayYellow": None,
                    "HomeRed": None,
                    "AwayRed": None
                })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Archivo generado: {output_path}")

# Ejemplo de uso con Premier League (puedes cambiarlo)
if __name__ == "__main__":
    url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"  # Premier League
    scrape_fbref_matches(url)
