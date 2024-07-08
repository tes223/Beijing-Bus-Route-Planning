import threading
import subprocess

def run_flask():
    subprocess.run(["python", "backend.py"])

def run_gradio():
    subprocess.run(["python", "frontend.py"])

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    gradio_thread = threading.Thread(target=run_gradio)
    
    flask_thread.start()
    gradio_thread.start()
    
    flask_thread.join()
    gradio_thread.join()