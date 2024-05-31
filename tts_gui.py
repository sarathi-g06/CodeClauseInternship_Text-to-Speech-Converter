import os
import pyttsx3
import simpleaudio as sa
import tkinter as tk
from tkinter import ttk, messagebox


def text_to_speech(text, rate=200, voice=None):
    speech = pyttsx3.init()
    if voice is not None:
        voices = speech.getProperty('voices')
        speech.setProperty('voice', voices[voice].id)
    speech.setProperty('rate', rate)
    filename = "output.wav"
    speech.save_to_file(text, filename)
    speech.runAndWait()
    return filename


def play_audio(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def update_rate_label(value):
    rate_value_label.config(text=f" {int(float(value))}")


def convert_and_play():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text to convert to speech.")
        return

    rate = rate_var.get()
    try:
        voice = int(voice_var.get().split(":")[0])
    except ValueError:
        messagebox.showwarning("Input Error", "Please select a valid voice.")
        return

    audio_file = text_to_speech(text, rate, voice)
    play_audio(audio_file)

    # Remove the audio file after playing
    if os.path.exists(audio_file):
        os.remove(audio_file)


# GUI
root = tk.Tk()
root.title("Text-to-Speech Converter")
root.iconbitmap('speaking.ico')

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="wens")
title_label = ttk.Label(frame, text="Text-to-Speech Converter\n\tBy SARATHI.G",
                        font=("Montserrat Subrayada", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

text_label = ttk.Label(frame, text="Enter Text:", font=("Montserrat Medium", 12))
text_label.grid(row=1, column=0, sticky=tk.W)

text_entry = tk.Text(frame, font=("Montserrat Medium", 12), width=40, height=10)
text_entry.grid(row=2, column=0, columnspan=3, pady=5)

rate_label = ttk.Label(frame, text="Speech Rate :   ", font=("Montserrat Medium", 12))
rate_label.grid(row=3, column=0, sticky=tk.W)

rate_var = tk.DoubleVar(value=200)
rate_slider = ttk.Scale(frame, from_=100, to=300, orient=tk.HORIZONTAL, variable=rate_var, command=update_rate_label)
rate_slider.grid(row=3, column=1, sticky=tk.W, pady=5)

rate_value_label = ttk.Label(frame, text=f"  {int(rate_var.get())}", font=("Montserrat Medium", 12))
rate_value_label.grid(row=3, column=2, sticky=tk.W)

voice_label = ttk.Label(frame, text="Voice  :", font=("Montserrat Medium", 12))
voice_label.grid(row=4, column=0, sticky=tk.W)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
voice_var = tk.StringVar(value="0")

voice_menu = ttk.Combobox(frame, textvariable=voice_var, values=[f"{i}: {v.name}" for i, v in enumerate(voices)],
                          state="readonly")
voice_menu.grid(row=4, column=1, sticky=tk.W)

convert_button = ttk.Button(frame, text="Convert and Play", command=convert_and_play, style="TButton")
convert_button.grid(row=5, column=0, columnspan=3, pady=10)

style = ttk.Style()
style.configure("TButton", font=("Montserrat Medium", 12))

root.mainloop()
