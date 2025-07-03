
import requests
import base64

# CONFIGURA ESTOS DATOS
GITHUB_TOKEN = "TU_GITHUB_TOKEN"
REPO_OWNER = "TU_USUARIO"
REPO_NAME = "futbol-predictor-app"
FILE_PATH = "data/matches.csv"  # Ruta dentro del repo
LOCAL_FILE = "data/matches.csv"  # Ruta local

def get_file_sha():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

def upload_file():
    with open(LOCAL_FILE, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")

    sha = get_file_sha()

    data = {
        "message": "update matches.csv",
        "content": content,
        "branch": "main"
    }

    if sha:
        data["sha"] = sha

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        print("✅ Archivo subido exitosamente.")
    else:
        print("❌ Error al subir archivo:", response.json())

if __name__ == "__main__":
    upload_file()
