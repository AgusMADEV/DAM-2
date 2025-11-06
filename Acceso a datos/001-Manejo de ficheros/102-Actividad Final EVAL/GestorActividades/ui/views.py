import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gestor Personal de Actividades')
        self.geometry('900x600')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tabs
        self.tab_list = ttk.Frame(self.notebook)
        self.tab_form = ttk.Frame(self.notebook)
        self.tab_stats = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_list, text='Lista')
        self.notebook.add(self.tab_form, text='Formulario')
        self.notebook.add(self.tab_stats, text='Estadísticas')

        self._build_list_tab()
        self._build_form_tab()
        self._build_stats_tab()

    def _build_list_tab(self):
        top = ttk.Frame(self.tab_list)
        top.pack(fill=tk.X, padx=6, pady=6)
        ttk.Label(top, text='Filtro:').pack(side=tk.LEFT)
        self.filter_entry = ttk.Entry(top)
        self.filter_entry.pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text='Buscar').pack(side=tk.LEFT, padx=4)

        columns = ('id', 'title', 'category', 'date', 'duration')
        self.tree = ttk.Treeview(self.tab_list, columns=columns, show='headings')
        headings = ('ID', 'Título', 'Categoría', 'Fecha', 'Duración')
        for col, text in zip(columns, headings):
            self.tree.heading(col, text=text)
            # establecer un ancho aproximado para cada columna
            if col == 'id':
                self.tree.column(col, width=0, stretch=False)
            elif col == 'title':
                self.tree.column(col, width=240)
            elif col == 'category':
                self.tree.column(col, width=120)
            elif col == 'date':
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=80)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def _build_form_tab(self):
        frm = ttk.Frame(self.tab_form, padding=8)
        frm.pack(fill=tk.X)
        ttk.Label(frm, text='Título:').grid(row=0, column=0, sticky='w')
        self.title_var = tk.StringVar(); ttk.Entry(frm, textvariable=self.title_var, width=40).grid(row=0, column=1, sticky='w')
        ttk.Label(frm, text='Categoría:').grid(row=1, column=0, sticky='w')
        self.cat_var = tk.StringVar(); ttk.Entry(frm, textvariable=self.cat_var).grid(row=1, column=1, sticky='w')
        ttk.Label(frm, text='Fecha (YYYY-MM-DD):').grid(row=2, column=0, sticky='w')
        self.date_var = tk.StringVar(); ttk.Entry(frm, textvariable=self.date_var).grid(row=2, column=1, sticky='w')
        ttk.Label(frm, text='Duración (min):').grid(row=3, column=0, sticky='w')
        self.dur_var = tk.StringVar(value='60'); ttk.Entry(frm, textvariable=self.dur_var).grid(row=3, column=1, sticky='w')
        ttk.Label(frm, text='Notas:').grid(row=4, column=0, sticky='nw')
        self.notes_text = tk.Text(frm, height=6, width=50); self.notes_text.grid(row=4, column=1, sticky='w')

        btns = ttk.Frame(frm); btns.grid(row=5, column=0, columnspan=2, pady=8)
        self.add_btn = ttk.Button(btns, text='Añadir')
        self.add_btn.pack(side=tk.LEFT, padx=4)
        self.update_btn = ttk.Button(btns, text='Actualizar')
        self.update_btn.pack(side=tk.LEFT, padx=4)
        self.delete_btn = ttk.Button(btns, text='Eliminar')
        self.delete_btn.pack(side=tk.LEFT, padx=4)

    def _build_stats_tab(self):
        self.stats_canvas = tk.Canvas(self.tab_stats, bg='white')
        self.stats_canvas.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    # helper methods for controller bindings
    def set_on_add(self, fn: Callable):
        self.add_btn.config(command=fn)

    def set_on_update(self, fn: Callable):
        self.update_btn.config(command=fn)

    def set_on_delete(self, fn: Callable):
        self.delete_btn.config(command=fn)
