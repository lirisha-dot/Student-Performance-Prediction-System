import os
from flask import Flask, render_template, request, jsonify
from db import get_conn
import model

app = Flask(__name__)

if not os.path.exists(model.MODEL_FILE):
    model.train()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def api_predict():
    d = request.get_json()
    try:
        name = (d.get("name") or "Unnamed").strip()[:100]
        vals = [float(d["study_hours"]), float(d["attendance"]),
                float(d["previous_marks"]), float(d["assignment_score"])]
    except (KeyError, ValueError, TypeError):
        return jsonify(error="Please fill in all fields with numbers."), 400

    if not (0 <= vals[0] <= 16 and all(0 <= v <= 100 for v in vals[1:])):
        return jsonify(error="Study hours must be 0-16; other values 0-100."), 400

    marks, level = model.predict(vals)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predictions (name, study_hours, attendance, previous_marks, "
        "assignment_score, predicted_marks, predicted_level) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (name, *vals, marks, level))
    conn.commit()
    conn.close()
    return jsonify(marks=marks, level=level)


@app.route("/api/history")
def api_history():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT name, study_hours, attendance, previous_marks, assignment_score, "
                "predicted_marks, predicted_level, created_at "
                "FROM predictions ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        r["created_at"] = r["created_at"].strftime("%d %b %Y, %H:%M")
    return jsonify(rows)


@app.route("/api/metrics")
def api_metrics():
    return jsonify(model.load_models()["metrics"])


@app.route("/api/train", methods=["POST"])
def api_train():
    return jsonify(model.train())


if __name__ == "__main__":
    app.run(debug=True)
