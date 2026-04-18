
import gradio as gr
from inference import run

history = []

def chat(user_msg, chat_history):
    response = run(user_msg, history)
    history.append({"user": user_msg, "assistant": response})
    chat_history.append((user_msg, response))
    return "", chat_history

with gr.Blocks(title="Pocket Agent") as demo:
    gr.Markdown("## 🤖 Pocket-Agent")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Weather in Karachi / Convert 100km to miles")
    msg.submit(chat, [msg, chatbot], [msg, chatbot])

demo.launch(share=True)
