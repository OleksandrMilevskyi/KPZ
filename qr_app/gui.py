from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class QRCodeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("720x520")
        self.minsize(640, 460)

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        root = ttk.Frame(self, padding=24)
        root.grid(row=0, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)

        title = ttk.Label(root, text="QR Code Generator", font=("Segoe UI", 20, "bold"))
        title.grid(row=0, column=0, sticky="w")

        subtitle = ttk.Label(root, text="Create QR code images from text or links.")
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 20))

        input_group = ttk.LabelFrame(root, text="Content", padding=16)
        input_group.grid(row=2, column=0, sticky="ew")
        input_group.columnconfigure(0, weight=1)

        ttk.Label(input_group, text="Text or link").grid(row=0, column=0, sticky="w")
        self.data_text = tk.Text(input_group, height=6, wrap="word")
        self.data_text.grid(row=1, column=0, sticky="ew", pady=(6, 0))

        output_group = ttk.LabelFrame(root, text="Output", padding=16)
        output_group.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        output_group.columnconfigure(1, weight=1)

        ttk.Label(output_group, text="File").grid(row=0, column=0, sticky="w")
        self.output_var = tk.StringVar(value="output/qr-code.png")
        output_entry = ttk.Entry(output_group, textvariable=self.output_var)
        output_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        actions = ttk.Frame(root)
        actions.grid(row=4, column=0, sticky="ew", pady=(20, 0))
        actions.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(actions, textvariable=self.status_var).grid(row=0, column=0, sticky="w")
        ttk.Button(actions, text="Generate").grid(row=0, column=1, sticky="e")


def run_gui() -> None:
    app = QRCodeApp()
    app.mainloop()
