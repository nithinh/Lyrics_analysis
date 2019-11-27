
from bs4 import BeautifulSoup

import requests
import re
import json

import csv
import urllib
from urllib.parse import urlparse,urlunparse,urlencode


def get_song_details(url):
    details = {}
    details["url"] = url
    page = requests.get(url)
    s = BeautifulSoup(page.content,"html.parser")
    lyrics = s.select('pre:is(#lyric-body-text)')
    
    if lyrics and len(lyrics) > 0:
        details['lyrics'] = lyrics[0].get_text().split('\r\n')
    artist = s.find(href=re.compile("artist/"))
    if artist:
        details['artist'] = artist.get_text()
    
    title = s.find(class_="lyric-title")
    if title:
        details["title"] = title.get_text()
    bio = s.find(class_="bio")
    if bio:
        details['bio'] = bio.get_text()
    genre = s.find(href=re.compile("genre/"))
    if genre:
        details['genre'] = genre.get_text()
    style = s.find(href=re.compile("style/"))
    if style:
        details['style'] = style.get_text()
    credits = s.find(class_="lyric-credits")
    if credits:
        details['credits'] = credits.get_text().split('\n')[-4:-1]
    year = s.find(href=re.compile("year/"))
    if year:
        details['year'] = int(year.get_text())
    views = s.find(class_="c-views")
    if views:
        b = views.get_text()
        re.sub(b,'^[0-9]*','')
        details['views'] = b.split()[0]
            
    return details
    

def get_random_song_url():
    random_page = requests.get("https://www.lyrics.com/random.php")
    soup = BeautifulSoup(random_page.content,"html.parser")
    url_content = soup.find(href=re.compile("lyrics.com/lyric"))
    if not url_content:
        return get_random_song_url()
    new_url = url_content['href']
    return new_url
    


def get_lyrics(artist,song_title):
    details = {}
    details['artist'] = artist
    details['title'] = song_title
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"
    details['url'] = url
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip()
        details['lyrics'] = [r for r in (re.split(r'\n|<br/>',lyrics)) if r] 
        return details
    except Exception as e:
        return "Exception occurred \n" +str(e)


def get_artist_url(song,artist):
    artist = re.sub('featuring','&',artist,flags=re.IGNORECASE)
    artist = re.sub('with','&',artist,flags=re.IGNORECASE)
    artists = artist.split('&')
    print(artists)
    a_url = None
    for ar in artists:
        base_url = "https://www.lyrics.com/serp.php?"
        f = { 'st' : ar, 'qtype':'2'}

        artist_search_url = base_url + urlencode(f)
        print(artist_search_url)
        search_page = requests.get(artist_search_url)
        soup = BeautifulSoup(search_page.content,"html.parser")
        name = ar.strip()
        url_content = soup.findAll('a',title=re.compile(name,re.I))
        if url_content:
            for url in url_content:
                if url['title'] == name:
                    a_url = url
                    break
        if a_url:
            break
    if not a_url:
        print("No artist links found")
        return None
    
    artist_path = a_url['href']
    parsed_page_url = urlparse(search_page.url)
    parsed_page_url = parsed_page_url._replace(path=artist_path)
    parsed_page_url = parsed_page_url._replace(query='')
    artist_url = urlunparse(parsed_page_url)
    print(artist_url)
    
    return artist_url
    
def get_song_url(song,artist):
    artist_url = get_artist_url(song,artist)
    if not artist_url:
        return None
    artist_page = requests.get(artist_url)
    soup = BeautifulSoup(artist_page.content,"html.parser")
    url_content = soup.findAll('a',text=re.compile(song,re.I),href=re.compile("lyric"))
    if not url_content:
        return None
    song_page_path = url_content[0]['href']
    parsed_page_url = urlparse(artist_page.url)
    parsed_page_url = parsed_page_url._replace(path=song_page_path)
    song_page_url = urlunparse(parsed_page_url)
    print(song_page_url)
    return song_page_url


downloaded_songs = []
i = 0
with open("songs_list.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        song = row['songs']
        artist = row['artists']
        try:
            song_url = get_song_url(song,artist)
            if(song_url):
                d = get_song_details(song_url)
                downloaded_songs.append(d)
            else:
                d = get_lyrics(artist,song)
                downloaded_songs.append(d)
        except:
            print("lyrics.com didn't work")
            d = get_lyrics(artist,song)
            downloaded_songs.append(d)

        if (i%20 == 0):
            with open("songs.json","w") as outfile:
                print(len(downloaded_songs), " downloaded from ", i)
                json.dump(downloaded_songs,outfile)
                print("Saved to json file")
            
        i+=1
            
            
with open("songs.json","w") as outfile:
    print(len(downloaded_songs), " downloaded from ", i)
    json.dump(downloaded_songs,outfile)
    


        
