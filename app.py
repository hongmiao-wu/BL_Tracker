from utils import get_carrier_from_bl
from scraper import getContainerNoFromPDF, msc, evergreen

from flask import Flask, render_template, request, send_file


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

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename:
        file.save(file.filename)
        try:
            container_numbers = getContainerNoFromPDF.extract_container_numbers_from_pdf(file.filename)
            if container_numbers:
                with open(f"{file.filename}-container_info.txt", "w", encoding="utf-8") as f:
                    f.write(f"BL NO: {file.filename}\n")
                    f.write("CTNR:\n")
                    for number in container_numbers:
                        f.write(f"{number}\n")

                #return send_file(f"{file.filename}-container_info.txt", as_attachment=True)
                return send_file(
                    f"{file.filename}-container_info.txt",
                    as_attachment=True,
                    download_name=f"{file.filename}-container_info.txt",  # Flask ≥2.0
                    mimetype="text/plain"
                )
            else:
                return "未在 PDF 中找到集装箱号"
        except Exception as e:
            return f"解析 PDF 时出错：{str(e)}"
    return "未接收到文件"


if __name__ == "__main__":
    import os
    # Render
    # port = int(os.environ.get("PORT", 5000))
    # Railway
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
