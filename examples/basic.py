import gradio as gr

gradio_app = gr.load_chat(
    "http://ollama.mamun.wtf/v1/", model="llama3.2:3b", token="ollama"
)

gradio_app.launch(share=False)
