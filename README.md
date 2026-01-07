# CSVConverter (纯前端版)

这是一个轻量级的 Web 工具，用于将 CSV 文件转换为 Excel (XLSX) 格式，并确保长数字不会丢失精度（强制使用文本格式）。

## 特性

*   **纯前端运行**：利用 JavaScript 在浏览器中完成转换，**文件不上传服务器**，安全隐私。
*   **适配 GitHub Pages**：无需后端，直接部署。
*   **防止精度丢失**：所有单元格强制转换为文本格式，完美解决身份证号、长订单号变成科学计数法的问题。
*   **支持多种编码**：支持 UTF-8, GBK, Latin-1 等编码。

## 使用方法

访问部署好的 GitHub Pages 地址（例如 `https://your-username.github.io/CSVConverter/`），选择 CSV 文件即可转换。

## 开发

本项目使用原生 HTML/JS，依赖以下库（通过 CDN 引入）：
*   [PapaParse](https://www.papaparse.com/): CSV 解析
*   [SheetJS (xlsx)](https://sheetjs.com/): Excel 生成

## 历史版本

原 Python Flask 版本已移动到 `python_backend/` 目录下。如果你需要部署到支持 Python 的服务器，请参考该目录下的文件。
