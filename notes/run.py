import uvicorn
import webbrowser
from threading import Timer

import uvicorn

if __name__ == "__main__":
    uvicorn.run("notes_main:app", host="127.0.0.1", port=8000, reload=True)