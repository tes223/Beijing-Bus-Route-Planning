import threading
import subprocess
import webbrowser

def run_flask():
    subprocess.run(["python", "./scripts/backend.py"])

def run_gradio():
    subprocess.run(["python", "./scripts/frontend.py"])

def run_browser():
    webbrowser.open("http://127.0.0.1:7860")
    

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    gradio_thread = threading.Thread(target=run_gradio)
    browser_thread = threading.Thread(target=run_browser)
    
    flask_thread.start()
    gradio_thread.start()
    browser_thread.start()
    
    flask_thread.join()
    gradio_thread.join()
    browser_thread.join()