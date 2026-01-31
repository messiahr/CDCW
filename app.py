from flask import Flask, render_template, request
from sheets_service import append_row  # make sure this works

app = Flask(__name__)

@app.route("/")
def index():
    # Serve the form HTML
    return render_template("personal_info_form.html")  # rename your HTML file to this

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

if __name__ == "__main__":
    # For Raspberry Pi / remote access, use host="0.0.0.0"
    app.run(debug=True, host="0.0.0.0")
