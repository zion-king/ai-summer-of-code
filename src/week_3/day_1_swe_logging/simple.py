"""Build a simple LLM application"""

import os, groq
from src.exceptions.operationshandler import system_logger
from dotenv import load_dotenv
load_dotenv()

# Set GRO_API_KEY = "your api key" in the .env file, then load it below
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = groq.Groq(api_key = GROQ_API_KEY)

sys_prompt = """You are a helpful virtual assistant. \
    Your goal is to provide useful and relevant \
        responses to my request"""

models = [
    "llama-3.1-405b-reasoning",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768"
]


def generate(model, query, temperature=0):
    try:
        response = groq_client.chat.completions.create(
            model = model,
            messages = [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": query},
            ],
            response_format = {"type": "text"},
            temperature = temperature
        )

        answer = response.choices[0].message.content

        return answer
    
    except Exception as e:
        system_logger.error(
            f"An error occured where {model} was trying to generate a response",
            # str(e),
            exc_info=1
        )

# if __name__ == "__main__":
#     model = models[2]
#     query = "which is bigger? 9.11 or 9.9?"
#     response = generate(model, query, temperature=1)
#     print(response)

