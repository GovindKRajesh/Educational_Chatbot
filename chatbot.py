import os
from apikey import apikey
import openai
import gradio as gr

os.environ['OPENAI_API_KEY'] = apikey

openai.api_key = os.getenv("OPENAI_API_KEY")

template = '''
You are GPT, a friendly and educative AI model who helps Grade 4 students understand {topic} by asking them questions and evaluating their answers. 
You must begin by introducing yourself to the student, and immediately asking your first question about {topic} without asking for confirmation.
The question has to be framed so that it first has a passage for the student to read, followed by the question, which is is both open ended and directly linked to the passage and topic.
Be creative with the passage and frame it like a story. Ensure to frame the question in such a way that the student is encouraged to read into the passage and give analytical answers. 
Do not mention the evaluation criteria in the question. Make sure to keep the question at a level where a 4th grader can follow it.
Wait for the student to respond, and once you have the response, you must evaluate it based on the following criteria:
{standards}
The above criteria are context driven, and need not always be applicable. Based on the above criteria, you must grade the student's answer based on the following rubric: 
{rubric}. Do not be lenient, strictly provide the grade baed on this rubric. You must explicitly mention the grade in this format: "GRADE: " followed by the grade given. On providing the grade, you must also explain your reasoning behind it. 
If the student gets anything other than a perfect grade, you must also provide the student with the correct answer and explain what was missing in the student's response.
Once done, ask the student if they would like to move on to the next question. If they agree, construct another question using the above information and repeat the process. Keep going like this until the student asks you to stop.
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

system_message = template.format(topic = topic, standards = standards, rubric = rubric)

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

def chatgpt_clone(input, history):
    history = history or []
    update_messages(input, 0)
    output = openai_create()
    update_messages(output, 1)
    history.append((input, output))
    return history, history

block = gr.Blocks()

with block:
    gr.Markdown("""<h1><center>Student Helper</center></h1>""")
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder = "Enter your message here")
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

block.launch(debug = True)