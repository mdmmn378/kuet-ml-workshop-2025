import gradio as gr

gr.load_chat("http://ollama.mamun.wtf/v1/", model="llama3.2", token="ollama").launch()
