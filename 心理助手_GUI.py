import gradio as gr
import subprocess


# 核心AI聊天逻辑（完全复用你原来的ollama调用，不用改）
def chat_with_ai(message, history):
    # 构造ollama请求，保持对话上下文
    prompt = "\n".join([f"用户：{h[0]}\nAI：{h[1]}" for h in history]) + f"\n用户：{message}\nAI："

    # 调用ollama本地模型（qwen2.5:0.5b，和你原来的完全一致）
    process = subprocess.Popen(
        ["ollama", "run", "qwen2.5:0.5b", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )

    # 实时流式输出（解决你之前“没反应”的问题！）
    response = ""
    for line in process.stdout:
        line = line.strip()
        if line:
            response += line
            yield response  # 边生成边显示，像ChatGPT一样！


# 适配Gradio 6.0的界面代码
with gr.Blocks(title="心理陪伴AI") as demo:
    gr.Markdown("# 🧠 心理陪伴AI · 随时陪你聊天")
    gr.Markdown("### 输入你的心事，我会一直在这里听你说～")

    # 新版Chatbot，自动气泡排版，无需旧参数
    chatbot = gr.Chatbot(
        height=600,
        avatar_images=(None, "https://cdn-icons-png.flaticon.com/512/4712/4712109.png")  # AI头像
    )

    # 输入框+发送按钮
    msg = gr.Textbox(label="输入消息", placeholder="在这里输入你想说的话...")
    clear = gr.Button("清空对话")

    # 绑定发送逻辑
    msg.submit(chat_with_ai, [msg, chatbot], [chatbot])
    msg.submit(lambda: "", None, [msg])  # 发送后清空输入框
    clear.click(lambda: None, None, chatbot, queue=False)  # 清空对话

# 启动程序（本地运行，自动打开浏览器，theme放到launch里）
if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        server_name="127.0.0.1",
        server_port=7860,
        theme=gr.themes.Soft()  # 主题放到launch里，适配6.0版本
    )