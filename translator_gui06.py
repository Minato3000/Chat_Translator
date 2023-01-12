import os  # OS to do operations on system
from tkinter import Tk, END, Frame, Text, Button, Label, CENTER, BOTH, TOP, BOTTOM, LEFT  # Tkinter necessary functions
from tkinter.font import Font  # Tkinter's font function to customize font
from tkinter.ttk import Combobox  # Tkinter's Combobox for language selection
from textblob import TextBlob  # Textblob to store and manipulate text

from googletrans import Translator, LANGUAGES  # To translate the text using google's translator
# googletrans version 3.1.0a0c

from gtts import gTTS  # To convert text to speech
from playsound import playsound  # playsound version 1.2.2

import pyttsx3 as pyt  # For accessing text to speech voices
import speech_recognition as sr  # To recognize the speech


class App(Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Translator")
        self.geometry('1000x600+20+20')

        # Place the heading frame in grid
        self.head = HeadingFrame(self)
        self.head.grid(row=0, column=0, columnspan=2, sticky="N")

        # Place the original frame in grid
        self.left = originalFrame(self)
        self.left.grid(row=1, column=0)

        # Place the translator frame in grid
        self.right = TranslateFrame(self)
        self.right.grid(row=1, column=1)


# Lang_code function
# To convert the selected language name to the language code
def lang_code(self, lang_option):
    for key, value in self.languages.items():
        if value == lang_option.get():
            code = key
            return code


# Refresh function
# To refresh each text widget
def refresh(text_widget):
    text_widget.configure(state='normal')
    text_widget.delete(1.0, END)
    text_widget.update()


# The original frame
class originalFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.config(width=500, height=500)

        # Defining the font
        basic_font = Font(family="Poppins", size=12)

        # Record language button
        self.record_btn = Button(self, text='Record', padx=8, pady=4, font=basic_font, bg='#45b592', fg='#ffffff',
                                 command=self.capture)
        self.record_btn.pack(side=TOP, fill=BOTH, expand=True)

        # The text to be translated - Text widget
        self.original_text = Text(self, bg="azure2", fg="black", width=50, height=20, font=basic_font, padx=4, pady=8)
        self.original_text.pack(side=TOP, fill=BOTH, expand=True)

        # Speaks the content - Button widget
        self.speak_btn = Button(self, text="Speak", padx=8, pady=3, font=basic_font, bg='#45b592', fg='#ffffff',
                                command=self.speak)
        self.speak_btn.pack(side=LEFT, fill=BOTH, expand=True)

        # The languages in the googletrans
        self.languages = LANGUAGES
        language_list = list(self.languages.values())

        # Selecting the language - Combobox
        self.from_language_option = Combobox(self, width=20, values=language_list, font=basic_font)
        self.from_language_option.current(21)
        self.from_language_option.pack(side=LEFT, fill=BOTH, expand=True)

        # To translate the text - Translate Button
        self.translate_btn = Button(self, text="Translate", padx=8, pady=3, font=basic_font, bg='#45b592', fg='#ffffff',
                                    command=self.translate)
        self.translate_btn.pack(side=LEFT, fill=BOTH, expand=True)

    # The capture function
    # Records the audio and recognizes the speech text
    def capture(self):
        rec = sr.Recognizer()
        mc = sr.Microphone()
        lang = lang_code(self, self.from_language_option)
        with mc as source:
            print("Speak Now !")
            rec.adjust_for_ambient_noise(source, duration=0.2)
            try:
                audio = rec.listen(source)
                MyText = rec.recognize_google(audio, language=lang)
                refresh(self.original_text)
                self.original_text.insert(1.0, MyText)
            except sr.UnknownValueError:
                print("Unable to Understand the Input")
            except sr.RequestError:
                print("Unable to provide Required Output")

    # The speak function
    # Produces audio of the text obtained
    def speak(self):
        text = self.original_text.get(1.0, END)
        lang = lang_code(self, self.from_language_option)
        tts = gTTS(text, lang=lang, slow=False)
        tts.save('./audio/original_audio_msg.mp3')
        playsound('./audio/original_audio_msg.mp3')
        os.remove('./audio/original_audio_msg.mp3')

    # The translate function
    # Convert the text of a language to another language
    def translate(self):
        # Textblob used to store and manipulate string
        text = TextBlob(self.original_text.get(1.0, END))

        # To translate using google trans
        translator = Translator()

        # Obtain the language code
        from_lang = lang_code(self, self.from_language_option)
        to_lang = lang_code(self, self.parent.right.to_language_option)

        # Translate the text
        context = translator.translate(text, src=from_lang, dest=to_lang)
        refresh(self.parent.right.translated_text)

        self.parent.right.translated_text.configure(state='normal')
        self.parent.right.translated_text.insert(1.0, context.text)
        self.parent.right.translated_text.configure(state='disabled')

        refresh(self.original_text)


# The translation frame
class TranslateFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.config(width=500, height=500)

        self.engine = pyt.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.engine.setProperty('rate', 190)
        self.engine.setProperty('volume', 0.7)

        # Font configuration
        basic_font = Font(family="Poppins", size=12)

        # Record language button
        self.record_btn = Button(self, text='Record', padx=8, pady=4, font=basic_font, bg='#45b592', fg='#ffffff',
                                 command=self.capture)
        self.record_btn.pack(side=TOP, fill=BOTH, expand=True)

        # The translated text - Text widget
        self.translated_text = Text(self, bg="azure2", fg="black", font=basic_font, width=50, height=20, padx=4, pady=8)
        self.translated_text.pack(side=TOP, fill=BOTH, expand=True)

        # The languages in the googletrans
        self.languages = LANGUAGES
        language_list = list(self.languages.values())

        # To translate the text - Translate Button
        self.translate_btn = Button(self, text="Translate", padx=8, pady=3, font=basic_font, bg='#45b592', fg='#ffffff',
                                    command=self.translate)
        self.translate_btn.pack(side=LEFT, fill=BOTH, expand=True)

        # Selecting the language - Combobox
        self.to_language_option = Combobox(self, width=20, values=language_list, font=basic_font)
        self.to_language_option.current(93)
        self.to_language_option.pack(side=LEFT, fill=BOTH, expand=True)

        # Speaks the translated content - Button widget
        self.speak_btn = Button(self, text="Speak", padx=8, pady=3, font=basic_font, bg='#45b592', fg='#ffffff',
                                command=self.speak)
        self.speak_btn.pack(side=BOTTOM, fill=BOTH, expand=True)

    # The capture function
    # Records the audio and recognizes the speech text
    def capture(self):
        rec = sr.Recognizer()
        mc = sr.Microphone()
        lang = lang_code(self, self.to_language_option)
        with mc as source:
            print("Speak Now !")
            rec.adjust_for_ambient_noise(source, duration=0.2)
            try:
                audio = rec.listen(source)
                MyText = rec.recognize_google(audio, language=lang)
                refresh(self.translated_text)
                self.translated_text.insert(1.0, MyText)
            except sr.UnknownValueError:
                print("Unable to Understand the Input")
            except sr.RequestError:
                print("Unable to provide Required Output")

    # The speak function
    # Produces audio of the text obtained
    def speak(self):
        text = self.translated_text.get(1.0, END)
        lang = lang_code(self, self.to_language_option)
        tts = gTTS(text, lang=lang, slow=False)
        tts.save('./audio/translated_audio_msg.mp3')
        playsound('./audio/translated_audio_msg.mp3')
        os.remove('./audio/translated_audio_msg.mp3')

    # The translate function
    # Convert the text of a language to another language
    def translate(self):
        # Textblob used to store and manipulate string
        text = TextBlob(self.translated_text.get(1.0, END))

        # To translate using google trans
        translator = Translator()

        # Obtain the language code
        from_lang = lang_code(self, self.to_language_option)
        to_lang = lang_code(self, self.parent.left.from_language_option)

        # Translate the text
        context = translator.translate(text, src=from_lang, dest=to_lang)
        refresh(self.parent.left.original_text)

        self.parent.left.original_text.configure(state='normal')
        self.parent.left.original_text.insert(1.0, context.text)
        self.parent.left.original_text.configure(state='disabled')

        refresh(self.translated_text)


# The heading frame
class HeadingFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.config(width=1000, height=100)

        heading_font = Font(family="Noto sans CJK TC", size=14, weight="bold", slant="italic")
        heading = Label(self, text="LanguagePedia", font=heading_font, bg="#0a3d62", fg="white", padx=30, pady=10,
                        relief="raised")
        heading.place(relx=0.5, rely=0.3, anchor=CENTER)

        subheading_font = Font(family="Poppins", size=12)
        subheading = Label(self, text="Your trustworthy translation partner", font=subheading_font, fg="#0a3d62",
                           padx=10,
                           pady=4, relief="flat")
        subheading.place(relx=0.5, rely=0.7, anchor=CENTER)


# The name function runs the whole translator app
if __name__ == "__main__":
    translator = App()
    translator.mainloop()
