# Educational_Chatbot

# Summary:

This is a project that makes use of OpenAI API to simulate an educational chatbot that teaches 4th grade students about a given topic.

The main file, chatbot.py has the following features:

- It takes the OpenAI API key from an external file, apikey.py.
- A prompt is present, outlining the role and behavior that GPT must follow. This also includes the reading standards to teach/measure, and scoring rubrics for the students' answers. This acts as the initial system message sent to GPT via API. Let's call this instance of GPT as Main Bot.
- It makes use of Gradio's chatbot component for the UI, and this is deployed locally for the prototype. The UI provides the user with chat history as well as a textbox to enter their prompts.
- When the user enters their prompt and hits submit, that prompt is sent along with the chat history to GPT, and the answer from the API is displayed on the chatbot screen.

The chatbotTest.py file is an automated test for the main chatbot.py file. It has the following features:

- This file is meant to be used alongside chatbot.py, and it interacts with the created Gradio web interface via Selenium.
- A prompt is given, used as a system message, explaining to another instance of GPT that it is a tester, who will provide answers to the questions asked by Main Bot. Let's call this test instance of GPT as Test Bot.
- Selenium is used to first start the conversation with the Main Bot, and then it retrieves the response (the question in this case) and feeds it to the Test Bot.
- The Test Bot then generates an answer to the question as per the system message (can be configured to give good or bad answers), and Selenium is once again used to submit that answer to Main Bot.
- Depending on the answer of the Main Bot, we can decide if the Main Bot's assessment was accurate or not (if it matches the settings given within the Test Bot's system message).

Design:

![System Design](https://github.com/GovindKRajesh/Educational_Chatbot/blob/main/Images/System%20Design.png)
