import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import ImageTk, Image


class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.qr_image = None
        self.raw_image = None
        self._build_ui()
        self._bind_keyboard()

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
            self.root, width=35,
            font=("Arial", 14),
            bg="#313149", fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat", justify="center"
        )
        self.input_field.pack(pady=15, ipady=8, padx=20)
        self.input_field.focus()

        # Buttons row
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=(0, 15))

        tk.Button(
            btn_frame, text="Generate QR",
            bg="#a6e3a1", fg="#1e1e2e",
            font=("Arial", 13, "bold"),
            relief="flat", cursor="hand2",
            activebackground="#a6e3a1",
            command=self._generate_qr,
            width=14
        ).grid(row=0, column=0, padx=5, ipady=8)

        tk.Button(
            btn_frame, text="Save QR",
            bg="#89b4fa", fg="#1e1e2e",
            font=("Arial", 13, "bold"),
            relief="flat", cursor="hand2",
            activebackground="#89b4fa",
            command=self._save_qr,
            width=10
        ).grid(row=0, column=1, padx=5, ipady=8)

        tk.Button(
            btn_frame, text="Clear",
            bg="#f38ba8", fg="#1e1e2e",
            font=("Arial", 13, "bold"),
            relief="flat", cursor="hand2",
            activebackground="#f38ba8",
            command=self._clear,
            width=8
        ).grid(row=0, column=2, padx=5, ipady=8)

        # QR display area
        self.qr_label = tk.Label(
            self.root, bg="#1e1e2e",
            text="Your QR code will appear here",
            fg="#6e6e8e", font=("Arial", 11)
        )
        self.qr_label.pack(pady=10)

        # Status label
        self.status_label = tk.Label(
            self.root, text="",
            bg="#1e1e2e", fg="#f38ba8",
            font=("Arial", 10)
        )
        self.status_label.pack()

        tk.Label(self.root, bg="#1e1e2e").pack(pady=10)

    def _bind_keyboard(self):
        self.root.bind("<Return>", lambda e: self._generate_qr())
        self.root.bind("<Escape>", lambda e: self._clear())

    def _generate_qr(self):
        text = self.input_field.get().strip()

        if not text:
            self.status_label.config(
                text=" Please enter some text or URL!", fg="#f38ba8"
            )
            return

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

        self.raw_image = img
        self.qr_image = ImageTk.PhotoImage(img)
        self.qr_label.config(image=self.qr_image, text="")
        self.status_label.config(text=" QR code generated! Press Enter to regenerate.", fg="#a6e3a1")

    def _save_qr(self):
        if self.raw_image is None:
            self.status_label.config(
                text=" Generate a QR code first!", fg="#f38ba8"
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="qrcode.png"
        )

        if file_path:
            self.raw_image.save(file_path)
            self.status_label.config(
                text=f" Saved to {file_path}", fg="#a6e3a1"
            )

    def _clear(self):
        self.input_field.delete(0, tk.END)
        self.qr_label.config(image="", text="Your QR code will appear here")
        self.qr_image = None
        self.raw_image = None
        self.status_label.config(text="")
        self.input_field.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()