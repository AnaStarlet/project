import uvicorn
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open("http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    Timer(1.5, open_browser).start()
    uvicorn.run("notes_main:app", host="127.0.0.1", port=8000, reload=True)
