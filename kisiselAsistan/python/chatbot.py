import os
from zemberek import TurkishSentenceNormalizer, TurkishTokenizer, TurkishMorphology
from flask import Flask, render_template, request, send_from_directory
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__, static_folder='build/static')

# Türkçe dil işleme araçlarını oluşturma
morphology = TurkishMorphology.create_with_defaults()
normalizer = TurkishSentenceNormalizer(morphology)
tokenizer = TurkishTokenizer(accepted_type_bits=0x1FF)

def analyze_sentence(sentence):
    normalized_sentence = normalizer.normalize(sentence)
    tokens = tokenizer.tokenize(normalized_sentence)
    word_analysis_list = []
    for token in tokens:
        word_analysis = morphology.analyze(token.content)
        word_analysis_list.append(word_analysis)
    return word_analysis_list

# ChatBot oluşturma
bot = ChatBot('Turkish Bot')

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.turkish")

# Eğitme verileri eklemek için kendi dosyalarınızı kullanabilirsiniz
#trainer.train("data/custom_data.yml")

@app.route("/message", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    bot_response = bot.get_response(user_message).text
    return {"bot_response": bot_response}

# React dosyalarını sunmak için route
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("build/" + path):
        return send_from_directory("build/", path)
    else:
        return send_from_directory("build", "index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)