from __future__ import annotations

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from .generator import build_qr_options, create_qr_image
from .history import HistoryEntry, add_history_entry, load_history


class QRCodeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("760x640")
        self.minsize(680, 560)
        self.preview_image: ImageTk.PhotoImage | None = None
        self.last_output_path: Path | None = None

        self._configure_theme()
        self._build_layout()
        self._refresh_history()

    def _configure_theme(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Hint.TLabel", foreground="#5f6b7a")
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        root = ttk.Frame(self, padding=24)
        root.grid(row=0, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)

        title = ttk.Label(root, text="QR Code Generator", style="Title.TLabel")
        title.grid(row=0, column=0, sticky="w")

        subtitle = ttk.Label(root, text="Create QR code images from text or links.", style="Hint.TLabel")
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 20))

        input_group = ttk.LabelFrame(root, text="Content", padding=16)
        input_group.grid(row=2, column=0, sticky="ew")
        input_group.columnconfigure(0, weight=1)

        ttk.Label(input_group, text="Text or link").grid(row=0, column=0, sticky="w")
        self.data_text = tk.Text(input_group, height=6, wrap="word")
        self.data_text.grid(row=1, column=0, sticky="ew", pady=(6, 0))

        preview_group = ttk.LabelFrame(root, text="Preview", padding=16)
        preview_group.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        preview_group.columnconfigure(0, weight=1)
        self.preview_label = ttk.Label(preview_group, text="QR preview will appear here.", anchor="center")
        self.preview_label.grid(row=0, column=0, sticky="ew")

        history_group = ttk.LabelFrame(root, text="Recent QR codes", padding=16)
        history_group.grid(row=4, column=0, sticky="ew", pady=(16, 0))
        history_group.columnconfigure(0, weight=1)
        self.history_list = tk.Listbox(history_group, height=5, activestyle="none")
        self.history_list.grid(row=0, column=0, sticky="ew")

        output_group = ttk.LabelFrame(root, text="Output", padding=16)
        output_group.grid(row=5, column=0, sticky="ew", pady=(16, 0))
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

        settings_group = ttk.LabelFrame(root, text="Style", padding=16)
        settings_group.grid(row=6, column=0, sticky="ew", pady=(16, 0))
        settings_group.columnconfigure(1, weight=1)
        settings_group.columnconfigure(3, weight=1)

        self.box_size_var = tk.IntVar(value=10)
        self.border_var = tk.IntVar(value=4)
        self.fill_var = tk.StringVar(value="black")
        self.back_var = tk.StringVar(value="white")

        ttk.Label(settings_group, text="Box size").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(settings_group, from_=1, to=40, textvariable=self.box_size_var, width=8).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(10, 24),
        )
        ttk.Label(settings_group, text="Border").grid(row=0, column=2, sticky="w")
        ttk.Spinbox(settings_group, from_=0, to=20, textvariable=self.border_var, width=8).grid(
            row=0,
            column=3,
            sticky="w",
            padx=(10, 0),
        )

        ttk.Label(settings_group, text="Fill color").grid(row=1, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(settings_group, textvariable=self.fill_var).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 24),
            pady=(12, 0),
        )
        ttk.Label(settings_group, text="Background").grid(row=1, column=2, sticky="w", pady=(12, 0))
        ttk.Entry(settings_group, textvariable=self.back_var).grid(
            row=1,
            column=3,
            sticky="ew",
            padx=(10, 0),
            pady=(12, 0),
        )

        actions = ttk.Frame(root)
        actions.grid(row=7, column=0, sticky="ew", pady=(20, 0))
        actions.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(actions, textvariable=self.status_var, style="Hint.TLabel").grid(row=0, column=0, sticky="w")
        self.open_folder_button = ttk.Button(actions, text="Open folder", command=self._open_output_folder)
        self.open_folder_button.grid(row=0, column=1, sticky="e", padx=(0, 10))
        ttk.Button(actions, text="Generate", style="Accent.TButton", command=self._generate).grid(
            row=0,
            column=2,
            sticky="e",
        )

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
            options = build_qr_options(
                box_size=self.box_size_var.get(),
                border=self.border_var.get(),
                fill_color=self.fill_var.get(),
                back_color=self.back_var.get(),
            )
            image = create_qr_image(data, options)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path)
        except ValueError as error:
            self.status_var.set(str(error))
            messagebox.showerror("Cannot generate QR code", str(error))
            return
        except OSError as error:
            self.status_var.set("Failed to save QR code.")
            messagebox.showerror("Cannot save QR code", str(error))
            return

        result = output_path.resolve()
        self.last_output_path = result
        self._show_preview(image)
        self._refresh_history(add_history_entry(data, result))
        self.status_var.set(f"Saved to {result}")
        messagebox.showinfo("QR code generated", f"Saved to:\n{result}")

    def _show_preview(self, image: Image.Image) -> None:
        preview = image.convert("RGB")
        preview.thumbnail((220, 220))
        self.preview_image = ImageTk.PhotoImage(preview)
        self.preview_label.configure(image=self.preview_image, text="")

    def _refresh_history(self, entries: list[HistoryEntry] | None = None) -> None:
        entries = entries or load_history()
        self.history_list.delete(0, tk.END)
        if not entries:
            self.history_list.insert(tk.END, "No saved QR codes yet.")
            return

        for entry in entries:
            self.history_list.insert(tk.END, f"{entry.created_at} - {entry.data} -> {entry.output_path}")

    def _open_output_folder(self) -> None:
        target_path = self.last_output_path or Path(self.output_var.get().strip() or "output")
        folder = target_path if target_path.is_dir() else target_path.parent
        folder.mkdir(parents=True, exist_ok=True)
        os.startfile(folder.resolve())


def run_gui() -> None:
    app = QRCodeApp()
    app.mainloop()
