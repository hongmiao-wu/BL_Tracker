import pdfplumber
import re

def extract_container_numbers_from_pdf(pdf_path):
    # 打开 PDF 文件
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        
        # 遍历每一页并提取文本
        for page in pdf.pages:
            full_text += page.extract_text()

    # 正则表达式匹配集装箱号
    # 集装箱号一般格式是 4 个字母 + 7 个数字，例如 MAEU1234567
    container_number_pattern = r'\b[A-Z]{4}[0-9]{7}\b'
    container_numbers = re.findall(container_number_pattern, full_text)

    return container_numbers

if __name__ == "__main__":
    # 提供 BL PDF 文件路径
    pdf_path = input("请输入提单的 PDF 文件路径：")
    
    # 从 PDF 中提取集装箱号
    container_numbers = extract_container_numbers_from_pdf(pdf_path)
    
    if container_numbers:
        print("✅ 从 PDF 提单中提取到的集装箱号：")
        for container in container_numbers:
            print(f"- {container}")
    else:
        print("❌ 未从 PDF 中提取到集装箱号。")
