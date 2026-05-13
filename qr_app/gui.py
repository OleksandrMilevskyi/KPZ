from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .generator import QRCodeOptions, generate_qr_code


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
        ttk.Button(output_group, text="Browse", command=self._choose_output_file).grid(
            row=0,
            column=2,
            sticky="e",
            padx=(10, 0),
        )

        actions = ttk.Frame(root)
        actions.grid(row=4, column=0, sticky="ew", pady=(20, 0))
        actions.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(actions, textvariable=self.status_var).grid(row=0, column=0, sticky="w")
        ttk.Button(actions, text="Generate", command=self._generate).grid(row=0, column=1, sticky="e")

    def _choose_output_file(self) -> None:
        filename = filedialog.asksaveasfilename(
            title="Save QR code",
            defaultextension=".png",
            filetypes=[("PNG image", "*.png"), ("All files", "*.*")],
        )
        if filename:
            self.output_var.set(filename)

    def _generate(self) -> None:
        data = self.data_text.get("1.0", "end").strip()
        output_path = Path(self.output_var.get().strip() or "output/qr-code.png")

        try:
            result = generate_qr_code(data, output_path, QRCodeOptions())
        except ValueError as error:
            self.status_var.set(str(error))
            messagebox.showerror("Cannot generate QR code", str(error))
            return
        except OSError as error:
            self.status_var.set("Failed to save QR code.")
            messagebox.showerror("Cannot save QR code", str(error))
            return

        self.status_var.set(f"Saved to {result}")
        messagebox.showinfo("QR code generated", f"Saved to:\n{result}")


def run_gui() -> None:
    app = QRCodeApp()
    app.mainloop()
