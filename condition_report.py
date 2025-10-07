from playwright.sync_api import sync_playwright
import time
from zipfile import ZipFile
import os

USERNAME = 'c.zorila'
PASSWORD = 'MemoCristian2025'

def get_condition_report(vins):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        # --- LOGIN ---
        page.goto("https://ams-de.mega-moves.com/")
        page.fill("input[name=username]", USERNAME)
        page.fill("input[name=password]", PASSWORD)
        page.click("button[type=submit]")

        pdf_files = []

        for vin in vins:
            time.sleep(1)
            page.goto("https://ams-de.mega-moves.com/portal/vehicles/start.php")
            # --- SEARCH VIN ---
            page.fill("input[name=FG_Nr]", vin)
            time.sleep(0.5)
            page.keyboard.press("Enter")
            page.get_by_text(f"{vin}").click()
            # --- OPEN APPRAISAL TAB ---
            page.get_by_text("Image data/Documents").click()
            page.locator("li.TabbedPanelsTab", has_text="Appraisal").click()
            # --- WAIT & GET LINK ---
            page.wait_for_selector(".TabbedPanelsContentVisible a")
            link = page.locator(".TabbedPanelsContentVisible a").first
            href = link.get_attribute("href")
            pdf_url = f"https://ams-de.mega-moves.com/{href}"
            # --- DOWNLOAD PDF USING AUTHENTICATED REQUEST ---
            response = context.request.get(pdf_url)
            if response.ok:
                pdf_bytes = response.body()
                with open(f"{vin}.pdf", "wb") as f:
                    f.write(pdf_bytes)
                pdf_files.append(f"{vin}.pdf")

        #zip files
        if pdf_files:
            zip_name = 'ConditionReports.zip'
            with ZipFile(zip_name, 'w') as zipf:
                for pdf in pdf_files:
                    zipf.write(pdf)

            for pdf in pdf_files:
                os.remove(pdf)

        browser.close()

# vins = [
#     'KMHKN81AFNU108307','VR3F4DGY8RY544759'
# ]