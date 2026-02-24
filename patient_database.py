import json
import os

DB_FILE = "patient_db.json"


def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)


def get_patient(patient_id):
    db = load_db()
    return db.get(patient_id)


def update_patient(patient_id, name, severity):

    db = load_db()

    if patient_id not in db:
        db[patient_id] = {
            "name": name,
            "history": []
        }

    db[patient_id]["name"] = name
    db[patient_id]["history"].append(severity)

    save_db(db)

    return db[patient_id]["history"]
