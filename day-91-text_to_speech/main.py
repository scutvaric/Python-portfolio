import tkinter as tk
from tkinter import filedialog, messagebox
import fitz
from google.cloud import texttospeech

pdf_text = ""
BG_COLOR = "#d0e6f7"

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def upload_PDF_file():
    global pdf_text
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if path:
        pdf_text = extract_text_from_pdf(path)
        messagebox.showinfo("PDF Loaded", "Text extracted successfully!")

def save_result():
    global pdf_text
    if not pdf_text:
        messagebox.showwarning("No PDF", "Please upload a PDF file first.")
        return

    #Avoid Google's text-to-speech free limitation:
    text_chunk = pdf_text[:500]

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_chunk)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    output_path = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 Audio", "*.mp3")],
        title="Save audio file as..."
    )
    # The response's audio_content is binary.
    if output_path:
        with open(output_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)

        messagebox.showinfo("Success", f'Audio content written to {output_path}')
    else:
        messagebox.showinfo("Cancelled", "Save cancelled.")

root = tk.Tk()
root.title("PDF to Speech")
root.geometry("300x300")

root.configure(bg=BG_COLOR)

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Button(button_frame,
          text="Upload PDF File",
          highlightthickness=0,
          bg=BG_COLOR,
          command=upload_PDF_file).pack(pady=5)
tk.Button(button_frame,
          text="Save Audio File",
          highlightthickness=0,
          bg=BG_COLOR,
          command=save_result).pack(pady=5)

root.mainloop()