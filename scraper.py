from playwright.sync_api import sync_playwright
import time

def get_equipment_value(vin):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
        )
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
