# gui/components/input_form.py

import tkinter as tk
from typing import Dict, List


class InputForm(tk.Frame):
    def __init__(
        self, parent, fields: List[str], entry_width: int = 25, label_width: int = 15
    ):
        super().__init__(parent)

        self.fields = fields
        self.entries: Dict[str, tk.Entry] = {}

        self._build_form(entry_width, label_width)

    def _build_form(self, entry_width, label_width):
        for row, field in enumerate(self.fields):
            label = tk.Label(self, text=f"{field}:", anchor="w", width=label_width)
            label.grid(row=row, column=0, padx=5, pady=6, sticky="w")

            entry = tk.Entry(self, width=entry_width)
            entry.grid(row=row, column=1, padx=5, pady=6)

            self.entries[field] = entry

    def get_data(self) -> Dict[str, str]:
        return {field: entry.get().strip() for field, entry in self.entries.items()}

    def set_data(self, data: Dict[str, str]):
        """
        Populate form fields from a dictionary.
        """
        for field, value in data.items():
            if field in self.entries:
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, value)

    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def get_entry(self, field: str) -> tk.Entry:
        return self.entries.get(field)
