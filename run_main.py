import streamlit
 
import streamlit.web.cli as stcli
import os, sys
 
 
def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.normpath(os.path.join(base_path, relative_path))
 
 
if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        get_path("main.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())