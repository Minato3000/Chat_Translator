import os
from tkinter import Tk, END, Frame, Text, Button
from tkinter.font import Font
from tkinter.ttk import Combobox
from textblob import TextBlob

import googletrans  # googletrans version 3.1.0a0c
from googletrans import Translator

from gtts import gTTS
from playsound import playsound  # playsound version 1.2.2


class App(Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Translator")
        self.geometry('800x500')

        # Frame Original text box
        self.left = originalFrame(self)
        self.left.grid(row=0, column=0, padx=10, pady=10)

        # Frame Translation text box
        self.right = TranslateFrame(self)
        self.right.grid(row=0, column=1, padx=10, pady=10)


def refresh(text_widget):
    text_widget.configure(state='normal')
    text_widget.delete(1.0, END)
    text_widget.update()


# The original frame
class originalFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        # Defining the font
        my_font = Font(
            family='Poppins',
            size=10,
            weight='bold'
        )

        # The text to be translated - Text widget
        self.original_text = Text(self, bg="azure2", fg="black", width=50, height=25, font=my_font, padx=4, pady=8)
        self.original_text.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # The languages in the googletrans
        self.languages = googletrans.LANGUAGES
        language_list = list(self.languages.values())

        # Selecting the language - Combobox
        self.language_option = Combobox(self, width=20, values=language_list, font=my_font)
        self.language_option.current(21)
        self.language_option.grid(row=2, column=0, padx=5, pady=5)

        # To translate the text - Translate Button
        self.translate_btn = Button(self, text="Translate", padx=8, pady=3,font=my_font , command=self.translate)
        self.translate_btn.grid(row=2, column=1, padx=5, pady=5)

    # Translation function
    def translate(self):
        # Textblob used to store and manipulate string
        text = TextBlob(self.original_text.get(1.0, END))

        # To translate using google trans
        translator = Translator()

        # Obtain the language code
        self.lang = self.getlangcode()

        # Translate the text
        context = translator.translate(text, self.lang)
        refresh(self.parent.right.translated_text)

        self.parent.right.translated_text.configure(state='normal')
        self.parent.right.translated_text.insert(1.0, context.text)
        self.parent.right.translated_text.configure(state='disabled')

        refresh(self.original_text)

    # Obtain language code function
    def getlangcode(self):
        for key, value in self.languages.items():
            if value == self.language_option.get():
                langcode = key
                return langcode


# The translation frame
class TranslateFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        # Font configuration
        my_font = Font(
            family='Poppins',
            size=10,
            weight='bold'
        )

        # The translated text - Text widget
        self.translated_text = Text(self, bg="azure2", fg="black", font=my_font, width=50, height=25, padx=4, pady=8)
        self.translated_text.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Speaks the translated content - Button widget
        self.speak_btn = Button(self, text="Speak", padx=8, pady=3,font=my_font , command=self.speak)
        self.speak_btn.grid(row=1, column=0, padx=5, pady=5)

    # Speak function
    def speak(self):
        text = self.translated_text.get(1.0, END)
        lang = self.parent.left.lang
        tts = gTTS(text, lang=lang, slow=False)
        tts.save('./audio/audio_msg.mp3')
        playsound('./audio/audio_msg.mp3')
        os.remove('./audio/audio_msg.mp3')


if __name__ == "__main__":
    translator = App()
    translator.mainloop()
