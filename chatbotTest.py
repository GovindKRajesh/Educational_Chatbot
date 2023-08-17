import os
from apikey import apikey
import time
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By

os.environ['OPENAI_API_KEY'] = apikey

openai.api_key = os.getenv("OPENAI_API_KEY")

template = '''
You are Alan, a chatbot tester who is attempting to check how effective a new educational chatbot is. The chatbot is meant to improve the reading comprehension skills of 4th grade students, and asks them questions about {topic}.
The bot first provides the student with a passage or story related to {topic}, and then asks a question based on it.
As a tester, you must check the chatbot's question and then give a completely incorrect or irrelevant response.
Aim for a grade of 'incorrect', which means 'Answer is completely incorrect, and shows no understanding of the provided passage.'
'''

topic = "baseball"

standards = '''
- The student must draw evidence from the provided text to support their answer.
- Must apply grade 4 Reading standards to literature (like "Describe in depth a character, setting, or event in a story or drama, drawing on specific details in the text.").
- Must apply grade 4 Reading standards to informational texts (like "Explain how an author uses reasons and evidence to support particular points in a text").
'''

rubric = '''
1. Perfect - Answer completely addresses all the points asked for in the question and shows deep understanding of the passage.
2. Can be better - Answer partially addresses the points asked for, but is missing some information that makes it short of perfect.
3. Not quite - Answer is inaccurate, but still shows some understanding of the provided passage.
4. Incorrect - Answer is completely incorrect, and shows no understanding of the provided passage.
'''

system_message = template.format(topic = topic)

messages = [
    {
    "role": "system",
    "content": system_message
    }
]

def openai_create():

    response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = messages,
    temperature = 0.9,
    max_tokens = 2000,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0
    )

    return response.choices[0].message.content

def update_messages(message, flag):
    if flag == 0:
        role = "user"
    else:
        role = "assistant"
    newMessage = {
        "role": role,
        "content": message
    }
    messages.append(newMessage)

driver = webdriver.Chrome()

url = "http://127.0.0.1:7860"
driver.get(url)

# Find the input element, enter text and then hit submit
input_element = driver.find_element(By.XPATH, "//textarea[@data-testid='textbox']")
text_input = "Hi, let's get started"
input_element.send_keys(text_input)
update_messages(text_input, 0)
submit_button_id = "component-5"
submit_button = driver.find_element(By.ID, submit_button_id)
submit_button.click()
time.sleep(10)

# Read the text from the textbox above the input element
div_element = driver.find_element(By.XPATH, "//div[@data-testid='bot']")
div_text = div_element.text

# Generate a response from the tester bot that should be rated as 'can be better'
update_messages(div_text, 1)
output = openai_create()
#update_messages(output, 0)

# Find the enter response and hit submit
input_element.clear()
input_element.send_keys(output)
submit_button.click()
time.sleep(20)

# Close the browser window
driver.quit()
