import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, send_file, jsonify,redirect, url_for, flash
from werkzeug.utils import secure_filename

from translator import PDFTranslator
from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel


app = Flask(__name__)
secret_key = os.urandom(16)  # 生成长度为 16 的随机字符串
TEMP_FILE_DIR = "upload_temps/"

@app.route('/')
def index():
    return '''
    <h1>File Upload</h1>
    <form method="post" action="/translation" enctype="multipart/form-data">
        <input type="file" name="file" />
        <input type="text" name="source_language" value="English">
        <input type="text" name="target_language" value="Chinese">
        <input type="text" name="file_format" value="markdown">
        <input type="submit" value="Upload" />
    </form>
    '''

@app.route('/translation', methods=['POST'])
def translation():
    try:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        upload_file = request.files['file']
        source_language = request.form.get('source_language', 'English')
        target_language = request.form.get('target_language', 'Chinese')
        target_file_format = request.form.get('file_format', 'markdown')

        LOG.debug(f"[upload_file]\n{upload_file}")
        LOG.debug(f"[upload_file.filename]\n{upload_file.filename}")

        if upload_file and upload_file.filename:
            # 创建临时文件
            # 加密文件名
            # filename = secure_filename(file.filename)
            upload_file_path = os.path.join(TEMP_FILE_DIR+file.filename)
            LOG.debug(f"[upload_file_path]\n{upload_file_path}")
            upload_file.save(upload_file_path)
            LOG.debug(f"upload_file successfully")

            # 调用翻译函数
            output_file_path = translator.translate_pdf(
                pdf_file_path=upload_file_path,
                file_format=target_file_format,
                source_language=source_language,
                target_language=target_language)
            
            # 移除临时文件
            # os.remove(upload_file_path)

            # 构造完整的文件路径
            output_file_path = os.getcwd() + "/" + output_file_path
            LOG.debug(output_file_path)

            # 返回翻译后的文件
            return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response), 400

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello world!'
def init_translator():
    # 初始化配置
    config_loader = ConfigLoader('config.yaml')
    config = config_loader.load_config()

    model_name = config['OpenAIModel']['model']
    api_key = config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)

    # 实例化 PDFTranslator 类，全局引用
    global translator
    translator = PDFTranslator(model)

    #flask启用测试
    # pdf_file_path = config['common']['book']
    # file_format = config['common']['file_format']
    # translator.translate_pdf(pdf_file_path, file_format)

if __name__ == "__main__":
    # 初始化 translator
    init_translator()
    # 启动 Flask Web Server
    app.run(host="0.0.0.0", port=5001, debug=True)
