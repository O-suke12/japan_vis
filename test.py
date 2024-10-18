import requests
from bs4 import BeautifulSoup

# 1. URLの設定
url = "https://www.ipss.go.jp/syoushika/tohkei/Data/Relation/1_Future/1_doukou/1-1-A19.htm"

# 2. ページのHTMLデータを取得
response = requests.get(url)
html = response.content

# 3. BeautifulSoupを使ってHTMLを解析
soup = BeautifulSoup(html, "html.parser")

# 4. ページ上の特定の要素を取得（例: table要素）
tables = soup.find_all("table")  # ページ内の全てのテーブルを取得

# 5. テーブルの内容を表示
for table in tables:
    print(table.prettify())  # テーブルのHTML構造を表示


# BeautifulSoupでパース
soup = BeautifulSoup(html, "html.parser")

# 各行の情報を取得
rows = soup.find_all("tr")
data = []

for row in rows:
    cells = row.find_all("td")
    if cells:
        # 県名を取得
        prefecture = cells[0].text.strip()

        # 数字を取得
        values = [cell.text.strip().replace(",", "") for cell in cells[1:]]

        # データのリストに追加
        data.append({"prefecture": prefecture, "values": values})

# 抽出結果を表示
for entry in data:
    print(entry)
