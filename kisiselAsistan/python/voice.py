import os
import speech_recognition as sr
from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from gtts import gTTS

app = Flask(__name__)

# ChatBot oluşturma
bot = ChatBot('Turkish Bot')

# Türkçe konuşma içeriğini eğitme
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.turkish")

# Ses tanıma motorunu oluşturma
recognizer = sr.Recognizer()


@app.route("/get_bot_response", methods=["POST"])
def get_bot_response():
    # Sesli yanıt al
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        # Sesli yanıtı metne çevir
        user_message = recognizer.recognize_google(audio, language="tr-TR")

        # Bot yanıtını al
        bot_response = bot.get_response(user_message).text

        # Bot yanıtını sesli olarak oluştur ve kaydet
        tts = gTTS(text=bot_response, lang="tr")
        tts.save("response.mp3")

        return jsonify({"bot_response": "response.mp3"})

    except sr.UnknownValueError:
        return jsonify({"bot_response": ""})

    except sr.RequestError as e:
        return jsonify({"bot_response": ""})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
