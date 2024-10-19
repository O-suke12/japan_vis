import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup

url = "https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson"
geojson = requests.get(url).json()
json_df = pd.DataFrame([i["properties"] for i in geojson["features"]])


url = "https://www.ipss.go.jp/syoushika/tohkei/Data/Relation/1_Future/1_doukou/1-1-A19.htm"
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "html.parser")
rows = soup.find_all("tr")
data = []

for row in rows:
    cells = row.find_all("td")
    if cells:
        prefecture = cells[0].text.strip()

        if (
            (prefecture in json_df["nam_ja"].values)
            | (prefecture in json_df["nam_ja"].str.replace("県", "").values)
            | (prefecture in json_df["nam_ja"].str.replace("都", "").values)
            | (prefecture in json_df["nam_ja"].str.replace("府", "").values)
        ):
            values = [cell.text.strip().replace(",", "") for cell in cells[1:]]

            data.append({"prefecture": prefecture, "values": values})

columns = ["2005", "2010", "2015", "2020", "2025", "2030", "2035"]
values = [d["values"][:-3] for d in data]
values = [list(map(int, v)) for v in values]
df_values = pd.DataFrame(values, columns=columns)
prefectures = [d["prefecture"] for d in data]
df_pref = pd.DataFrame(prefectures, columns=["prefecture"])
df_pop = pd.concat([df_pref, df_values], axis=1)
json_df["nam_ja"] = json_df["nam_ja"].str.replace("県", "").str.replace("府", "")
json_df["nam_ja"] = json_df["nam_ja"].apply(
    lambda x: x.replace("都", "") if x == "東京都" else x
)
pop_ratio_df = pd.merge(
    json_df, df_pop, left_on="nam_ja", right_on="prefecture", how="inner"
)
for year in ["2010", "2015", "2020", "2025", "2030", "2035"]:
    pop_ratio_df[f"ratio_{year}_2005"] = pop_ratio_df[year] / pop_ratio_df["2005"]
