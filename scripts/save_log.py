from logger import Logger
import json
from make_db import db_engine
from datetime import datetime


def save_data_logs(error_dict):
    try:
        session_data = db_engine()
        if session_data["status"] != 200:
            return {"status": 500, "error": "Failed to connect to database."}

        session = session_data["session"]

        meta_json = json.dumps(error_dict["meta"], default=datetime_converter)
        errors_json = json.dumps(error_dict["errors"], default=datetime_converter)

        error = Logger(
            RunID=error_dict["meta"].get("run_id", "N/A"),
            meta=meta_json,
            errors=errors_json,
        )
        session.add(error)
        session.commit()
        session.close()
        print("data saved successfully")
        return {"status": 200}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": 500, "error": str(e)}


def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
