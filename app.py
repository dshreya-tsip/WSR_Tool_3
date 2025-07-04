from flask import Flask, request, jsonify, render_template
import csv
import os
from openpyxl import Workbook
import traceback

# Initialize Flask app
wsr_app = Flask(__name__)

# Network path to shared folder
SAVE_PATH = r"\\10.188.103.251\WSR_Reports"
CSV_FILE = os.path.join(SAVE_PATH, "WeeklyStatusReport.csv")
EXCEL_FILE = os.path.join(SAVE_PATH, "WeeklyStatusReport.xlsx")

# Ensure the path exists (will only work if permissions allow)
os.makedirs(SAVE_PATH, exist_ok=True)


@wsr_app.route('/')
def index():
    return render_template('index.html')


@wsr_app.route('/data', methods=['GET'])
def load_data():
    rows = []
    try:
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                rows = [row for row in reader]
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(rows)


@wsr_app.route('/save', methods=['POST'])
def save_data():
    data = request.json.get('tableData')
    header = ["Week Days", "Etria(Activity)", "Solutions(Activity)", "Meeting Summary"]

    try:
        # Confirm SAVE_PATH exists or create it
        if not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH, exist_ok=True)

        # Verify write permission by attempting to write a temp file
        test_file = os.path.join(SAVE_PATH, 'test_write_permission.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)

        # Save as CSV
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

        # Save as Excel
        wb = Workbook()
        ws = wb.active
        ws.append(header)
        for row in data:
            ws.append(row)
        wb.save(EXCEL_FILE)

        return jsonify({'message': f'Data saved successfully to {SAVE_PATH}.'})
    except PermissionError:
        logging.error(f"Permission denied when accessing path: {SAVE_PATH}")
        return jsonify({'error': f"Permission denied: Cannot write to {SAVE_PATH}. Check permissions."}), 500
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    wsr_app.run(host='0.0.0.0', port=5000, debug=True)
