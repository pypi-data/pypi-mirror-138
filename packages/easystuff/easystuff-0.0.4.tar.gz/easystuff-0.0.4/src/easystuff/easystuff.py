import requests, shutil


def download(url, location):
    file = requests.get(url)
    open(location, 'wb').write(file.content)

def copy(file, destination):
    shutil.copy(file, destination)