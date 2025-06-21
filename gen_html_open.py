import os
import tempfile

def gen_html_open(markdown_content):

    # Markdown 内容
    markdown_content = markdown_content.replace("```","",-1)
    # HTML 模板
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Markdown Preview</title>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}
        </style>
    </head>
    <body>
        <div id="markdown-content"></div>
        <script>
            const markdownString = `{markdown_content}`;
            document.getElementById('markdown-content').innerHTML = marked.parse(markdownString);
        </script>
    </body>
    </html>
    """

    # 创建临时 HTML 文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as tmp_file:
        tmp_file.write(html_template)
        tmp_file_path = tmp_file.name

    # 在默认浏览器中打开文件
    os.system(f'open {tmp_file_path}')  # macOS