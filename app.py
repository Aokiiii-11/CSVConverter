import os
import tempfile
import uuid
from flask import Flask, render_template, request, send_file, after_this_request
from csv_to_excel import get_reader, write_with_xlsxwriter, write_with_openpyxl

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 限制上传大小为 500MB

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template('index.html', error="请选择一个文件")

        if not file.filename.lower().endswith('.csv'):
            return render_template('index.html', error="仅支持 .csv 文件")

        encoding = request.form.get('encoding', 'utf-8-sig')
        engine = request.form.get('engine', 'xlsxwriter')

        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        try:
            # 保存上传的 CSV
            input_filename = f"{uuid.uuid4()}.csv"
            input_path = os.path.join(temp_dir, input_filename)
            file.save(input_path)

            # 准备输出路径
            output_filename = os.path.splitext(file.filename)[0] + '.xlsx'
            output_path = os.path.join(temp_dir, output_filename)

            # 执行转换
            try:
                # 使用之前的逻辑读取 CSV
                f, reader = get_reader(input_path, encoding, delimiter=None)
                
                # 写入 Excel
                if engine == 'openpyxl':
                    write_with_openpyxl(reader, output_path, "Sheet1")
                else:
                    write_with_xlsxwriter(reader, output_path, "Sheet1")
                
                f.close()
            except Exception as e:
                return render_template('index.html', error=f"转换失败: {str(e)}")

            # 发送文件并在发送后清理
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(input_path)
                    os.remove(output_path)
                    os.rmdir(temp_dir)
                except Exception:
                    pass
                return response

            return send_file(output_path, as_attachment=True, download_name=output_filename)

        except Exception as e:
            return render_template('index.html', error=f"处理出错: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
