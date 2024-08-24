import logging, pathlib
from pathlib import Path

current_working_directory = Path.cwd()

def setup_logger(
    logger_name: str,
    log_file: str,
    log_level: int = logging.INFO
) -> logging.Logger:
    
    """
    This function allows the system to create and write log data
    of the system's operations.

    Args:
        logger_name (str): the name of the log file to create
        log_file (str): file path to the log file
        log_level (int): the value of the log type (warn, info, debug)
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    format = logging.Formatter('%(asctime)s - %(name)s- %(levelname)s - %(message)s')
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)

    return logger


def create_folder_and_log_file(
    folder_name: str, 
    file_name: str
) -> pathlib.Path:
    """
    This function creates a folder for logging and a corresponding logfile

    Args:
        folder_name (str): name of the folder
        file_name (str): name of the log file
    """

    new_path = current_working_directory.joinpath(folder_name)
    
    # create folder_path only once if not exist
    new_path.mkdir(exist_ok=True)
    log_file_path = new_path.joinpath(file_name)

    # create file if not exist
    log_file_path.touch()


folder_name = "logs"
log_files_to_create = [
    "system.log",
    "userops.log",
    "llmresponse.log"
]

for file in log_files_to_create:
    create_folder_and_log_file(folder_name, file)


system_logger = setup_logger(__name__, f'{current_working_directory}/logs/system.log') # system logger
userops_logger = setup_logger("userLogger", f'{current_working_directory}/logs/userops.log') # user logger
llmresponse_logger = setup_logger("LLMResponseLogger", f'{current_working_directory}/logs/llmresponse.log') # llm response logger




