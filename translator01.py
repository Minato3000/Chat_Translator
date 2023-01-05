from googletrans import Translator # Use googletrans 3.1.0a0c
from gtts import gTTS
from playsound import playsound


def trans(org_text, lang):
  translator = Translator()
  conv_text = translator.translate(org_text, lang)
  return conv_text.text

def speak(text, lang):
  tts = gTTS(text, lang=lang)
  tts.save('audio_msg.mp3')
  playsound('./audio_msg.mp3')


if __name__ == '__main__':
  lang = 'ta'

  say_hello = trans("Hello I am your friend", lang)
  print(say_hello)

  speak(say_hello, lang)

