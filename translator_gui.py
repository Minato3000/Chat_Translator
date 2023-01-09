from tkinter import *
from tkinter import ttk

from translator01 import speak

window = Tk()

lang_label = Label(window, text="Select a language:")
lang_label.grid(column=0, row=0, sticky=W, padx=5, pady=5)

lang = Entry(window)
lang.grid(column=1, row=0, sticky=E, padx=5, pady=5)

message_text = Text(window, width=40, height=10, padx=8, pady=4)
message_text.grid(column=0, row=1, columnspan=2, sticky=EW, padx=5, pady=5)
message = message_text.get('1.0', "end-1c")

translate_button = Button(window, text="Translate", command=lambda: speak(message, lang))
translate_button.grid(column=1, row=3, sticky=E, padx=5, pady=5)

window.mainloop()
