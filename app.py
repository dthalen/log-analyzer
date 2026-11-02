from flask import Flask, render_template, request
from detector import analyze_log

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():   
    error = ""

    if request.method == "POST":
        request.files["logfile"].save("uploaded.log")
        try:
            with open ("uploaded.log") as f:
                log_lines = f.readlines()
            breaches, brute_force, odd_hours, stats = analyze_log("uploaded.log")

        except UnicodeDecodeError:
            error = "That file could not be read. Please upload a plain-text log file."
            breaches = []
            brute_force = []
            odd_hours = []
            log_lines = []
            stats = {"total": 0, "failed": 0, "breaches": 0}


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
                           stats=stats,
                           error=error)

if __name__ == "__main__":
    app.run(debug=True)