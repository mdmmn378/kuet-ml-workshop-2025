import time
import gradio as gr
import openai
from functools import cache
import os
import json
from functions import tools, REGISTERED_FUNCTIONS


@cache
def get_client():
    print("Creating client")
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "Please set OPENAI_API_KEY environment variable"
    client = openai.Client(api_key=api_key)
    return client


def chat_interface(message, history, system_prompt):
    client = get_client()
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, stream=False,
        tools=tools
    )
    print("Response:", response)
    buffer = ""
    tools_calls = response.choices[0].message.tool_calls

    if not tools_calls:
        for message in response:
            time.sleep(0.05)
            content = message.choices[0].delta.content
            if content:
                buffer += content
                yield "AI: " + buffer
    
    result = str | None
    for tool_call in tools_calls:
        function_name = tool_call.function.name
        arguments = tool_call.function.arguments

        arguments = json.loads(arguments)
        
        if function_name in REGISTERED_FUNCTIONS:
            result = REGISTERED_FUNCTIONS[function_name](**arguments)
        else:
            result = "Sorry, I can't help with that."
    
    result = result.split(" ")
    if result is not None:
        for i, message in enumerate(result):
            buffer += message + " "
            time.sleep(0.05)
            yield "AI: " + buffer



with gr.Blocks() as demo:
    system_prompt = gr.Textbox("You are helpful AI.", label="System Prompt")
    gr.ChatInterface(chat_interface, additional_inputs=[system_prompt], type="messages")

demo.launch()
