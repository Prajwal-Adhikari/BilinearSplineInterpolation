import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

def bilinear_spline_interpolation(img, scale):
    # Get image dimensions
    height, width, channels = img.shape

    # Calculate new dimensions
    new_height = int(height * scale)
    new_width = int(width * scale)

    # Create empty image with new dimensions
    new_img = np.zeros((new_height, new_width, channels), dtype=np.uint8)

    # Calculate scaling ratios
    x_ratio = float(width - 1) / (new_width - 1) if new_width > 1 else 0
    y_ratio = float(height - 1) / (new_height - 1) if new_height > 1 else 0

    # Apply bilinear spline interpolation
    for y in range(new_height):
        for x in range(new_width):
            x_val = x * x_ratio
            y_val = y * y_ratio
            x_min = int(x_val)
            y_min = int(y_val)
            x_max = min(x_min + 1, width - 1)
            y_max = min(y_min + 1, height - 1)
            x_diff = x_val - x_min
            y_diff = y_val - y_min

            # Fit bilinear spline to surrounding pixels
            p00 = img[y_min, x_min]
            p01 = img[y_min, x_max]
            p10 = img[y_max, x_min]
            p11 = img[y_max, x_max]

            a = p00
            b = p01 - p00
            c = p10 - p00
            d = p11 + p00 - p01 - p10

            # Calculate interpolated pixel value using bilinear spline
            new_img[y, x] = a + b * x_diff + c * y_diff + d * x_diff * y_diff

    return new_img

def open_image():
    global img_path, img_label
    img_path = filedialog.askopenfilename(initialdir='/', title='Select Image',
                                          filetypes=(('Image Files', ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif')),))

    if img_path:
        load_image(img_path)

def load_image(path):
    global img, img_label
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_resized = img_pil.resize((400, 400), resample=Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    if img_label is None:
        img_label = tk.Label(root, image=img_tk)
        img_label.image = img_tk
        img_label.pack()
    else:
        img_label.configure(image=img_tk)
        img_label.image = img_tk

def resize_image():
    global img, scale_entry, scaled_img_label

    scale = float(scale_entry.get())

    if img is not None:
        # Scale image using bilinear spline interpolation
        scaled_img = bilinear_spline_interpolation(img, scale)
        scaled_img_rgb = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2RGB)
        scaled_img_pil = Image.fromarray(scaled_img_rgb)
        scaled_img_resized = scaled_img_pil.resize((400, 400), resample=Image.LANCZOS)
        scaled_img_tk = ImageTk.PhotoImage(scaled_img_resized)

        if scaled_img_label is None:
            scaled_img_label = tk.Label(root, image=scaled_img_tk)
            scaled_img_label.image = scaled_img_tk
            scaled_img_label.pack()
        else:
            scaled_img_label.configure(image=scaled_img_tk)
            scaled_img_label.image = scaled_img_tk

        save_path = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=(('JPEG', '*.jpg'), ('PNG', '*.png')))
        if save_path:
            scaled_img_pil.save(save_path)
            print("Resized image saved successfully.")

root = tk.Tk()
root.title("Bilinear Spline Interpolation")
root.geometry("800x600")

img_label = None
scaled_img_label = None
img_path = None
img = None

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(pady=10)

scale_label = tk.Label(root, text="Scale Factor:")
scale_label.pack()

scale_entry = tk.Entry(root)
scale_entry.pack()

resize_button = tk.Button(root, text="Resize Image", command=resize_image)
resize_button.pack(pady=10)

root.mainloop()
