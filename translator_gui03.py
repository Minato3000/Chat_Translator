from tkinter import *
from tkinter import filedialog

from translator01 import speak, trans

main_window = Tk()

text_window = Frame(main_window)
translate_window = Frame(main_window)

lang = 'ta'


def text_translate():
    text_window.pack(fill=Y, expand=1)
    translate_window.pack_forget()


def translate_text():
    translate_window.pack(fill=X, expand=1)
    text_window.pack_forget()


def save_file():
    text_to_save = message_text.get('1.0', END)
    save_dialog = filedialog.asksaveasfile(filetypes=[('text file', '*.txt')],
                                           defaultextension='.txt', initialdir='/',
                                           mode='w')
    text_to_save = trans(text_to_save, 'ta')
    print(text_to_save)
    save_dialog.write(text_to_save)
    save_dialog.close()
    message_text.delete('1.0', END)  # Delete from position 0 till end
    message_text.update()
    convertor_button.config(text="Complete")
    convertor_button.after(3000, lambda: convertor_button.config(text='Convert'))



def speak_translation():
    text_to_speak = filedialog.askopenfile(filetypes=[('text file', '*.txt')],
                                           defaultextension='.txt', initialdir='/')
    translated_text.insert('1.0', text_to_speak.read())
    speak(translated_text.get('1.0', END), 'ta')
    print(text_to_speak.read())


# Text window frame
message_text = Text(text_window, width=20, height=8, padx=8, pady=4)
message_text.pack()

convertor_button = Button(text_window, text='Convert', command=lambda: save_file())
convertor_button.pack()

# Translate window frame
translated_text = Text(translate_window, width=20, height=8, padx=8, pady=4)
translated_text.pack()

speak_button = Button(translate_window, text='Speak', command=lambda: speak_translation())
speak_button.pack()

# Window
main_button = Button(main_window, text='Text', command=text_translate)
main_button.pack(side=TOP)

translate_button = Button(main_window, text='Translate', command=translate_text)
translate_button.pack(side=TOP)

main_window.mainloop()
