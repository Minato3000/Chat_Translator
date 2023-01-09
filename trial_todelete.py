from googletrans import Translator
from gtts import gTTS
from playsound import playsound


translator = Translator()
from_lang = 'en'
to_lang = 'ta'
MyText = "Hello, I am your translator. What is your name? I know few languages. Do you need any help?"

trans_text = translator.translate(MyText,src = from_lang, dest = to_lang)
print(trans_text.text)

voice = gTTS(trans_text.text,lang=to_lang, slow=False)
voice.save("voice.mp3")
playsound("./voice.mp3")