import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def upload_base_image():
    global base_image
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if path:
        base_image = Image.open(path).convert("RGBA")
        preview_image(base_image)

def upload_watermark():
    global base_image
    if base_image is None:
        return

    wm_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if wm_path:
        watermark = Image.open(wm_path).convert("RGBA")

        result = base_image.copy()
        x = result.width - watermark.width - 10
        y = result.height - watermark.height - 10
        result.paste(watermark, (x, y), mask=watermark)

        preview_image(result)
        base_image = result

def save_result():
    if base_image:
        path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if path:
            base_image.convert("RGB").save(path)

def preview_image(img):
    img_preview = img.copy()
    img_preview.thumbnail((400, 400))
    tk_img = ImageTk.PhotoImage(img_preview)
    canvas.delete("all")
    canvas.create_image(200, 200, image=tk_img)
    canvas.image = tk_img

root = tk.Tk()
root.title("Simple Watermark App")

base_image = None

tk.Button(root, text="Upload Image", command=upload_base_image).pack(pady=5)
tk.Button(root, text="Upload Watermark", command=upload_watermark).pack(pady=5)
tk.Button(root, text="Save Image", command=save_result).pack(pady=5)

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

root.mainloop()