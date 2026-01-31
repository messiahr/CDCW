from flask import Flask, render_template, request, redirect, url_for
from sheets_service import append_row

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Append the data to Google Sheets
    append_row([name, email, message])

    # Redirect back to the form with a simple success message
    return f"<h2>Thanks, {name}! Your response has been recorded.</h2><a href='/'>Back to form</a>"

if __name__ == "__main__":
    app.run(debug=True)
