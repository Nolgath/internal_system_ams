from flask import Flask, render_template, request, send_file
from io import BytesIO
import pandas as pd
from scraper import get_equipment_value

app = Flask(__name__)

@app.route("/health")
def health():
    return "OK", 200

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

        # Show results on screen
        results_text = "\n".join(f"{r['VIN']} | {r['Equipment']}" for r in table_data)

        # ✅ Convert to DataFrame
        df = pd.DataFrame(table_data)

        # ✅ Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Data")

        output.seek(0)

        # ✅ Send file for download
        return send_file(
            output,
            as_attachment=True,
            download_name="textarea_data.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    return render_template("index.html", results=results_text)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)