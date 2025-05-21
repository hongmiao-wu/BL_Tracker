from utils import get_carrier_from_bl
from scraper import getContainerNoFromPDF, msc, evergreen
from urllib.parse import quote
from flask import Flask, render_template, request, send_file
import datetime
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bl_number = request.form["bl_number"]
        carrier = get_carrier_from_bl(bl_number)
        
        if carrier == "MSC":
            container_number = msc.get_container_number(bl_number)
        elif carrier == "EVERGREEN":
            container_number = evergreen.get_container_number(bl_number)
        else:
            container_number = "BL No. Not Support"

        with open(f"{bl_number}-container_info.txt", "w", encoding="utf-8") as f:
            f.write(f"BL NO: {bl_number}\n")
            f.write(f"Shipping Company: {carrier}\n")
            f.write("CTNR:\n")
            for number in container_number:
                f.write(f"{number}\n")

        return send_file(f"{bl_number}-container_info.txt", as_attachment=True)
    
    return render_template("index.html")

# 获取当前时间的时间戳，格式为：YYYYMMDD_HHMMSS
def generate_timestamp_filename(filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 将时间戳和原始文件名结合起来
    return f"{timestamp}_{filename}"

def clean_filename(filename):
    # 清理文件名，去除不必要的特殊字符
    return re.sub(r'[^\w\s.-]', '_', filename).strip()

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename:
        # 生成带有时间戳的文件名
        cleaned_filename = clean_filename(file.filename)
        timestamped_filename = generate_timestamp_filename(cleaned_filename)
        
        # 保存文件
        file.save(timestamped_filename)
        try:
            container_numbers = getContainerNoFromPDF.extract_container_numbers_from_pdf(timestamped_filename)
            if container_numbers:
                txt_filename = f"{timestamped_filename}-container_info.txt"
                with open(txt_filename, "w", encoding="utf-8") as f:
                    f.write(f"BL NO: {timestamped_filename}\n")
                    f.write("CTNR:\n")
                    for number in container_numbers:
                        f.write(f"{number}\n")

                # 返回包含时间戳的文件名
                return send_file(
                    txt_filename,
                    as_attachment=True,
                    download_name=quote(txt_filename),  # URL 编码文件名
                    mimetype="text/plain"
                )
            else:
                return "未在 PDF 中找到集装箱号"
        except Exception as e:
            return f"解析 PDF 时出错：{str(e)}"
    return "未接收到文件"

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
