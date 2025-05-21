import requests
from bs4 import BeautifulSoup

def get_container_number(bl_number):
    url = "https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do"
    session = requests.Session()
    session.get(url)  # 获取初始 cookie
    bl_trimmed = bl_number[4:]
    payload = {
        "TYPE": "BL",
        "BL": bl_trimmed,
        "CNTR": "",
        "bkno": "",
        "query_bkno": "",
        "query_rvs": "",
        "query_docno": "",
        "query_seq": "",
        "PRINT": "",
        "SEL": "s_bl",
        "NO": bl_trimmed
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": url,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = session.post(url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")

    container_numbers = []
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if columns:
                container_no = columns[0].get_text(strip=True)
                if container_no and container_no[:4].isalpha():
                    container_numbers.append(container_no)

    return container_numbers
