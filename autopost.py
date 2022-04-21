import requests
import json
import base64
import shutil
from time import time, sleep

site="https://test.com"
url = site+"/wp-json/wp/v2"
user = 'root'ss
passwd = "90co A322 xHj7 8Dkj iFxU it8e"
creds = user+":"+passwd
token = base64.b64encode(creds.encode())
headers = {"Authorization":"Basic "+token.decode("utf-8")}
uploadheader = {
     "Authorization":"Basic "+token.decode("utf-8"),
      "Content-Disposition": "form-data",
      'filename': "banner.jpg"
}

youtubekey="API key"
uploadsid="UUr_-h0CAV9l023UZ0vCJZNw"
videos= []

def download(url,fname):
    filename = fname
    d = requests.get(url, stream=True)
    if d.status_code == 200:
        d.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(d.raw, f)

        print('Image successfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retrieved')


def postwp(title,content,time,id):
    post = {
        'date': time,
        'title': title,
        'content': content,
        'status': 'publish',
        'featured_media':id
    }
    r = requests.post(url+'/posts',headers=headers,json=post)
    print("Success")



def wp_media(fname):
    url = site+"/wp-json/wp/v2/media/"
    r = requests.post(url, headers=uploadheader,files = {'file' : open(fname,'rb')})
    return r.json()["id"]


def VideoIDGen(number):
    post = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=" + uploadsid + "&maxResults="+str(number)+"&key="+youtubekey)
    for i in range(number):
        jdata = post.json()
        print(jdata["items"][i]["snippet"]["resourceId"]["videoId"])
        f = open("videoId.txt", "a")
        f.write(jdata["items"][i]["snippet"]["resourceId"]["videoId"]+"\n")
        f.close()


def VideoArry():
    with open("videoId.txt", "r") as f:
        for i in f.readlines():
            videos.append(i.strip("\n"))






def auto(number):
  num =  int(number)
  while True:
    sleep(10)
    print("working ....")
    post = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=" + uploadsid + "&maxResults="+str(num)+"&key="+youtubekey)
    for i in range(num):
        jdata = post.json()
        if(str(jdata["items"][i]["snippet"]["resourceId"]["videoId"]) in videos):
            pass
        else:
            videos.append(str(jdata["items"][i]["snippet"]["resourceId"]["videoId"]))
            title = jdata["items"][i]["snippet"]["title"]
            content = jdata["items"][i]["snippet"]["description"]
            time = jdata["items"][i]["snippet"]["publishedAt"]
            fileurl = jdata["items"][i]["snippet"]["thumbnails"]["maxres"]["url"]
            filename = jdata["items"][i]["snippet"]["resourceId"]["videoId"] + ".jpg"
            download(fileurl, filename)
            id = wp_media(filename)
            postwp(title, content, time, id)



if(__name__=='__main__'):
    while True:
        print("Enter 1 to upload latest videos and goes auto")
        print("Enter 2 to auto upload latest videos when youtube populated")
        a = input("Enter your choice:")
        if(int(a)==1):
            n=input("Number of video you want to post:")
            auto(n)
            del videos
        elif(int(a)==2):
            VideoIDen(5)
            VideoArry()
            auto(5)
