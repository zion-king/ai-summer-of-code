## Simple FastAPI for Q&A LLM System

To activate your virtual environment, run the following commands in your terminal (ideally from your VS Code):

- For venv
```
    # create the virtual environmnet
    python -m venv .venv

    # activate the virtual environmnet

    # Windows
    source .venv/Scripts/activate

    # Linux
    source .venv/bin/activate
```

- For poetry
```
    # create the virtual environmnet
    pip install poetry
    poetry new your_desired_venv_name
    poetry init
    poetry shell
    poetry add your_dependency
```

- For conda (Windows)
```
    # Open command prompt and activate conda base enviroment
    # - skip this step if your Command prompt opens in a base environment, indicated with `(base)` at the start of your command line

    # run this command for Anaconda
    "C:\ProgramData\Anaconda3\Scripts\activate.bat"

    # run this for Miniconda
    "C:\ProgramData\Miniconda3\Scripts\activate.bat"

    # If the above doesn't work, then you probably did User installation of Anaconda or Miniconda
    # - Navigate to the specific path it was installed in, and copy the full path to `activate.bat` file, then run it in your terminal.

    # Now that your command line is in the base environment, create a new virtual environment
    conda create -n your_desired_venv_name python=3.9

    # activate the environment
    conda activate your_desired_venv_name

```

To install all dependencies in your requirements.txt, run the following command in your terminal:

```pip install -r requirements.txt```


To run app.py, run the following command in your terminal:

`uvicorn app:app --host 127.0.0.1 --port 5000 --reload`

You can update the host and port number to any other values you choose

Request body for testing in Postman

```
    {
        "question": "which is bigger? 9.11 or 9.9?",
        "model": "llama-3.1-8b-instant",
        "temperature": 0.2
    }
```

