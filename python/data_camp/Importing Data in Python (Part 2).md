# 1. Importing data from the Internet
## 1.1 Importing flat files from the web

```python
from urllib.request import urlretrieve
import pandas as pd

url = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_1606/datasets/winequality-red.csv' ## Winquality에 대한 url을 저장 
urlretrieve(url, 'winequality-red.csv') ## Save file locally

df = pd.read_csv('winequality-red.csv', sep=';')
print(df.head())

# Opening and reading flat files from the web
import matplotlib.pyplot as plt
import pandas as pd
    
url = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_1606/datasets/winequality-red.csv'
df = pd.read_csv(url, sep = ';')
print(df.head())
    
## Plot first column of df
pd.DataFrame.hist(df.ix[:, 0:1])
plt.xlabel('fixed acidity (g(tartaric acid)/dm$^3$)')
plt.ylabel('count')
plt.show()

# Importing non-flat files from the web
import pandas as pd
url = 'http://s3.amazonaws.com/assets.datacamp.com/course/importing_data_into_r/latitude.xls'

xls = pd.read_excel(url, sheet_name = None) ## excel sheet를 url에서 불러오기, 이때 xls는 dict
## sheet_name = None : 모든 sheet의 이름을 불러옴 

print(type(xls))
print(xls.keys()) ## sheet이름이 'Key'로 들어감 

# Print the head of the first sheet (using its name, NOT its index)
print(xls['1700'].head())
```

## 1.2 HTTP requests to import files from the web

```python
# Performing HTTP requests in Python using urllib
## HTTP를 python으로 받아오는 정석적인 방법 
from urllib.request import urlopen, Request

url = "http://www.datacamp.com/teach/documentation"

request = Request(url) ## Request()를 이용한 url 요청
response = urlopen(request) ## urlopen()을 이용한 request 오픈 = url 주소 열기 
print(type(response))

response.close() ## 닫기 

# Printing HTTP request results in Python using urllib
from urllib.request import urlopen, Request
url = "http://www.datacamp.com/teach/documentation"
request = Request(url)
response = urlopen(request)

html = response.read() ## Extract the response: html, url의 html을 읽어온다. 
print(html) ## Print the html

response.close()

# Performing HTTP requests in Python using requests
## requests package를 이용해 좀 더 간편히 HTTP page를 불러오는 방법
import requests

url = "http://www.datacamp.com/teach/documentation"

r = requests.get(url) # requests.get = Request() + urlopen()
text = r.text ## Extract the response: text, text로 html page를 불러옴. 

print(text)
```

## 1.3 Scraping the web in Python
Web page에서 data를 긁어오는 방법으로 BeautifulSoup package를 이용해보자. 
```python
# Parsing HTML with BeautifulSoup
import requests
from bs4 import BeautifulSoup

url = 'https://www.python.org/~guido/'

r = requests.get(url)
html_doc = r.text

soup = BeautifulSoup(html_doc) ## Create a BeautifulSoup object from the HTML: soup
pretty_soup = soup.prettify() ## Prettify the BeautifulSoup object: pretty_soup

print(pretty_soup) ## Print the pretty_soup
print(html_doc) ## pretty_soup과 html_doc의 비교. pretty쪽이 조금 더 읽기 편해졌다. 

# Turning a webpage into data using BeautifulSoup: getting the text
import requests
from bs4 import BeautifulSoup
url = 'https://www.python.org/~guido/'

r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc)

guido_title = soup.title ## web page의 title만 가져옴. soup의 title attribute call
print(guido_title)

guido_text = soup.get_text() ## web page의 text만 가져옴. soup에 .get_text() method 이용. 
print(guido_text)

# Turning a webpage into data using BeautifulSoup: getting the hyperlinks
a_tags = soup.find_all('a') ## soup에 .find_all('a')을 이용해 a가 들어간 hyper link 찾기 

# Print the URLs to the shell
for link in a_tags :
    print(link.get('href'))
```
# 2. Interacting with APIs to import data from the web
## 2.1 Introduction to APIs and JSONs
```python
# Loading and exploring a JSON
## with을 이용한 context manager을 사용. 
with open("a_movie.json") as json_file: # open('json' 파일 이름)
    json_data = json.load(json_file) ## json.load()를 이용해 json data를 object로 저장 

for k in json_data.keys(): ## json file은 dict으로 저장되기 때문에 key:value로 불러올 수 있음. 
    print(k + ': ', json_data[k])
```

## 2.2 APIs and interacting with the world wide web
```python
# API requests
import requests
url = 'http://www.omdbapi.com/?apikey=72bc447a&t=the+social+network'
## 'http://www.omdbapi.com'까지 주소
## '/?apikey=72bc447a' 쿼리 1
## 't=the+social+network' 쿼리 2. 쿼리 1과 2를 연결해주기 위해 '&' 추가 

r = requests.get(url)
print(r.text)

# JSON–from the web to Python
import requests
url = 'http://www.omdbapi.com/?apikey=72bc447a&t=social+network'

r = requests.get(url) ## Package the request, send the request and catch the response: r
json_data = r.json() ## Decode the JSON data into a dictionary: json_data
## .json method를 이용해 url로 받아온 json data를 dict으로 풀어냈다. 

## Print each key-value pair in json_data
for k in json_data.keys():
    print(k + ': ', json_data[k])
    
# Checking out the Wikipedia API
import requests
url = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles=pizza'
r = requests.get(url)

json_data = r.json()

## extract Wikipedia page
pizza_extract = json_data['query']['pages']['24768']['extract'] ## dict data형태를 보니 nested dict인듯하다.
## 여러 개의 key로 원하는 부분을 extract했다. 
print(pizza_extract)
```

# 3. Diving deep into the Twitter API
## 3.1 The Twitter API and Authentication

```python
# API Authentication
import tweepy

## Store OAuth authentication credentials in relevant variables
access_token = "1092294848-aHN7DcRP9B4VMTQIhwqOYiB14YkW92fFO8k8EPy"
access_token_secret = "X4dHmhPfaksHcQ7SCbmZa2oYBBVSD2g8uIHXsp5CTaksx"
consumer_key = "nZ6EA0FxZ293SxGNg8g8aP0HM"
consumer_secret = "fJGEodwe3KiKUnsYJC3VRndj7jevVvXbK2D5EiJ2nehafRgA6i" 
## ID, PW의 관계로 보인다. 

## Pass OAuth details to tweepy's OAuth handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) ## 먼저 권한에 대한 ID, PW를 입력
auth.set_access_token(access_token, access_token_secret) ## access에 대한 ID, PW를 입력 

# Streaming tweets
l = MyStreamListener() ## Initialize Stream listener
stream = tweepy.Stream(auth, l) ## Create your Stream object with authentication
stream.filter(track = ['clinton', 'trump', 'sanders', 'cruz']) ## Filter Twitter Streams to capture data by the keywords:
## keyword는 list로 입력해야하는 모양

# Load and explore your Twitter data
import json

tweets_data_path = 'tweets.txt' ## String of path to file: tweets_data_path
tweets_data = [] ## Initialize empty list to store tweets: tweets_data, loop를 이용한 공간 생성 

tweets_file = open(tweets_data_path, "r") ## Open connection to file

## Read in tweets and store in list: tweets_data
for line in tweets_file:
    tweet = json.loads(line) ## tweets_file의 각 line을 json.loads()를 이용해 dict으로 변환, tweet으로 return
    tweets_data.append(tweet) ## tweets_data에 .append() method를 이용, tweet을 추가함. 


tweets_file.close() ## Close connection to file

print(tweets_data[0].keys()) ## Print the keys of the first tweet dict

# Twitter data to DataFrame
import pandas as pd

df = pd.DataFrame(tweets_data, columns=['text', 'lang']) ## Build DataFrame of tweet texts and languages
## columns = ['str', 'str'] : dataframe의 columns을 정의. tweets_data는 dict이므로 'key'를 column으로 정의함. 
print(df.head())

# A little bit of Twitter text analysis
# # Initialize list to store tweet counts
[clinton, trump, sanders, cruz] = [0, 0, 0, 0]

## Iterate through df, counting the number of tweets in which
for index, row in df.iterrows():
    clinton += word_in_text('clinton', row['text'])
    trump += word_in_text('trump', row['text'])
    sanders += word_in_text('sanders', row['text'])
    cruz += word_in_text('cruz', row['text'])
    
print([clinton, trump, sanders, cruz]) ## [9, 77, 6, 14]

# Plotting your Twitter data
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(color_codes=True) ## Set seaborn style
cd = ['clinton', 'trump', 'sanders', 'cruz'] ## Create a list of labels:cd

## Plot the bar chart
ax = sns.barplot(cd, [clinton, trump, sanders, cruz]) 
## cd : x-axis
## [clinton, trump, sanders, cruz] : 이전 예제에서 만들어둔 각 후보자의 언급 횟수
ax.set(ylabel="count")
plt.show()
```
