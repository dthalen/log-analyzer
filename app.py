from flask import Flask, render_template, request
from detector import analyze_log

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():   

    if request.method == "POST":
        request.files["logfile"].save("uploaded.log")

        with open ("uploaded.log") as f:
            log_lines = f.readlines()
        breaches, brute_force, odd_hours, stats = analyze_log("uploaded.log")

    else:
        breaches = []
        brute_force = []
        odd_hours = []
        log_lines = []
        stats = {"total": 0, "failed": 0, "breaches": 0}

        
        

    

    return render_template("dashboard.html",
                           breaches=breaches,
                           brute_force=brute_force,
                           odd_hours=odd_hours,
                           log_lines=log_lines,
                           stats=stats)

if __name__ == "__main__":
    app.run(debug=True)