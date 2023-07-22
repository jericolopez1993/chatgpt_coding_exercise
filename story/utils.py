# importing the openai API
import openai
# import the generated API key from the secret_key file
from .secret_key import API_KEY
# loading the API key from the secret_key file
openai.api_key = API_KEY


def check_status(response):
     status = response['id'] is None
     if status:
          return False
     else:
         return True


def request_from_openai(messages):
    # set the temperature
    temperature = float(0.1)

    max_retries = 3
    retry = 1
    status = None
    response = None
    while status is None or status == False or retry == 3 :
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            max_tokens=1000,
        )
        status = check_status(response)

        if not status:
            retry += 1
            time.sleep(5)

    return response
