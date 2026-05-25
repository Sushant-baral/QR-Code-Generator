import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import ImageTk, Image


class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Generator")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")

        self.qr_image = None
        self.raw_image = None
        self._build_ui()
        self._bind_keyboard()

    def _build_ui(self):
        # Top bar
        top_bar = tk.Frame(self.root, bg="#f7f7f5", height=50)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        tk.Label(
            top_bar, text="⬛ QR Generator",
            bg="#f7f7f5", fg="#1a1a1a",
            font=("Helvetica Neue", 13, "bold")
        ).pack(side="left", padx=20, pady=12)

        tk.Label(
            top_bar, text="by Sushant",
            bg="#f7f7f5", fg="#a0a0a0",
            font=("Helvetica Neue", 11)
        ).pack(side="right", padx=20, pady=12)

        # Divider
        tk.Frame(self.root, bg="#e8e8e5", height=1).pack(fill="x")

        # Main content
        content = tk.Frame(self.root, bg="#ffffff")
        content.pack(padx=40, pady=30)

        # Heading
        tk.Label(
            content, text="Generate a QR Code",
            bg="#ffffff", fg="#1a1a1a",
            font=("Helvetica Neue", 22, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        tk.Label(
            content, text="Paste a URL, write text, anything.",
            bg="#ffffff", fg="#a0a0a0",
            font=("Helvetica Neue", 12),
            anchor="w"
        ).pack(fill="x", pady=(0, 20))

        # Input label
        tk.Label(
            content, text="INPUT",
            bg="#ffffff", fg="#a0a0a0",
            font=("Helvetica Neue", 9, "bold"),
            anchor="w"
        ).pack(fill="x")

        # Input box with border simulation
        input_wrapper = tk.Frame(content, bg="#e8e8e5", padx=1, pady=1)
        input_wrapper.pack(fill="x", pady=(4, 20))

        self.input_field = tk.Entry(
            input_wrapper,
            width=38,
            font=("Helvetica Neue", 13),
            bg="#fafafa",
            fg="#1a1a1a",
            insertbackground="#1a1a1a",
            relief="flat",
        )
        self.input_field.pack(ipady=10, padx=10)
        self.input_field.focus()

        # Buttons row
        btn_frame = tk.Frame(content, bg="#ffffff")
        btn_frame.pack(fill="x", pady=(0, 24))

        tk.Button(
            btn_frame, text="Generate",
            bg="#1a1a1a", fg="#ffffff",
            font=("Helvetica Neue", 12, "bold"),
            relief="flat", cursor="hand2",
            activebackground="#333333",
            activeforeground="#ffffff",
            command=self._generate_qr,
            padx=20
        ).pack(side="left", ipady=8, padx=(0, 8))

        tk.Button(
            btn_frame, text="Save PNG",
            bg="#f0f0ee", fg="#1a1a1a",
            font=("Helvetica Neue", 12),
            relief="flat", cursor="hand2",
            activebackground="#e0e0de",
            activeforeground="#1a1a1a",
            command=self._save_qr,
            padx=20
        ).pack(side="left", ipady=8, padx=(0, 8))

        tk.Button(
            btn_frame, text="Clear",
            bg="#f0f0ee", fg="#1a1a1a",
            font=("Helvetica Neue", 12),
            relief="flat", cursor="hand2",
            activebackground="#e0e0de",
            activeforeground="#1a1a1a",
            command=self._clear,
            padx=20
        ).pack(side="left", ipady=8)

        # Divider
        tk.Frame(content, bg="#e8e8e5", height=1).pack(fill="x", pady=(0, 20))

        # QR display area
        self.qr_label = tk.Label(
            content,
            bg="#ffffff",
            text="↑  Enter something above and hit Generate",
            fg="#c0c0c0",
            font=("Helvetica Neue", 11),
            padx=10,
            pady=10
        )
        self.qr_label.pack()

        # Status
        self.status_label = tk.Label(
            content, text="",
            bg="#ffffff", fg="#a0a0a0",
            font=("Helvetica Neue", 10),
            anchor="w"
        )
        self.status_label.pack(fill="x", pady=(12, 0))

    def _bind_keyboard(self):
        self.root.bind("<Return>", lambda e: self._generate_qr())
        self.root.bind("<Escape>", lambda e: self._clear())

    def _generate_qr(self):
        text = self.input_field.get().strip()

        if not text:
            self.status_label.config(text="⚠  Please enter some text or a URL.")
            return

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#1a1a1a", back_color="#ffffff")
        img = img.resize((250, 250), Image.LANCZOS)

        self.raw_image = img
        self.qr_image = ImageTk.PhotoImage(img)
        self.qr_label.config(image=self.qr_image, text="")
        self.status_label.config(text="✓  QR code ready — scan or save it.")

    def _save_qr(self):
        if self.raw_image is None:
            self.status_label.config(text="⚠  Generate a QR code first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="qrcode.png"
        )

        if file_path:
            self.raw_image.save(file_path)
            self.status_label.config(text=f"✓  Saved to {file_path}")

    def _clear(self):
        self.input_field.delete(0, tk.END)
        self.qr_label.config(
            image="",
            text="↑  Enter something above and hit Generate"
        )
        self.qr_image = None
        self.raw_image = None
        self.status_label.config(text="")
        self.input_field.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()