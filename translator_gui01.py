from tkinter import *
from googletrans import Translator  # Use googletrans 3.1.0a0c

window = Tk()

main = Frame(window)
translate = Frame(window)

lang = 'ta'


def main_translate():
    main.pack(fill='both', expand=1)
    translate.pack_forget()


def translate_main():
    translate.pack(fill='both', expand=1)
    main.pack_forget()


# Main window frame
message_text = Text(main, width=20, height=8, padx=8, pady=4)
message_context = message_text.get('1.0', 'end')
message_text.pack()

translator_button = Button(main, text='Translate')
translator_button.pack()

# Translate window frame
translate_context = StringVar()
translated_text = Text(translate, width=20, height=8, padx=8, pady=4)
translated_text.insert('1.0', message_context)
translated_text.pack()

# Window
main_button = Button(window, text='Main', command=main_translate)
main_button.pack()

translate_button = Button(window, text='Translate', command=translate_main)
translate_button.pack()

window.mainloop()