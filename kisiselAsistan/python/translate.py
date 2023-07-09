from flask import Flask, request, jsonify, send_from_directory
import os
from googletrans import Translator

app = Flask(__name__, static_folder='build_translate/static')


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['text']
    source_lang = data['sourceLang']
    target_lang = data['targetLang']

    translator = Translator(service_urls=['translate.google.com'])
    translated_text = translator.translate(text, src=source_lang, dest=target_lang).text

    return jsonify({'translated_text': translated_text})


# React dosyalarını sunmak için route
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("build_translate/" + path):
        return send_from_directory("build_translate/", path)
    else:
        return send_from_directory("build_translate", "index.html")


if __name__ == '__main__':
    app.run()
