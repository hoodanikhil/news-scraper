# app.py
from flask import Flask, render_template, jsonify, request
from newsplease import NewsPlease
import requests
import xml.etree.ElementTree as ET

#extract the final url from google news url
def get_final_url(google_news_url):
    try:
        response = requests.get(google_news_url)
        return response.url
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while getting final URL: {e}")

#extract the rss feed from google news search query
def get_google_rss(search_query):
    try:
        return requests.get(f"https://news.google.com/rss/search?q={search_query}&hl=en-IN&gl=IN&ceid=IN:en").content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while getting Google RSS: {e}")

#extract the links from the rss feed
def get_links_from_rss(rss_feed):
    try:
        root = ET.fromstring(rss_feed) #parse the xml
        links = root.findall('.//link') #find all the links in the xml
        links = links[1:] #remove the first link as it is the link to the google news search query
        sources = root.findall('.//source')
        return links, sources
    except ET.ParseError as e:
        print(f"An error occurred while parsing XML: {e}")
        return [], []

#extract the news links from the search query
def get_news_from_search_query(search_query, max_no_of_news=2):
    rss_feed = get_google_rss(search_query) #get the rss feed
    if rss_feed:
        links, sources = get_links_from_rss(rss_feed) #get the links from the rss feed
        
        news_links = [] #list to store the news links
        for link, source in zip(links, sources):
            final_url = get_final_url(link.text) #get the final url from the google news url
            if final_url:
                news_links.append((final_url, source.text)) #append the final url to the list
                if len(news_links) == max_no_of_news: # stop if the number of news links is equal to the max number of news
                    break
        return news_links
    return []

#extract the article details from the news links
def get_articles_from_news_links(news_links): 
    news_details = [] #list to store the news titles
    for link in news_links:
        try:
            article = NewsPlease.from_url(link[0]) #get the article from the news link
            news_details.append({'headline' : article.title,
                                 'description' : article.description,
                                 'body' : article.maintext,
                                 'image_url': article.image_url,
                                 'article_url': article.url,
                                 'date_publish' : article.date_publish,
                                 'source' : link[1]}) #append the article details to the list
        except Exception as e:
            print(f"An error occurred while getting news from the link: {e}")
    return news_details

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='A (very) basic news scraper', message='A (very) basic news scraper')

@app.route('/button', methods=['POST'])
def button():
    input_text = request.form.get('text')
    num_articles = request.form.get('num_articles')
    if num_articles is not None and num_articles.isnumeric():
        num_articles = int(num_articles)
    else:
        num_articles = 5
    # You can do any processing with input_text here
    news_links = get_news_from_search_query(input_text, num_articles) #get the news links
    articles = get_articles_from_news_links(news_links) #get the articles
    return jsonify({'result': articles})

if __name__ == '__main__':
    app.run(debug=True)
