import requests
import os

def download_excel():
    # delete old file if exists
    if os.path.exists("stock_list.xlsx"):
        os.remove("stock_list.xlsx")

    session = requests.Session()
    payload = {
        'username': 'c.zorila',
        'password': 'MemoCristian2025'
    }

    session.post('https://ams-de.mega-moves.com/', data=payload)
    r = session.get('https://ams-de.mega-moves.com/portal/after-sale/pages/list-export-inventory.php?action=bestandsliste')

    with open("stock_list.xlsx", "wb") as f:
        f.write(r.content)

download_excel()