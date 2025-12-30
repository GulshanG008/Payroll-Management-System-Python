# gui/components/table_widget.py

import tkinter as tk
from tkinter import ttk
from typing import Any, List, Tuple


class TableWidget(tk.Frame):
    def __init__(
        self,
        parent,
        columns: List[Tuple[str, str, int]],
        height: int = 10,
        select_mode: str = "browse",
    ):
        super().__init__(parent)

        self.columns = columns
        self._build_table(height, select_mode)

    def _build_table(self, height, select_mode):
        column_ids = [col[0] for col in self.columns]

        self.tree = ttk.Treeview(
            self,
            columns=column_ids,
            show="headings",
            height=height,
            selectmode=select_mode,
        )

        # Scrollbars
        y_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Define columns
        for col_id, heading, width in self.columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, anchor="center")

        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def insert_row(self, values: Tuple[Any, ...]):
        self.tree.insert("", "end", values=values)

    def insert_rows(self, rows: List[Tuple[Any, ...]]):
        for row in rows:
            self.insert_row(row)

    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def get_selected_row(self) -> Tuple[Any, ...] | None:
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected)["values"]

    def bind_select(self, callback):
        self.tree.bind("<<TreeviewSelect>>", callback)
