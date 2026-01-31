from flask import Flask, render_template, request, jsonify
from sheets_service import append_row, get_ids  # Make sure 'get_ids' is imported from sheets_service

app = Flask(__name__)

@app.route("/")
def index():
    # Serve the form HTML
    return render_template("personal_info_form.html")  # Rename your HTML file to this

@app.route("/qr_code")
def qr_code():
    return render_template("qr_code_website.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Get form values
    name = request.form.get("name")
    age_range = request.form.get("dob")
    gender = request.form.get("gender")
    height_range = request.form.get("height")
    features = request.form.get("features")

    # Append data to Google Sheets
    append_row([name, age_range, gender, height_range, features])

    # Send a simple success message
    return f"""
    <h2>Your response has been recorded.</h2>
    <a href='/'>Back to form</a>
    """

# Add this route to fetch IDs from the Google Sheets
@app.route("/get-ids")
def get_ids_from_sheet():
    # Fetch the IDs from the Google Sheets API
    ids = get_ids()
    return jsonify(ids)  # Return the list as JSON

if __name__ == "__main__":
    # For Raspberry Pi / remote access, use host="0.0.0.0"
    app.run(debug=True, host="0.0.0.0")
