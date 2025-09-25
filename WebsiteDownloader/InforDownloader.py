import requests
import re
import os
import urllib3
from urllib.parse import urljoin


# Ignorera SSL-varningar
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Webfolder och autentiseringsuppgifter
base_url = "https://secure2.infor.com/ftpdownload/updates/2.1_b6_bo/"
username = r'ecommerce\310000h'
password = "Infor2025"

# Lokal mapp för nedladdade filer
download_folder = "DownloadedFiles"
os.makedirs(download_folder, exist_ok=True)

# Headers som simulerar en webbläsare
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}

# Skapa en session
session = requests.Session()
session.auth = (username, password)
session.headers.update(headers)

# Hämta HTML från webfoldern
try:
    response = session.get(base_url, timeout=30, verify=False)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"❌ Kunde inte hämta sidan: {e}")
    exit()

    

# Extrahera filnamn från länkar
file_links = re.findall(r'HREF="([^"?][^"]+)"', response.text)

if not file_links:
    print("⚠️ Inga filer hittades.")
    exit()

# Ladda ner varje fil


for file_name in file_links:
    # Hoppa över länkar som slutar med '/' (dvs mappar)
    if file_name.endswith("/"):
        continue

    file_url = urljoin(base_url, file_name)
    file_name_only = os.path.basename(file_url)
    local_path = os.path.join(download_folder, file_name_only)

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    print(f"⬇️ Laddar ner: {file_url}")
    try:
        file_response = session.get(file_url, timeout=30, verify=False)
        file_response.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(file_response.content)
        print(f"✅ Sparad: {local_path}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Misslyckades att ladda ner: {file_url} ({e})")

