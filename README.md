# CSV 转 Excel 网页工具

这是一个轻量级的 Web 工具，用于将 CSV 文件转换为 Excel (XLSX) 格式，并确保长数字不会丢失精度（强制使用文本格式）。

## 目录结构
- `app.py`: Flask 主程序
- `csv_to_excel.py`: 核心转换逻辑
- `templates/index.html`: 前端页面
- `requirements.txt`: 依赖列表

## 部署步骤

1. **安装 Python 3**
   确保服务器已安装 Python 3.8 或更高版本。

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行服务**
   ```bash
   python app.py
   ```
   默认运行在 `http://0.0.0.0:8000`。

## 生产环境部署建议
在生产环境中，建议使用 `gunicorn` 或 `uwsgi` 来运行 Flask 应用，而不是直接使用 `python app.py`。

示例（使用 gunicorn）：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
