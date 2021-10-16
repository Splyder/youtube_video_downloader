#fais le 16/10/2021 par Splyder en s'inspirant du code de billy

#importation des modules
from requests import get
from os import system, mkdir, name
from os.path import isdir

#definition des fonctions
def get_title(id)->str:
    verify_url="https://www.youtube.com/oembed?format=json&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D" + id
    response=get(verify_url)
    if response.status_code==400:
        return False
    json=response.json()
    return json["title"]

def yt_download(video_url:str,mode:str,default_path:str="Downloads")->bool:
    #mode recoit soit "mp3" soit "mp4"
    
    #recuperation de l'id de la video
    video_id=video_url.split("watch?v=")[-1]
    video_id=video_id.split("&")[0]

    #recuperation du lien de telechargement
    if mode=='mp3':
        download_url="https://www.yt-download.org/api/button/mp3/"+video_id
    elif mode=='mp4':
        download_url="https://www.yt-download.org/api/button/videos/"+video_id

    response=get(download_url).text
    response=response.split('"')
    textures=list(reversed([link for link in response if video_id in link]))

    quality=int(len(textures))
    download_url=textures[quality-1]

    content = get(download_url).content

    #si il n'y a pas de fichier nomme "Downloads", on en cree un
    if not isdir(default_path):
        mkdir(default_path)


    video_title = get_title(video_id)

    if not video_title:
        return False


    for char in ('\\', '/', ':', '*', '?', '"', '<', '>', '|'):
        video_title = video_title.replace(char, '')

    path = default_path+"/"+video_title +"."+mode

    with open(path, 'wb') as f:
        f.write(content)
    
    #on retourne True si la fonction marche
    return True

yt_download("https://www.youtube.com/watch?v=wLoWd2KyUro","mp3")
