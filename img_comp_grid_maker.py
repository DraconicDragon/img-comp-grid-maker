import os
import sys
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

# NOTE: pip install tkinterdnd2-universal because tkinterdnd2 is broken on linux
# to build with nuitka change TkinterPlugin.py to search for win-x64 and linux-x64 instead of win64 and linux64 at around L143


class ImageComparisonTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Comparison Grid Maker Tool Thing")
        self.root.configure(bg="#202020")  # main window

        if os.name == "nt":  # set dark title bar on Windows https://github.com/alijafari79/Tkinter_dark_Title_bar
            import ctypes as ct

            def dark_title_bar(window):
                window.update()
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
                get_parent = ct.windll.user32.GetParent
                hwnd = get_parent(window.winfo_id())
                rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
                value = 2
                value = ct.c_int(value)
                set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))

            dark_title_bar(self.root)

        # drag-and-drop support
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.drop_files)

        self.image_entries = []  # tuples (image_path, caption)

        self.frame = tk.Frame(self.root, bg="#202020")
        self.frame.pack(padx=4, pady=4, fill="x")

        self.canvas = tk.Canvas(
            self.frame,
            width=700,
            height=350,
            bg="#202020",
            highlightcolor="#202020",
            highlightbackground="#202020",
            highlightthickness=0,  # some of this probably doesnt even do anything
        )
        self.canvas.pack(fill="both", expand=True)

        self.generate_button = tk.Button(
            self.frame,
            text="Generate Comparison Image Grid Thing",
            command=self.generate_image,
            bg="#3c3c3c",
            fg="#ffffff",
            relief="solid",
            activebackground="#1e1e1e",
            activeforeground="#ffffff",
        )
        self.generate_button.pack(pady=4)

    def drop_files(self, event):
        # file paths from file drop event
        file_paths = self.root.tk.splitlist(event.data)
        for file_path in file_paths:
            self.add_image(file_path)

    def add_image(self, image_path):
        # frame as container for image and caption
        entry_frame = tk.Frame(self.canvas, bg="#202020")
        entry_frame.pack(side="left", padx=5)

        # image display
        img = Image.open(image_path)
        img.thumbnail((272, 272))
        img = ImageTk.PhotoImage(img)
        label = tk.Label(entry_frame, image=img, bg="#2e2e2e")
        label.image = img  # this because Garbage Collection is cringe, more like cringe collection. im not funny
        label.pack()

        # Caption entry textbox
        caption_entry = tk.Entry(entry_frame, width=42, bg="#3c3c3c", fg="#ffffff", insertbackground="white")
        caption_entry.pack()
        caption_entry.insert(0, "Enter caption")

        # right-click to remove
        def remove_image(event):
            entry_frame.destroy()
            self.image_entries = [(path, entry) for path, entry in self.image_entries if entry != caption_entry]

        label.bind("<ButtonRelease-3>", remove_image)

        self.image_entries.append((image_path, caption_entry))

    def generate_image(self):
        if not self.image_entries:
            messagebox.showwarning("Warning", "No images to generate.")
            return

        images = []
        captions = []
        total_width = 0
        max_height = 0

        for image_path, caption_entry in self.image_entries:
            caption = caption_entry.get()
            captions.append(caption)

            img = Image.open(image_path)
            images.append(img)

            total_width += img.width
            max_height = max(max_height, img.height)

        # TODO: make better math for fitting in font inside white space
        # the white space for captions above the images
        comparison_image = Image.new("RGB", (total_width, max_height + 128), (255, 255, 255))
        draw = ImageDraw.Draw(comparison_image)

        x_offset = 0
        for img, caption in zip(images, captions):
            comparison_image.paste(img, (x_offset, 128))

            # Initial font size
            original_font_size = 120
            font_size = original_font_size

            if os.name == "nt":
                font_path = "arial.ttf"
            else:
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
                # Update this path if necessary
            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), caption, font=font)
            text_width = bbox[2] - bbox[0]

            # Calculate 45% threshold for font size
            font_size_threshold = int(original_font_size * 0.45)

            while text_width > img.width and font_size > font_size_threshold:
                font_size -= 1
                font = ImageFont.truetype(font_path, font_size)
                bbox = draw.textbbox((0, 0), caption, font=font)
                text_width = bbox[2] - bbox[0]

            # If the font size is below the 45% threshold, we break the text into two lines
            if font_size <= font_size_threshold:
                words = caption.split()
                first_line = ""
                second_line = ""
                for word in words:
                    # Temporarily append the word to see if it fits in the first line
                    if draw.textbbox((0, 0), first_line + word + " ", font=font)[2] - bbox[0] <= img.width:
                        first_line += word + " "
                    else:
                        second_line += word + " "

                # Adjust positions for two lines
                first_bbox = draw.textbbox((0, 0), first_line, font=font)
                second_bbox = draw.textbbox((0, 0), second_line, font=font)

                first_text_width = first_bbox[2] - first_bbox[0]
                second_text_width = second_bbox[2] - second_bbox[0]

                # Center each line horizontally
                first_text_x = x_offset + (img.width - first_text_width) // 2
                second_text_x = x_offset + (img.width - second_text_width) // 2

                # Vertically adjust for the height of two lines
                font_ascent, font_descent = font.getmetrics()
                first_text_height = first_bbox[3] - first_bbox[1] + font_descent
                second_text_height = second_bbox[3] - second_bbox[1] + font_descent
                total_height = first_text_height + second_text_height

                first_text_y = (128 - total_height) // 2 - 4
                second_text_y = first_text_y + first_text_height

                # Draw the two lines of text
                draw.text((first_text_x, first_text_y), first_line.strip(), font=font, fill="black")
                draw.text((second_text_x, second_text_y), second_line.strip(), font=font, fill="black")
            else:
                # Center the single line of text vertically and horizontally
                text_x = x_offset + (img.width - text_width) // 2
                font_ascent, font_descent = font.getmetrics()
                text_height = bbox[3] - bbox[1] + font_descent
                text_y = (128 - text_height) // 2 - 8
                draw.text((text_x, text_y), caption, font=font, fill="black")

            x_offset += img.width

        # saves image to same path as script/exe location
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Save the image to the base directory
        save_path = os.path.join(base_dir, "comparison_image.jpg")
        comparison_image.save(save_path)
        messagebox.showinfo("Success", f"Comparison image generated as '{save_path}'.")


if __name__ == "__main__":
    root = TkinterDnD.Tk()  # using TkinterDnD.Tk() so drag-and-drop works
    app = ImageComparisonTool(root)
    root.mainloop()
