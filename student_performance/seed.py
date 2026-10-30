"""Fills the students table with 300 sample records (run once)."""
import random
from db import get_conn

random.seed(42)
rows = []
for i in range(300):
    study = round(random.uniform(0, 8), 1)
    att = random.randint(40, 100)
    prev = random.randint(30, 100)
    assign = random.randint(30, 100)
    final = 0.35 * prev + 0.20 * assign + 0.20 * att + 3 * study + random.uniform(-5, 5)
    final = round(max(0, min(100, final)), 1)
    rows.append((f"Student {i+1}", study, att, prev, assign, final))

conn = get_conn()
cur = conn.cursor()
cur.executemany(
    "INSERT INTO students (name, study_hours, attendance, previous_marks, assignment_score, final_marks) "
    "VALUES (%s,%s,%s,%s,%s,%s)", rows)
conn.commit()
print(len(rows), "records inserted")
conn.close()
