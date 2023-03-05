import pafy
import youtube_dl
import requests
import os
import codecs
import argparse
import ISO3166

dilleer = []
bos = "bos"
vlcOynat = ""
vlcKonum = "\"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe\""
baslik = "\"ZorluYouTubePremium\""
video = None

def icineDisina(dil):
    global dilleer
    uzun = len(dilleer)
    if uzun < 0:
        uzun=0
    dilleer.append(dil)
    try:
        return ISO3166.ISO3166[dil]
    except:
        return dil

def secimIste(sec, url, isim):
    global video
    global bos
    secim = sec
    if secim == -1:
        secim = int(input("1-) Video URL'si ile video izle\n2-) Video adı ile video izle\nSeçiminizi giriniz: "))
    if secim == 1:
        if url == bos:
            video = pafy.new(str(input("YouTube linkini giriniz: ")))
        else:
            video = pafy.new(url)
    elif secim == 2:
        if isim == "":
            video = pafy.new(str(youtube_dl.YoutubeDL({'forceurl': True}).extract_info(("ytsearch:" + str(input("Lütfen video adını girin: "))), False)['entries'][0]['webpage_url']))
        else:
            video = pafy.new(str(youtube_dl.YoutubeDL({'forceurl': True}).extract_info(("ytsearch:" + isim), False)['entries'][0]['webpage_url']))
    else:
        print("Hatalı tuşlama yaptınız!\n")
        secimIste(-1, bos, "")

def cozunurlukIste(coz, otoMu):
    global vlcOynat
    global baslik
    global vlcKonum
    uzunluk = 0
    defDict = dict()
    for s in video.videostreams:
        uzunluk = uzunluk + 1
    for i in range(uzunluk):
        defChars = list(video.videostreams[i].resolution)
        xYeri = 0
        for j in range(len(defChars)-1,-1,-1):
            if defChars[j] == 'x':
                xYeri = j+1
                break
        cozunurluk = ""
        for k in range(xYeri,len(defChars)):
            cozunurluk = cozunurluk + defChars[k]
        defDict[cozunurluk + "p"]= i
    cozunurlukSecimii = -1
    if coz == bos and otoMu == False:
        print("Lütfen video çözünürlüğü seçin: ")
        a = 0
        for m in defDict.keys():
            print(str(a)+": "+m)
            a = a + 1
        cozunurlukSecimi = int(input(""))
        a = 0
        for n in defDict.values():
            if a == cozunurlukSecimi:
                cozunurlukSecimii = n
            a = a + 1
    else:
        try:
            cozunurlukSecimii = defDict[coz]
        except:
            for n in defDict.values():
                cozunurlukSecimii = n
    if cozunurlukSecimii < 0:
        print("Hatalı tuşlama yapıldı.")
        cozunurlukIste(bos, False)
    elif uzunluk > cozunurlukSecimii:
        ses = ""
        if(len(video.audiostreams)-1) >= 0:
            ses = (" --input-slave=\"" + str(video.audiostreams[len(video.audiostreams)-1].url) + "\"")
        vlcOynat = (vlcOynat + vlcKonum + " \"" + str(video.videostreams[cozunurlukSecimii].url) + "\" --meta-title=" + baslik + ses)
    else:
        print("Hatalı tuşlama yapıldı.")
        cozunurlukIste(bos, False)

def altyaziIste(alt, otoMu):
    global vlcOynat
    altyazilar = youtube_dl.YoutubeDL({'forceurl': True, 'writesubtitles': True, 'allsubtitles': True}).extract_info("https://youtu.be/"+str(video.videoid), download = False)
    dilSecimi = 0
    try:
        altyazilarf = altyazilar['requested_subtitles']
        if alt == bos and otoMu == False:
            print("Lütfen altyazı dili seçin: ")
            print("0: Altyazısız izle")
            i=1
            for diller in altyazilarf:
                print(str(i)+": "+str(icineDisina(diller)))
                i = i+1
            dilSecimi = int(input(""))
        else:
            i=1
            for diller in altyazilarf:
                icineDisina(diller)
                if alt == diller:
                    dilSecimi = i
                i = i+1
    except:
        dilSecimi = 0
    if dilSecimi < 0:
        print("Hatalı tuşlama yapıldı.")
        altyaziIste(bos, False)
    elif dilSecimi == 0:
        print("Altyazısız devam edilecek.")
    elif len(dilleer) >= dilSecimi:
        istek = requests.get(str(altyazilar['requested_subtitles'][dilleer[dilSecimi-1]]['url']), stream = True)
        istek.encoding = 'utf-8'
        f1 = codecs.open("altyazi.vtt", "w", "utf-8")
        f1.write(str(istek.text))
        f1.close()
        vlcOynat = (vlcOynat + " --sub-file=\"altyazi.vtt\"")
    else:
        print("Hatalı tuşlama yapıldı.")
        altyaziIste(bos, False)

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--video-url", dest="url", default=bos, help="Video URL'si")
parser.add_argument("-i", "--video-ismi", dest="isim", default="", help="Video ismi")
parser.add_argument("-a", "--alt-dili", dest="alt", default=bos, help="Video altyazisi")
parser.add_argument("-c", "--cozunurluk", dest="coz", default=bos, help="Video cozunurlugu")
degerler = parser.parse_args()
if degerler.url == bos:
    if degerler.isim == "":
        secimIste(-1, degerler.url, degerler.isim)
        cozunurlukIste(degerler.coz, False)
        altyaziIste(degerler.alt, False)
    else:
        secimIste(2, degerler.url, degerler.isim)
        cozunurlukIste(degerler.coz, True)
        altyaziIste(degerler.alt, True)
else:
    secimIste(1, degerler.url, degerler.isim)
    cozunurlukIste(degerler.coz, True)
    altyaziIste(degerler.alt, True)
os.popen(vlcOynat)