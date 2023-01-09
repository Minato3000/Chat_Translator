from tkinter import *
from textblob import TextBlob
from googletrans import Translator # Use googletrans 3.1.0a0c


window = Tk()


def refresh(text_widget):
    text_widget.configure(state='normal')
    text_widget.delete(1.0, END)
    text_widget.update()


def translate_text():
    context = TextBlob(original_text.get(1.0, END))

    translator = Translator()
    context = translator.translate(context, 'ta')

    refresh(translated_text)

    translated_text.configure(state='normal')
    translated_text.insert(1.0, context.text)
    translated_text.configure(state='disabled')

    refresh(original_text)


original_text = Text(window, width=60, height=6, padx=4, pady=6)
original_text.pack()

translate_btn = Button(window, text='Translate', command=translate_text)
translate_btn.pack()

translated_text = Text(window, state='disabled', width=60, height=6, padx=4, pady=6)
translated_text.pack()

window.mainloop()
