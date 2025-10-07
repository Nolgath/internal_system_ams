from flask import Flask, render_template, request, send_file
from io import BytesIO
import pandas as pd
from scraper import get_equipment_value
from condition_report import get_condition_report
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    results_text = ""
    table_data = []
    if request.method == "POST":
        # Always read the textarea content
        user_input = request.form.get("user_input", "")
        vins = [v.strip() for v in user_input.splitlines() if v.strip()]
        for vin in vins:
            value = get_equipment_value(vin)
            table_data.append({"VIN": vin, "Equipment": value})
        #  Convert to DataFrame
        df = pd.DataFrame(table_data)
        #  Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Data")
        output.seek(0)
        # Send file for download
        return send_file(
            output,
            as_attachment=True,
            download_name="textarea_data.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    return render_template("index.html", results=results_text)

@app.route('/condition_report', methods=['GET','POST'])
def condition_report():
    if request.method == 'POST':
        user_input = request.form.get("user_input", "")
        vins = [v.strip() for v in user_input.splitlines() if v.strip()] #uses vins pasted and converts in list

        get_condition_report(vins)

        #sending zip file to user
        zip_path = 'ConditionReports.zip'
        if os.path.exists(zip_path):
            return send_file(
                zip_path,
                as_attachment=True,
                download_name="ConditionReports.zip",
                mimetype="application/zip"
            )
        else:
            return "No condition reports found."

    return render_template('condition_report_m.html')



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)