from flask import Flask, request, url_for, redirect, render_template
import urllib2, json, spotipy, sys, praw

app=Flask(__name__)

def getCombinations(tags):
    #This function does not actually return all possible combinations of tags. For our purposes, though, it's good enough.
    combs=[]
    size=len(tags)
    index=0
    while size>0:
        while index<=len(tags)-size:
            new=[]
            for i in range(index,size):
                new.append(tags[i])
            combs.append(new)
            index=index+1
        index=0
        size=size-1
    return combs

def getRecipes(tags):
    yummly = "http://api.yummly.com/v1/api/recipes?_app_id=4a5d0d78&_app_key=818e8b8a15bd453e736c1308a331d7f8&q="
    tags=getCombinations(tags)
    i=0
    results=[]
    while len(results)==0:
        for tag in tags[i]:
            yummly+=tag+"+"
            request = urllib2.urlopen(yummly)
            d=json.loads(request.read())
        for r in d['matches']:
            results.append(r['recipeName']+": "+str(r['totalTimeInSeconds']))
        i=i+1
    return results

#print getRecipes(["of"])

def getSongs(tag):
    sp = spotipy.Spotify()
    tags=tag.split()
    tags=getCombinations(tags)
    results=[]
    i=0
    while len(results)==0:
        src=""
        for tag in tags[i]:
            src=src+tag+"+"
        src=src[:-1]
        songs = sp.search(q='track:' + src, type='track')
        items = songs['tracks']['items']
        j = 0
        results = []
        for item in items:
            track = items[i]
            results.append( track['name'] )
            j = j + 1
        i=i+1
    return results
    
def getHeadlines():
    r = praw.Reddit(user_agent='project-that-uses-a-lot-of-data-to-do-nothing')
    headlines = r.get_subreddit('news').get_new(limit=50)
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

topWords=[]
for i in range(10):
    topWords.append(freq[i][0])
print topWords

recipe = getRecipes(topWords)

print recipe[0]

songs = getSongs(recipe[0].split(':')[0])

print songs
