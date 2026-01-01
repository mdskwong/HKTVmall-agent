import openai
import logging
import os
import time
import requests
import json
from dotenv import load_dotenv
from .vision_utils import encode_image, screen_capture

from openai import OpenAI

load_dotenv(override=True)
MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_TYPE = os.getenv('MODEL_TYPE')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')
BASE_URL = os.getenv('OPENAI_BASE_URL')

# add
MODEL_SERVER = os.getenv('MODEL_SERVER')

def get_llm_config(index=None):
    if index == 1:
        return os.getenv('OPENAI_BASE_URL_1'), os.getenv('OPENAI_API_KEY_1'), os.getenv('MODEL_NAME_1')
    elif index == 2:
        return os.getenv('OPENAI_BASE_URL_2'), os.getenv('OPENAI_API_KEY_2'), os.getenv('MODEL_NAME_2')
    elif index == 3:
        return os.getenv('OPENAI_BASE_URL_3'), os.getenv('OPENAI_API_KEY_3'), os.getenv('MODEL_NAME_3')
    elif index == 4:
        return os.getenv('OPENAI_BASE_URL_4'), os.getenv('OPENAI_API_KEY_4'), os.getenv('MODEL_NAME_4')
    else:
        return None, None, None

class OpenAI:
    """
    A class for interacting with the OpenAI API, allowing for chat completion requests.

    This class simplifies the process of sending requests to OpenAI's chat model by providing
    a convenient interface for the chat completion API. It handles setting up the API key
    and organization for the session and provides a method to send chat messages.

    Attributes:
        model_name (str): The name of the model to use for chat completions. Default is set
                          by the global `MODEL_NAME`.
        api_key (str): The API key used for authentication with the OpenAI API. This should
                       be set through the `OPENAI_API_KEY` global variable.
        organization (str): The organization ID for OpenAI. Set this through the
                            `OPENAI_ORGANIZATION` global variable.
    """

    def __init__(self, selected_llm=None):
        """
        Initializes the OpenAI object with the given configuration.
        """
        selected_base_url, selected_api_key, selected_model_name = get_llm_config(selected_llm)

        if selected_base_url:
            self.base_url = selected_base_url
        else:
            self.base_url = BASE_URL

        if selected_api_key:
            self.api_key = selected_api_key
        else:
            self.api_key = OPENAI_API_KEY

        if selected_model_name:
            self.model_name = selected_model_name
        else:
            self.model_name = MODEL_NAME

    def chat(self, messages, temperature=0, prefix=""):
        """
        Sends a chat completion request to the OpenAI API using the specified messages and parameters.

        Args:
            messages (list of dict): A list of message dictionaries, where each dictionary
                                     should contain keys like 'role' and 'content' to
                                     specify the role (e.g., 'system', 'user') and content of
                                     each message.
            temperature (float, optional): Controls randomness in the generation. Lower values
                                           make the model more deterministic. Defaults to 0.

        Returns:
            str: The content of the first message in the response from the OpenAI API.

        """
        try:
            # response = openai.chat.completions.create(
            #     model=self.model_name,
            #     messages=messages,
            #     temperature=temperature
            # )
            client = openai.OpenAI(base_url=self.base_url, api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature
            )
        except Exception as e:
            if "Rate limit exceeded" in str(e):
                time.sleep(61)
                logging.info(f"api call failed: {e}. Retrying in {60} seconds...")
                # response = openai.chat.completions.create(
                #     model=self.model_name,
                #     messages=messages,
                #     temperature=temperature
                # )
                client = openai.OpenAI(base_url=self.base_url, api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature
                )

        if len(prefix) > 0 and prefix[-1] != " ":
            prefix += " "
        logging.info(f"{prefix}Response: {response.choices[0].message.content}")

        return response.choices[0].message.content


class OLLAMA:
    """
    A class for interacting with the OpenAI API, allowing for chat completion requests.

    This class simplifies the process of sending requests to OpenAI's chat model by providing
    a convenient interface for the chat completion API. It handles setting up the API key
    and organization for the session and provides a method to send chat messages.

    Attributes:
        model_name (str): The name of the model to use for chat completions. Default is set
                          by the global `MODEL_NAME`.
        api_key (str): The API key used for authentication with the OpenAI API. This should
                       be set through the `OPENAI_API_KEY` global variable.
        organization (str): The organization ID for OpenAI. Set this through the
                            `OPENAI_ORGANIZATION` global variable.
    """

    def __init__(self):
        """
        Initializes the OpenAI object with the given configuration.
        """

        self.model_name = MODEL_NAME

        self.llama_serve = MODEL_SERVER + "/api/chat"

        self.llama_serve_generate = MODEL_SERVER + "/api/generate"

    def chat(self, messages, temperature=0):
        """
        Sends a chat completion request to the OpenAI API using the specified messages and parameters.

        Args:
            messages (list of dict): A list of message dictionaries, where each dictionary
                                     should contain keys like 'role' and 'content' to
                                     specify the role (e.g., 'system', 'user') and content of
                                     each message.
            temperature (float, optional): Controls randomness in the generation. Lower values
                                           make the model more deterministic. Defaults to 0.

        Returns:
            str: The content of the first message in the response from the OpenAI API.

        """
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
            
        }

        headers = {
                "Content-Type": "application/json"}

        response = requests.post(self.llama_serve, data=json.dumps(payload),headers=headers)

        if response.status_code == 200:
            # Get the response data
            logging.info(f"""Response: {response.json()["message"]["content"]}""")
            return response.json()["message"]["content"]
        else:
            logging.error("Failed to call LLM: ", response.status_code)
            return ""
        
    def generate(self, prompt, images, itemperature=0):
        """
        Sends a generate completion request to the OpenAI API using the specified messages and parameters.

        Args:
            prompt (list of dict): A list of message dictionaries, where each dictionary
                                     should contain keys like 'role' and 'content' to
                                     specify the role (e.g., 'system', 'user') and content of
                                     each message.
            images: (list of str): A list of images in base64 encoded string
            temperature (float, optional): Controls randomness in the generation. Lower values
                                           make the model more deterministic. Defaults to 0.

        Returns:
            str: The response from the response body from the OpenAI API.

        """
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "images": images
            
        }

        headers = {
                "Content-Type": "application/json"}

        response = requests.post(self.llama_serve_generate, data=json.dumps(payload),headers=headers)


        if response.status_code == 200:
            # Get the response data
            logging.info(f"""Response: {response.json()["response"]}""")
            return response.json()["response"]
        else:
            logging.error("Failed to call LLM: ", response.status_code)
            return ""
'''
def main():
    start_time = time.time()
    messages = [{'role': 'system', 'content': 'You are Open Interpreter, a world-class programmer that can complete any goal by executing code.\nFirst, write a plan. **Always recap the plan between each code block** (you have extreme short-term memory loss, so you need to recap the plan between each message block to retain it).\nWhen you execute code, it will be executed **on the user\'s machine**. The user has given you **full and complete permission** to execute any code necessary to complete the task. Execute the code.\nIf you want to send data between programming languages, save the data to a txt or json.\nYou can access the internet. Run **any code** to achieve the goal, and if at first you don\'t succeed, try again and again.\nYou can install new packages.\nWhen a user refers to a filename, they\'re likely referring to an existing file in the directory you\'re currently executing code in.\nWrite messages to the user in Markdown.\nIn general, try to **make plans** with as few steps as possible. As for actually executing code to carry out that plan, for *stateful* languages (like python, javascript, shell, but NOT for html which starts from 0 every time) **it\'s critical not to try to do everything in one code block.** You should try something, print information about it, then continue from there in tiny, informed steps. You will never get it on the first try, and attempting it in one go will often lead to errors you cant see.\nYou are capable of **any** task.\n\n# THE COMPUTER API\n\nA python `computer` module is ALREADY IMPORTED, and can be used for many tasks:\n\n```python\ncomputer.browser.search(query) # Google search results will be returned from this function as a string\ncomputer.files.edit(path_to_file, original_text, replacement_text) # Edit a file\ncomputer.calendar.create_event(title="Meeting", start_date=datetime.datetime.now(), end=datetime.datetime.now() + datetime.timedelta(hours=1), notes="Note", location="") # Creates a calendar event\ncomputer.calendar.get_events(start_date=datetime.date.today(), end_date=None) # Get events between dates. If end_date is None, only gets events for start_date\ncomputer.calendar.delete_event(event_title="Meeting", start_date=datetime.datetime) # Delete a specific event with a matching title and start date, you may need to get use get_events() to find the specific event object first\ncomputer.contacts.get_phone_number("John Doe")\ncomputer.contacts.get_email_address("John Doe")\ncomputer.mail.send("john@email.com", "Meeting Reminder", "Reminder that our meeting is at 3pm today.", ["path/to/attachment.pdf", "path/to/attachment2.pdf"]) # Send an email with a optional attachments\ncomputer.mail.get(4, unread=True) # Returns the {number} of unread emails, or all emails if False is passed\ncomputer.mail.unread_count() # Returns the number of unread emails\ncomputer.sms.send("555-123-4567", "Hello from the computer!") # Send a text message. MUST be a phone number, so use computer.contacts.get_phone_number frequently here\n```\n\nDo not import the computer module, or any of its sub-modules. They are already imported.\n\nUser InfoName: hanchengcheng\nCWD: /Users/hanchengcheng/Documents/official_space/open-interpreter\nSHELL: /bin/bash\nOS: Darwin\nUse ONLY the function you have been provided with — \'execute(language, code)\'.'}, {'role': 'user', 'content': "Plot AAPL and META's normalized stock prices"}]
    # message.append({"role": "user", "content": 'hello'})
    # print(OPENAI_API_KEY)
    # print(BASE_URL)
    llm = OLLAMA()
    response = llm.chat(messages)
    print(response)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"len(response): {len(response)}")
    print(f"execution_time: {execution_time}s")
'''

def main():
    start_time = time.time()
    messages = [{'role': 'system', 'content': 'You are Open Interpreter, a world-class programmer that can complete any goal by executing code.\nFirst, write a plan. **Always recap the plan between each code block** (you have extreme short-term memory loss, so you need to recap the plan between each message block to retain it).\nWhen you execute code, it will be executed **on the user\'s machine**. The user has given you **full and complete permission** to execute any code necessary to complete the task. Execute the code.\nIf you want to send data between programming languages, save the data to a txt or json.\nYou can access the internet. Run **any code** to achieve the goal, and if at first you don\'t succeed, try again and again.\nYou can install new packages.\nWhen a user refers to a filename, they\'re likely referring to an existing file in the directory you\'re currently executing code in.\nWrite messages to the user in Markdown.\nIn general, try to **make plans** with as few steps as possible. As for actually executing code to carry out that plan, for *stateful* languages (like python, javascript, shell, but NOT for html which starts from 0 every time) **it\'s critical not to try to do everything in one code block.** You should try something, print information about it, then continue from there in tiny, informed steps. You will never get it on the first try, and attempting it in one go will often lead to errors you cant see.\nYou are capable of **any** task.\n\n# THE COMPUTER API\n\nA python `computer` module is ALREADY IMPORTED, and can be used for many tasks:\n\n```python\ncomputer.browser.search(query) # Google search results will be returned from this function as a string\ncomputer.files.edit(path_to_file, original_text, replacement_text) # Edit a file\ncomputer.calendar.create_event(title="Meeting", start_date=datetime.datetime.now(), end=datetime.datetime.now() + datetime.timedelta(hours=1), notes="Note", location="") # Creates a calendar event\ncomputer.calendar.get_events(start_date=datetime.date.today(), end_date=None) # Get events between dates. If end_date is None, only gets events for start_date\ncomputer.calendar.delete_event(event_title="Meeting", start_date=datetime.datetime) # Delete a specific event with a matching title and start date, you may need to get use get_events() to find the specific event object first\ncomputer.contacts.get_phone_number("John Doe")\ncomputer.contacts.get_email_address("John Doe")\ncomputer.mail.send("john@email.com", "Meeting Reminder", "Reminder that our meeting is at 3pm today.", ["path/to/attachment.pdf", "path/to/attachment2.pdf"]) # Send an email with a optional attachments\ncomputer.mail.get(4, unread=True) # Returns the {number} of unread emails, or all emails if False is passed\ncomputer.mail.unread_count() # Returns the number of unread emails\ncomputer.sms.send("555-123-4567", "Hello from the computer!") # Send a text message. MUST be a phone number, so use computer.contacts.get_phone_number frequently here\n```\n\nDo not import the computer module, or any of its sub-modules. They are already imported.\n\nUser InfoName: hanchengcheng\nCWD: /Users/hanchengcheng/Documents/official_space/open-interpreter\nSHELL: /bin/bash\nOS: Darwin\nUse ONLY the function you have been provided with — \'execute(language, code)\'.'}, {'role': 'user', 'content': "Plot AAPL and META's normalized stock prices"}]
    #  message = [
     #         {"role": "user", "content": 'hello'},
     #     ]
    print(OPENAI_API_KEY)
    print(BASE_URL)
    llm = OpenAI()
    response = llm.chat(messages)
    print(response)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"len(response): {len(response)}")
    print(f"execution_time: {execution_time}s")

def test_vision():

    save_dir = 'observations'
    os.makedirs(save_dir, exist_ok= True)
    capture_path = screen_capture(save_dir)
    prompt = 'what is in this image?'

    img_ = [encode_image(capture_path)]

    llm = OLLAMA()
    start_time = time.time()
    response = llm.generate(prompt, img_)

    print(response)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"len(response): {len(response)}")
    print(f"execution_time: {execution_time}s")


if __name__ == '__main__':
    #main()
    test_vision()