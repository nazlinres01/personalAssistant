from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import goslate

app = Flask(__name__, static_folder='build_recipe/static')

gs = goslate.Goslate()

@app.route('/recipe', methods=['POST'])
def get_recipe():
    data = request.get_json()
    recipe_name = data['recipe_name']

    # Türkçe yemek adını İngilizce'ye çevir
    translated_name = gs.translate(recipe_name, 'en')

    # İnternetten yemek tarifini almak için bir API çağrısı yapalım
    recipe = get_recipe_from_external_api(translated_name)

    return jsonify(recipe)

def get_recipe_from_external_api(recipe_name):
    # Burada, kullanabileceğiniz bir API'ya istek yapabilirsiniz.
    # Örnek olarak, "Edamam" adlı bir yemek tarifi API'sını kullanalım
    base_url = 'https://api.edamam.com/search'
    app_id = '4bbe1359'
    app_key = '951a271e4345b289ff3dd1bd4749c361'

    params = {
        'q': recipe_name,
        'app_id': app_id,
        'app_key': app_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Gelen verileri işleyerek gerekli bilgileri alalım
    recipe = {
        'tarif adı': '',
        'malzemeler': [],
        'yapılışı': ''
    }

    if 'hits' in data and len(data['hits']) > 0:
        hit = data['hits'][0]['recipe']
        ingredients = hit['ingredientLines']

        recipe['tarif adı'] = recipe_name
        recipe['malzemeler'] = ingredients
        recipe['yapılışı'] = hit['url']

    return recipe

# React dosyalarını sunmak için route
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("build_recipe/" + path):
        return send_from_directory("build_recipe/", path)
    else:
        return send_from_directory("build_recipe", "index.html")

if __name__ == '__main__':
    app.run(debug=True)
