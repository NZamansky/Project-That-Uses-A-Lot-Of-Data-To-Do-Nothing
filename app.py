from flask import Flask, request, url_for, redirect, render_template
import urllib2, json

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

print getRecipes(["onion","soup"])
