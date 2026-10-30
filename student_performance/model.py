import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score
from db import get_conn

FEATURES = ["study_hours", "attendance", "previous_marks", "assignment_score"]
MODEL_FILE = "model.pkl"


def level_from_marks(m):
    """Convert marks to a performance level (target for the Decision Tree)."""
    if m >= 80: return "Excellent"
    if m >= 65: return "Good"
    if m >= 50: return "Average"
    return "Needs Improvement"


def load_data():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT {', '.join(FEATURES)}, final_marks FROM students")
    data = np.array(cur.fetchall(), dtype=float)
    conn.close()
    return data[:, :-1], data[:, -1]


def train():
    X, y = load_data()
    levels = np.array([level_from_marks(m) for m in y])
    X_tr, X_te, y_tr, y_te, l_tr, l_te = train_test_split(
        X, y, levels, test_size=0.2, random_state=42)

    lr = LinearRegression().fit(X_tr, y_tr)
    dt = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_tr, l_tr)

    metrics = {
        "records": int(len(X)),
        "lr_r2": round(r2_score(y_te, lr.predict(X_te)), 3),
        "lr_mae": round(mean_absolute_error(y_te, lr.predict(X_te)), 2),
        "dt_accuracy": round(accuracy_score(l_te, dt.predict(X_te)), 3),
        "importance": {f: round(float(v), 3) for f, v in zip(FEATURES, dt.feature_importances_)},
    }
    joblib.dump({"lr": lr, "dt": dt, "metrics": metrics}, MODEL_FILE)
    return metrics


def load_models():
    return joblib.load(MODEL_FILE)


def predict(values):
    bundle = load_models()
    x = np.array([values], dtype=float)
    marks = float(np.clip(bundle["lr"].predict(x)[0], 0, 100))
    level = str(bundle["dt"].predict(x)[0])
    return round(marks, 1), level


if __name__ == "__main__":
    print(train())
