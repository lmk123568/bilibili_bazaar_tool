from PyInstaller.utils.hooks import copy_metadata
from PyInstaller.utils.hooks import collect_data_files


# import importlib
# print(importlib.util.find_spec("streamlit"))

datas = [
    (
        "C:\\Users\\24089\\miniconda3\\Lib\\site-packages\\streamlit\\runtime",
        "./streamlit/runtime",
    )
]
datas += copy_metadata("streamlit")
datas += collect_data_files("streamlit")

datas += [(".\\main.py", ".")]
datas += [(".\\bilibili.png", ".")]
