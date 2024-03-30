from scripts.logger import Logger


def save_data_logs(session, error_dict):
    try:
        with session.begin():
            error = Logger(files=error_dict["filename"], logs=error_dict["errors"])
            session.add(error)
        return {"status": 200}
    except Exception as e:
        print(e)  # Log the exception for debugging purposes
        return {"status": 500}
