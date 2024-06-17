import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_file(url, base_url, folder):
    url_path = urlparse(urljoin(base_url, url)).path
    local_path = os.path.join(folder, url_path.lstrip('/'))
    local_folder = os.path.dirname(local_path)

    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path

def download_assets_from_html(html, base_url, folder='downloads'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(['img', 'link', 'script'])

    for tag in tags:
        if tag.name == 'img' and tag.get('src'):
            url = urljoin(base_url, tag['src'])
        elif tag.name == 'link' and tag.get('href'):
            url = urljoin(base_url, tag['href'])
        elif tag.name == 'script' and tag.get('src'):
            url = urljoin(base_url, tag['src'])
        else:
            continue

        try:
            print(f'Downloading {url}')
            download_file(url, base_url, folder)
        except Exception as e:
            print(f'Failed to download {url}: {e}')

if __name__ == "__main__":
    url = 'https://r.webbsite.com/511663/'
    response = requests.get(url)
    if response.status_code == 200:
        download_assets_from_html(response.text, url)
    else:
        print(f'Failed to retrieve {url}')
