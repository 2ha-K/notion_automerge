# main.py
from dotenv import load_dotenv
#from read_database import *: import 所有/其實也可以import class類別
from read_database import get_database_pages

def main():
    load_dotenv()
    pages = get_database_pages()
    for pid, title in pages:
        print(f"Page ID: {pid}\nTitle: {title}\n")

# 這段讓程式可以直接執行也能當模組匯入時不會自動執行
if __name__ == "__main__": # 讓你的程式既可以「當主程式執行」，也可以「當模組被匯入」而不自動執行。
    main()
"""
雙底線變數（dunder = "double underscore"）
全名是：特殊魔術變數（magic variables） 或 特殊方法（magic methods）
# __name__, __init__, __str__ 這些是 Python 的 magic method 或 magic variable
# 格式是 __開頭__結尾，代表特殊用途，建議不要自訂這種名字
"""

