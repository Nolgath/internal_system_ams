from flask import Flask, render_template, request, send_file, Response, make_response
from io import BytesIO
import pandas as pd
from equipment_export import equipment_export
from conditionreports import conditionreports
from apscheduler.schedulers.background import BackgroundScheduler
from download_excel import download_excel_stock,download_excel_sales
from kpis import n_of_cars, brands_available, count_p_brand, units_sold, models_available, average_sell_price
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
    model_selected = request.form.get("model", "")

    # if user clicked a model but no brand sent, keep previous brand
    if not brand_selected and model_selected:
        brand_selected = request.cookies.get("brand_selected", "")

    total_cars = n_of_cars()
    brands = brands_available()
    models = models_available(brand_selected) if brand_selected else ""
    brand_count = count_p_brand(model_selected) if model_selected else ""
    units_sold_brand = units_sold(model_selected) if model_selected else ""
    avg_selling_price = average_sell_price(model_selected) if model_selected else ""

    response =  make_response(render_template(
        "index.html",
        total_cars=total_cars,
        brands=brands,
        brand_count=brand_count,
        brand_selected=brand_selected,
        model_selected=model_selected,
        units_sold_brand=units_sold_brand,
        models=models,
        avg_selling_price=avg_selling_price
    ))

    # save the selected brand in a cookie for later POSTs
    if brand_selected:
        response.set_cookie("brand_selected", brand_selected)

    return response

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