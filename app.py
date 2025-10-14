from flask import Flask, render_template, request, send_file, Response
from io import BytesIO
import pandas as pd
from equipment_export import equipment_export
from conditionreports import conditionreports
from apscheduler.schedulers.background import BackgroundScheduler
from download_excel import download_excel_stock,download_excel_sales
from kpis import n_of_cars, brands_available, count_p_brand, units_sold
import requests
import os

scheduler = BackgroundScheduler()
scheduler.add_job(download_excel_stock, 'cron', hour=6, minute=0)  # runs every day at 06:00
scheduler.add_job(download_excel_sales, 'cron', hour=6, minute=5)  # runs every day at 06:00
scheduler.start()
app = Flask(__name__, template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

@app.route("/", methods=["GET", "POST"])
def home():
    brand_selected = request.form.get("brand", "")
    total_cars = n_of_cars()
    brands = brands_available()
    brand_count = count_p_brand(brand_selected) if brand_selected else ""
    units_sold_brand = units_sold(brand_selected) if brand_selected else ""
    return render_template(
        "index.html",
        total_cars=total_cars,
        brands=brands,
        brand_count=brand_count,
        brand_selected=brand_selected,
        units_sold_brand=units_sold_brand
    )

@app.route("/equipment_export", methods=["GET", "POST"])
def equipment_export_route():
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        vins = [v.strip() for v in user_input.splitlines() if v.strip()]
        # Call function and get Excel file
        excel_file = equipment_export(vins)
        # Send it to the user for download
        return send_file(
            excel_file,
            as_attachment=True,
            download_name="equipment_export.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    return render_template("equipment_export.html")

@app.route('/condition_report', methods=['GET','POST'])
def condition_report():
    if request.method == 'POST':
        user_input = request.form.get("user_input", "")
        vins = [v.strip() for v in user_input.splitlines() if v.strip()]

        conditionreports(vins)
        # sending zip file to user
        zip_path = 'ConditionReports.zip'
        if os.path.exists(zip_path):
            return send_file(
                zip_path,
                as_attachment=True,
                download_name="ConditionReports.zip",
                mimetype="application/zip"
            )
    return render_template('condition_reports.html')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)