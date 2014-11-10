from flask import Flask, request, url_for, redirect, render_template
import urllib2, json, spotipy, sys, praw

app=Flask(__name__)

def getRecipes(tags):
    yummly = "http://api.yummly.com/v1/api/recipes?_app_id=4a5d0d78&_app_key=818e8b8a15bd453e736c1308a331d7f8&q="
    for tag in tags:
        yummly+=tag+"+"
        request = urllib2.urlopen(yummly)
        d=json.loads(request.read())
    results=[]
    for r in d['matches']:
        results.append(r['recipeName']+": "+str(r['totalTimeInSeconds']))
    return results

#print getRecipes(["of"])

def getSongs(tag):
    sp = spotipy.Spotify()
    songs = sp.search(q='track:' + tag, type='track')
    items = songs['tracks']['items']
    i = 0
    results = []
    for item in items:
        track = items[i]
        results.append( track['name'] )
        i = i + 1
    return results
    
#print getSongs("Chicken Caesar Pita")[0]

def getHeadlines():
    r = praw.Reddit(user_agent='project-that-uses-a-lot-of-data-to-do-nothing')
    headlines = r.get_subreddit('news').get_new(limit=10)
    return [str(x) for x in headlines]

headlines =  getHeadlines()

words = {}

for line in headlines:
    w = line.translate(None,"""1234567890,./;'[]\-=`~!@#$%^&*()_+{}|:"<>?""").split(' ')
    for word in w:
        if word not in words:
            words[word]=1
        else:
            words[word]=words[word]+1

# print words
    
freq = []

for w in sorted(words, key=words.get, reverse=True):
    freq.append([w,words[w]])

print freq[0][0]

recipe = getRecipes([freq[0][0]])

print recipe[0]

songs = getSongs(recipe[0].split(':')[0])

print songs
