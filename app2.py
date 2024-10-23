import chainlit as cl
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import ChatOpenAI

# general code area 
# - use for functions that are used in multiple places
# - use for variables that are used in multiple places
# - use for running code for all sessions

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Demonstrate how to handle actions

@cl.action_callback("Hide button")
async def on_action(action):
    await cl.Message(content=f"Hiding the button").send()
    await action.remove()

@cl.action_callback("Show text")
async def on_action(action):
    # any processing can be done here
    await cl.Message(content=f"Button clicked has this value: {action.value}").send()

# demonstrate how to change parameters of the LLM through actions

@cl.action_callback("english")
async def on_action(action):
    cl.user_session.set("language", "english")
    await cl.Message(content="Responses from the Chatbot will be in English").send()

@cl.action_callback("icelandic")
async def on_action(action):
    cl.user_session.set("language", "icelandic")
    await cl.Message(content="Responses from the Chatbot will be in Icelandic").send()

# templates for the LLM

user_template = """
        Question:
        {question}

        Language:
        {language}
    """

system_template = """
    You are a helpful assistant who always speaks in a pleasant tone!
    Do your best to answer the question succinctly and truthfully.
    Think through your answers carefully.
    Respond in the language provided below. If no language is provided, use Italian.
""" 

#################################################
### On Chat Start (Session Start) Section     ###
### Use this for pre-session setup processing ###
#################################################
@cl.on_chat_start
async def on_chat_start():
    # create a chain
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", user_template)
    ])
    chat_model = ChatOpenAI(model="gpt-4o-mini")
    simple_chain = chat_prompt | chat_model
    cl.user_session.set("chain", simple_chain)

    response = await cl.AskActionMessage(
        content="Do you want to experiment with buttons?",
        actions=[
            cl.Action(name="yes", value="yes", label="✅ Yes"),
            cl.Action(name="no", value="no", label="❌ No"),
            cl.Action(name="maybe", value="maybe", label="❌ Maybe"),
        ],
    ).send()
    if response and response.get("value") == "yes":
        actions = [
            cl.Action(name="Hide button", value="hide_button", description="Hide this button"),
            cl.Action(name="Show text", value="show_text", description="Show thetext")
        ]

        await cl.Message(content="Different actions", actions=actions).send()
    else: 
        await cl.Message(content="No buttons for you").send()
    
    await cl.Message(content="Lets see how to change the language of the responses from the LLM").send()

    actions = [
        cl.Action(name="english", value="english", description="English"),
        cl.Action(name="icelandic", value="icelandic", description="Icelandic")
    ]

    await cl.Message(content="Languages", actions=actions).send()
    
    await cl.Message(content="Ask the chatbot a question. Then click the Icelandic button and ask again.").send()

#################################################
### On Message Section                        ###
### Use this for processing each user message ###
#################################################   
@cl.on_message
async def main(message: cl.Message):
    # get the session variables
    chain = cl.user_session.get("chain")
    language = cl.user_session.get("language", "english")
    question = message.content

    response = chain.invoke({"question": question, "language": language})
    print(response.content)
    await cl.Message(content=response.content).send()
