import googletrans
from googletrans import Translator # Use googletrans 3.1.0a0c
from gtts import gTTS
from playsound import playsound


def trans(org_text, lang):
  translator = Translator()
  conv_text = translator.translate(org_text, lang)
  return conv_text.text

def speak(text, lang):
  result = ",".join([text.rstrip('\n')])
  tts = gTTS(result, lang=lang, slow=False)
  tts.save('audio_msg.mp3')
  print(result)
  playsound('./audio_msg.mp3')


if __name__ == '__main__':
  lang = 'ta'

  MyText = "Hello"

  say_hello = trans(MyText, lang)
  print(say_hello)

  speak(say_hello, lang)

  languages = googletrans.LANGUAGES

  print(list(languages))

