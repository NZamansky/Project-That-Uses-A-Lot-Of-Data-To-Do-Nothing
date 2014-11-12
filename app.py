# -*- coding: utf-8 -*-

from flask import Flask, request, url_for, redirect, render_template
import urllib2, json, spotipy, sys, praw, random

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

#Gets all the recepes corresponding to a set of tags
def getRecipes(tags):
    yummly = "http://api.yummly.com/v1/api/recipes?_app_id=4a5d0d78&_app_key=818e8b8a15bd453e736c1308a331d7f8&q="
    tags=getCombinations(tags)
    i=0
    results=[]
    while len(results)==0:
        if tags[i] != []: #if tag isn't empty
            for tag in tags[i]:
                yummly+=tag+"+"
                request = urllib2.urlopen(yummly)
                d = json.loads(request.read())#print d
                for r in d['matches']:
                    results.append(r['recipeName'])
                    ##results.append(r['recipeName']+": "+str(r['totalTimeInSeconds']))
        i=i+1
    return results

#Gets the songs corresponding to a certain tags
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
        for item in items:
            track = items[j]
            results.append( track['name'] )
            j = j + 1
        i=i+1
    return results
    
#Gets the top headlines
def getHeadlines():
    r = praw.Reddit(user_agent='project-that-uses-a-lot-of-data-to-do-nothing')
    headlines = r.get_subreddit('news').get_new(limit=50)
    headlines= [str(x) for x in headlines]
    return headlines

#takes all of the words from the top headline
def getWords(headline):
	words = headline.translate(None,"""1234567890,./;'[]\-=`~!@#$%^&*()_+{}|:"<>?""").split()
	freq = {}
	for word in words:
		if word not in freq:
			freq[word]=1
		else:
			freq[word]=freq[word]+1
	final=[]
	for w in sorted(freq, key=freq.get, reverse=True):
		final.append([w,freq[w]])
	common=[]
	for i in range(10):
		common.append(final[i][0])
	return common
   # r = random.randrange( len(words) )
   # result = words[r]
    #return result


<<<<<<< HEAD

headlines = getHeadlines()
r = random.randrange( len(headlines) )
headline = headlines[r]
headline = headline[5:]
#print "headline", headline
newsReel=""
for i in headlines:
	newsReel+=i[5:]+"\n"
print newsReel

words = getWords(newsReel)
print "top",words

recipe = getRecipes(words)
recipe = recipe[0]
print "recipe: ",recipe

song = getSongs(recipe[0].split(':')[0])
#song = song[0]
print "songs: ",song

headline=""
for i in range(len(newsReel)):
	if ord(newsReel[i])>=128:
		newsReel=newsReel[:i]+"?"+newsReel[i+1:]
headline=newsReel.replace('\n','<br>\n')


songs=""
for s in song:
	songs+=s+"<br>"
print songs
#print allTogetherNow()

=======
>>>>>>> 2b5059a0986a1ea740b03814cedc70174859cee5
########## webapp stuff ############

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def base():
<<<<<<< HEAD
    return render_template("home.html",headline=headline, recipe=recipe,songs=songs)
=======
    headlines = getHeadlines()
    r = random.randrange( len(headlines) )
    headline = headlines[r]
    headline = headline[5:]
    print "headline", headline
    
    words = getWords(headline)
    print "top",words
    
    recipe = getRecipes(words)
    recipe = recipe[0]
    print "recipe",recipe
    
    song = getSongs(recipe[0].split(':')[0])
    song = song[0]
    print "song",song
    return render_template("home.html",headline=headline, recipe=recipe,song=song)
>>>>>>> 2b5059a0986a1ea740b03814cedc70174859cee5

if __name__=="__main__":
    app.debug=True
    app.run()
