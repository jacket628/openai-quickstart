import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from translator import PDFTranslator
from model import GLMModel, OpenAIModel

def translation(input_file, file_format, source_language, target_language):
    LOG.debug(f"AI Translator Input filename: {input_file.name} Source: {source_language} Target: {target_language}")

    output_file_path = translator.translate_pdf(
        pdf_file_path=input_file.name, file_format=file_format,
        source_language=source_language, target_language=target_language)

    return output_file_path

def launch_gradio():
    interface = gr.Interface(
        fn=translation,
        title="AI-Translator v1.0(PDF电子书翻译)",
        description="当前使用OpenAI模型，支持多语种，翻译为PDF和markdown格式",
        inputs=[
            gr.File(label="上传PDF文件"),
            gr.Textbox(label="目标文件格式", placeholder="markdown", value="markdown"),
            gr.Textbox(label="源语言（默认为英文）", placeholder="English", value="English"),
            gr.Textbox(label="目标语言（默认为中文）", placeholder="Chinese", value="Chinese")
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    interface.launch(share=True, server_name="0.0.0.0")

def initialize_translator():
    # 初始化配置
    config_loader = ConfigLoader('config.yaml')
    config = config_loader.load_config()

    model_name = config['OpenAIModel']['model']
    api_key = config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)

    # 实例化 PDFTranslator 类，全局引用
    global translator
    translator = PDFTranslator(model)

if __name__ == "__main__":
    # 初始化 translator
    initialize_translator()
    # 启动 Gradio 服务
    launch_gradio()
