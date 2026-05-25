import tkinter as tk
from tkinter import font
import qrcode
from PIL import ImageTk, Image

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.qr_image = None
        self._build_ui()

    def _build_ui(self):
        # Title
        tk.Label(
            self.root, text="QR Code Generator",
            bg="#1e1e2e", fg="#cdd6f4",
            font=("Arial", 20, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            self.root, text="Enter text or URL below",
            bg="#1e1e2e", fg="#6e6e8e",
            font=("Arial", 11)
        ).pack()

        # Input box
        self.input_field = tk.Entry(
            self.root,
            width=35,
            font=("Arial", 14),
            bg="#313149",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat",
            justify="center"
        )
        self.input_field.pack(pady=15, ipady=8, padx=20)
        self.input_field.focus()

        # Generate button
        tk.Button(
            self.root, text="Generate QR",
            bg="#a6e3a1", fg="#1e1e2e",
            font=("Arial", 13, "bold"),
            relief="flat", cursor="hand2",
            activebackground="#a6e3a1",
            command=self._generate_qr,
            width=20
        ).pack(pady=(0, 15), ipady=8)

        # QR display area
        self.qr_label = tk.Label(
            self.root,
            bg="#1e1e2e",
            text="Your QR code will appear here",
            fg="#6e6e8e",
            font=("Arial", 11)
        )
        self.qr_label.pack(pady=10)

        # Status label
        self.status_label = tk.Label(
            self.root, text="",
            bg="#1e1e2e", fg="#f38ba8",
            font=("Arial", 10)
        )
        self.status_label.pack()

        # Padding at bottom
        tk.Label(self.root, bg="#1e1e2e").pack(pady=10)

    def _generate_qr(self):
        text = self.input_field.get().strip()

        if not text:
            self.status_label.config(text="⚠️ Please enter some text or URL!", fg="#f38ba8")
            return

        # Generate QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#1e1e2e", back_color="white")
        img = img.resize((250, 250), Image.LANCZOS)

        self.qr_image = ImageTk.PhotoImage(img)
        self.qr_label.config(image=self.qr_image, text="")
        self.status_label.config(text="✅ QR code generated!", fg="#a6e3a1")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()