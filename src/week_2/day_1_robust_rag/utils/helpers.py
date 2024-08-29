import os
from werkzeug.utils import secure_filename
from src.exceptions.operationshandler import system_logger


allowed_files = ["txt", "csv", "json", "pdf", "doc", "docx", "pptx"]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_files


def file_checks(files):

    if not files:
        return {
            "detail": "No file found",
            "status_code": 400
        }

    for file in files:
        if not file or file.filename == '':
            return {
                "detail": "No selected file",
                "status_code": 400
            }
        
        if not allowed_file(file.filename):
            print(file.filename)
            return {
                "detail": f"File format not supported. Use any of {allowed_files}",
                "status_code": 415
            }
    
    return {
        "detail": "success",
        "status_code": 200
    }

async def upload_files(files, temp_dir):

    checks = file_checks(files)
    
    if checks["status_code"] == 200:
        try: 
            for file in files:
                filename = secure_filename(file.filename)
                file_path = os.path.join(temp_dir, filename)

                file_obj = await file.read()

                with open(file_path, "wb") as buffer:
                    buffer.write(file_obj)
                
            return {
                "detail": "Upload completed",
                "status_code": 200
            }
    
        except Exception as e:
            message = f"An error occured during upload: {e}"
            system_logger.error(
                message,
                # str(e),
                exc_info=1
            )
            raise UploadError(message)

    return checks


class UploadError(Exception):
    pass

class QueryEngineError(Exception):
    pass

        