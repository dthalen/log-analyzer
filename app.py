from flask import Flask, render_template
from detector import analyze_log

app = Flask(__name__)

@app.route("/")
def home():
    breaches, brute_force, odd_hours = analyze_log("auth.log")
    return render_template("dashboard.html",
                           breaches=breaches,
                           brute_force=brute_force,
                           odd_hours=odd_hours)

if __name__ == "__main__":
    app.run(debug=True)