import requests
import subprocess
import time

DEFAULT_MODEL = "llama3:8b"
DEFAULT_URL = "http://localhost:11434"

def is_ollama_running(ollama_url=DEFAULT_URL):
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

def start_ollama_server():
    """
    Starts the Ollama server in a new PowerShell window.
    """
    subprocess.Popen(
        ["powershell.exe", "-NoExit", "ollama", "serve"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    print("Starting Ollama server...")

def wait_for_ollama(timeout=30):
    print("Waiting for Ollama to be ready...")
    for _ in range(timeout):
        if is_ollama_running():
            print("Ollama is running.")
            return True
        time.sleep(1)
    print("Ollama did not start in time.")
    return False


def fetch_available_ollama_models(ollama_url=DEFAULT_URL):
    """
    Fetches available Ollama models by querying the /api/tags endpoint and returns a list of model names.
    """
    models_list = []
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            if models:
                for model in models:
                    models_list.append(model.get('name', 'unknown'))
    except Exception:
        pass
    return models_list
