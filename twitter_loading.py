# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

## Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from rdflib import Graph, URIRef
import sys
import requests
import config
import calendar
import time
def convert_status_to_pi_content_item(status):
    # My code here
    user=status["user"]
##    if status["lang"]=="en"|status["lang"]=="es"|status["lang"]=="ar"|status["lang"]=="ja":
##        language = status["lang"]
##    else:
##        language= "en"
    return { 
        'userid': user["id"],#str(s.user.id), 
        'id': status["id"],#str(s.id), 
        'sourceid':'python-twitter', 
        'contenttype':'text/plain', 
        'language':"en",#s.lang, 
        'content': status["text"].encode("ascii", "ignore"),#s.text, 
        'created': 1000 * getCreatedAtInSeconds(status["created_at"]),
        'reply': (status["in_reply_to_status_id"] == None),
        'forward': False
    }

def getCreatedAtInSeconds(s):
    return calendar.timegm(time.strptime(s, '%a %b %d %H:%M:%S +0000 %Y'))

## Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '577377458-IPUK52EqezklphV5CV7PTtIiMib50s5xivdhTMpY'
ACCESS_SECRET = '6S1yYlqWcw7op7EpvH9XtSn4epVtNpXtentludyBdlfU1'
CONSUMER_KEY = '12CZfNAzj80K0bLnXmXoAhrSw'
CONSUMER_SECRET = 'QDYF30csfdouRxlt9USTifbrOaW7dchZbSIWx1vWckx3l1pMdW'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)

##followers =twitter.followers.list(screen_name="mkp0705")

#initialize a list to hold all the Tweets
alltweets=[]
screen_name = "BarackObama"
#make initial request for most recent tweets (200 is the maximum allowed count)
statuses = twitter.statuses.user_timeline(screen_name = screen_name,count=200,include_rts=True)

#save most recent tweets
alltweets.extend(statuses)

#save the id of the oldest tweet less one
oldest = alltweets[-1]["id"] - 1


#keep grabbing tweets until there are no tweets left to grab
while len(statuses) > 0:
    print "getting tweets before %s" % (oldest)
		
    #all subsiquent requests use the max_id param to prevent duplicates
    statuses = twitter.statuses.user_timeline(screen_name = screen_name,count=200,max_id=oldest,include_rts=True)
		
		#save most recent tweets
    alltweets.extend(statuses)
		
		#update the id of the oldest tweet less one
    oldest = alltweets[-1]["id"] - 1
		
    print "...%s tweets downloaded so far" % (len(alltweets))
##    if len(alltweets)==1399:
##        break

pi_content_items_array = map(convert_status_to_pi_content_item, alltweets)
pi_content_items = { 'contentItems' : pi_content_items_array }

r = requests.post(config.pi_url + '/v2/profile', 
			auth=(config.pi_username, config.pi_password),
			headers = {
                'content-type': 'application/json',
                'accept': 'application/json'
            },
			data=json.dumps(pi_content_items)
		)
print("Profile Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
##print json.loads(r.text)
##print r.text

text_file = open("sample_tweet_feed.txt", "w")
text_file.write(r.text)
text_file.close()

##for status in statuses:
##	print "(%s) %s" % (status["GetCreatedAtInSeconds"], status["text"].encode("ascii", "ignore"))
##print 'followers'+ json.dumps(followers, indent=4)

##following =twitter.friends.list(screen_name="mkp0705")
##print 'following'+ json.dumps(following, indent=4)



###########
##g = Graph();
##g.parse("http://dbpedia.org/resource/Elvis_Presley")
##print len(g)



from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
 PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
SELECT ?link
WHERE { <http://dbpedia.org/resource/Asturias>
            dbpedia-owl:wikiPageExternalLink ?link 
    }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print results


##for result in results["results"]["bindings"]:
##    print result["label"]["value"]




###########Working with loaded r.text from sample_tweet.txt############
file = open('Sample_tweet_feed.txt', 'r')

r= file.read()

tweets= json.loads(r)
values = tweets["tree"]["children"][2]
print ('VALUES')
for item in tweets["tree"]["children"][2]["children"][0]["children"]:
        print item["id"]
print ('BIG 5')
for item in tweets["tree"]["children"][0]["children"][0]["children"]:
    print item["id"]
    for it1 in item["children"]:
        print it1["id"]
    print["\n"]
print ('NEEDS')
for item in tweets["tree"]["children"][1]["children"][0]["children"]:
    print item["id"]
