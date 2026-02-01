from flask import Flask, render_template, request, jsonify
from sheets_service import append_row, append_record_row, get_services, generate_unique_id, get_all_records
from thermal.thermal import TicketPrinter
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    # Serve the form HTML
    return render_template("personal_info_form.html")  # Rename your HTML file to this

@app.route("/qr_code")
def qr_code():
    return render_template("qr_code.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Get form values
    name = request.form.get("name")
    age_range = request.form.get("dob")
    gender = request.form.get("gender")
    height_range = request.form.get("height")
    features = request.form.get("features")

    # Append data to Google Sheets
    id = generate_unique_id([name, age_range, gender, height_range, features])
    append_row([id, name, age_range, gender, height_range, features])

    # Send a simple success message
    return f"""
    <h2>Your response has been recorded.</h2>
    <a href='/'>Back to form</a>
    """

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json

    qr_code = data.get("qr_code")
    service = data.get("service")
    x = datetime.datetime.now()
    date = x.strftime("%x")

    if not qr_code or not service:
        return jsonify({"message": "Missing data"}), 400

    # Write to spreadsheet
    append_record_row([qr_code, service, date])

    return jsonify({
        "message": f"Recorded {service} for {qr_code}"
    })


@app.route("/select-service", methods=["POST"])
def select_service():
    data = request.json
    service_id = data.get("service")

    print("Selected service:", service_id)

    # Store in session, DB, or use immediately
    return jsonify({
        "ok": True,
        "selected_service": service_id
    })

# Add this route to fetch IDs from the Google Sheets
@app.route("/get-services")
def get_services_from_sheet():
    # Fetch the IDs from the Google Sheets API
    services = get_services()
    return jsonify(services)  # Return the list as JSON

@app.route("/get-records")
def get_records_from_sheet():
    # Fetch all records from the Google Sheets API
    records = get_all_records()
    return jsonify(records)

@app.route("/print", methods=["POST"])
def print_custom_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    text = data.get("text", "")
    qr_code = data.get("qr_code")
    newlines = data.get("newlines", 10)

    try:
        newlines = int(newlines)
    except (ValueError, TypeError):
        return jsonify({"error": "newlines must be an integer"}), 400

    tp = TicketPrinter()
    try:
        tp.print_custom(text, qr_code, newlines)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For Raspberry Pi / remote access, use host="0.0.0.0"
    app.run(debug=True, host="0.0.0.0", port=80)
