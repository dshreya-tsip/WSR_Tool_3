from flask import Flask, request, jsonify, render_template
import csv
import os

app = Flask(__name__)

# Replace this with your network path:
SAVE_PATH = r"\\10.188.103.251\WeeklyStatusReport"
CSV_FILE = os.path.join(SAVE_PATH, "WeeklyStatusReport.csv")

# Ensure the path exists
os.makedirs(SAVE_PATH, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data", methods=["GET"])
def get_data():
    rows = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip header
            for row in reader:
                rows.append(row)
    return jsonify(rows)


@app.route("/save", methods=["POST"])
def save():
    try:
        data = request.get_json()
        table_data = data.get("tableData", [])
        if not table_data:
            return jsonify({"message": "No data to save."}), 400

        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week Range", "Etria", "Solutions", "Meeting Summary"])
            writer.writerows(table_data)

        return jsonify({"message": "Data saved successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
