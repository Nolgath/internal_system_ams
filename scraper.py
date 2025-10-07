import os
import subprocess

# Ensure Chromium is installed before importing Playwright
cache_path = os.path.expanduser("~/.cache/ms-playwright")
chromium_path = os.path.join(cache_path, "chromium_headless_shell-1187")

if not os.path.exists(chromium_path):
    try:
        print("Chromium not found — installing now...")
        subprocess.run(
            ["python", "-m", "playwright", "install", "chromium", "--with-deps"],
            check=True
        )
        print("Chromium installed successfully.")
    except Exception as e:
        print("Playwright install failed:", e)


from playwright.sync_api import sync_playwright
import time

vin = 'KMHKN81AFNU108307'

#WAUZZZF25LN099526


def get_equipment_value(vin):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://ams-de.mega-moves.com/")
        page.fill("input[name=username]", "c.zorila")
        page.fill("input[name=password]", "MemoCristian2025")
        page.click("button[type=submit]")

        page.fill("input[name=FG_Nr]", vin)
        time.sleep(1)
        page.keyboard.press("Enter")

        time.sleep(0.5)
        page.get_by_text(f"{vin}").click()

        value = page.get_attribute("#tradex_equipment", 'value')

        browser.close()
        return value

