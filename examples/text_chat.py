import time
import gradio as gr
import openai
from functools import cache


@cache
def get_client():
    print("Creating client")
    client = openai.Client(base_url="http://ollama.mamun.wtf/v1", api_key="ollama")
    return client


def chat_interface(message, history, system_prompt):
    client = get_client()
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="llama3.2:3b", messages=messages, stream=True
    )
    buffer = ""
    for message in response:
        time.sleep(0.05)
        buffer += message.choices[0].delta.content
        yield "AI: " + buffer


with gr.Blocks() as demo:
    system_prompt = gr.Textbox("You are helpful AI.", label="System Prompt")
    gr.ChatInterface(chat_interface, additional_inputs=[system_prompt], type="messages")

demo.launch()
