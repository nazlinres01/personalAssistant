from flask import Flask, jsonify, send_from_directory, redirect, request
import os
from gnewsclient import gnewsclient
import re

app = Flask(__name__, static_folder='build_news/static')


# Kategorilere göre haberleri çek ve döndür
def fetch_news(category):
    client = gnewsclient.NewsClient(language='turkish', location='turkey')
    client.topic = category
    articles = client.get_news()

    # Her bir haber objesine url alanını ekle
    for article in articles:
        article['url'] = article['link']
        article['title'] = re.sub(r'(https?:\/\/[^\s]+)', '', article['title']).strip()

    return articles


# Flask API endpoint'ı
@app.route('/api/news/<category>', methods=['GET'])
def get_news_by_category(category):
    articles = fetch_news(category)

    return jsonify(articles)


# Haber sayfasına yönlendirme
@app.route('/api/news/redirect', methods=['POST'])
def redirect_to_news_page():
    url = request.json['url']
    return redirect(url, code=302)


# React dosyalarını sunmak için route
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("build_news/" + path):
        return send_from_directory("build_news/", path)
    else:
        return send_from_directory("build_news", "index.html")


if __name__ == '__main__':
    app.run()
