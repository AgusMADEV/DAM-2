import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json, csv, uuid, re
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from domain import Appointment
from storage import JsonAppointmentRepo
from services import AgendaService, SlotEngine, AppointmentStats
from validators import v_fecha, v_hora, v_telefono

class ModernAppointmentApp:
    def __init__(self, root):
        self.root = root
        # Paleta de colores moderna
        self.colors = {
            'primary': '#2563eb',      # Azul moderno
            'success': '#16a34a',      # Verde moderno
            'warning': '#eab308',      # Amarillo moderno
            'danger': '#dc2626',       # Rojo moderno
            'background': '#f8fafc',   # Fondo claro
            'surface': '#ffffff',      # Superficie
            'text': '#1e293b',        # Texto principal
            'text-secondary': '#64748b' # Texto secundario
        }
        
        # Configurar tema general
        self.root.configure(bg=self.colors['background'])
        style = ttk.Style()
        # Intentar usar tema 'clam' para que los estilos de botones y backgrounds se apliquen mejor
        try:
            style.theme_use('clam')
        except Exception:
            pass

        # Estilo general
        style.configure('.',
            background=self.colors['background'],
            foreground=self.colors['text'],
            font=('Segoe UI', 10)
        )

        # Mejor contraste para botones: especificar background/foreground y relief
        style.configure('Primary.TButton',
            background=self.colors['primary'],
            foreground='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat'
        )
        style.map('Primary.TButton',
            background=[('active', '#1d4ed8'), ('pressed', '#1e40af')],
            foreground=[('disabled', '#a1a1aa')]
        )

        style.configure('Success.TButton',
            background=self.colors['success'],
            foreground='white',
            font=('Segoe UI', 10),
            relief='flat'
        )
        style.map('Success.TButton',
            background=[('active', '#15803d'), ('pressed', '#166534')],
            foreground=[('disabled', '#a1a1aa')]
        )

        style.configure('Warning.TButton',
            background=self.colors['warning'],
            foreground='black',
            font=('Segoe UI', 10),
            relief='flat'
        )
        style.map('Warning.TButton',
            background=[('active', '#ca8a04'), ('pressed', '#a16207')],
            foreground=[('disabled', '#6b6b6b')]
        )

        style.configure('Danger.TButton',
            background=self.colors['danger'],
            foreground='white',
            font=('Segoe UI', 10),
            relief='flat'
        )
        style.map('Danger.TButton',
            background=[('active', '#b91c1c'), ('pressed', '#991b1b')],
            foreground=[('disabled', '#a1a1aa')]
        )

        # Configuración común para todos los botones
        style.configure('TButton',
            padding=(12, 6),
            background=self.colors['surface'],
            foreground=self.colors['text']
        )
        
        # Frames
        style.configure('Card.TFrame',
            background=self.colors['surface'],
            relief='flat',
            borderwidth=1
        )
        
        # Labels
        style.configure('Header.TLabel',
            font=('Segoe UI', 12, 'bold'),
            foreground=self.colors['text'],
            background=self.colors['background'],
            padding=(0, 10)
        )
        
        style.configure('Caption.TLabel',
            font=('Segoe UI', 9),
            foreground=self.colors['text-secondary'],
            background=self.colors['background']
        )
        
        # Entradas
        style.configure('TEntry',
            padding=(10, 5),
            relief='flat',
            borderwidth=1
        )
        
        # Treeview con estilos mejorados
        style.configure('Treeview',
            background='white',
            fieldbackground='white',
            foreground=self.colors['text'],
            rowheight=30,
            font=('Segoe UI', 10)
        )
        style.map('Treeview',
            background=[('selected', '#e2e8f0')],
            foreground=[('selected', self.colors['text'])]
        )
        style.configure('Treeview.Heading',
            background='#f1f5f9',
            foreground=self.colors['text'],
            font=('Segoe UI', 10, 'bold'),
            padding=(10, 5),
            relief='flat'
        )
        style.map('Treeview.Heading',
            background=[('active', '#e2e8f0')]
        )
        
        # Notebook
        style.configure('TNotebook',
            background=self.colors['background'],
            tabmargins=[2, 5, 2, 0]
        )
        style.configure('TNotebook.Tab',
            padding=(15, 5),
            font=('Segoe UI', 10)
        )
        style.map('TNotebook.Tab',
            background=[('selected', self.colors['surface'])],
            expand=[('selected', [1, 1, 1, 0])]
        )
        # Inicializar servicios antes de crear la UI
        self.initialize_services()
        # Estado para filtrado/ordenación
        self._all_citas = []
        self._sort_col = None
        self._sort_reverse = False
        # Crear la interfaz
        self._ui()
        # Cargar datos iniciales
        self._refrescar()

    def _setup_tab_historial(self):
        """Stub mínimo para asegurar que el método existe antes de su uso."""
        # Si la pestaña ya está creada en _ui(), este método será reemplazado
        # por una implementación más completa más abajo en el archivo.
        if not hasattr(self, 'tab_historial'):
            self.tab_historial = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(self.tab_historial, text='📋 Historial')
        # implementación mínima: un label
        for child in getattr(self, 'tab_historial').winfo_children():
            child.destroy()
        ttk.Label(self.tab_historial, text='Historial (cargando...)').grid(row=0, column=0, padx=10, pady=10)

    def _ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(sticky='nsew')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky='nsew')
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Pestaña de Gestión de Citas
        self.tab_citas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_citas, text='📅 Gestión de Citas')
        
        # Pestaña de Historial y Seguimiento
        self.tab_historial = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_historial, text='📋 Historial')
        
        # Pestaña de Estadísticas
        self.tab_stats = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_stats, text='📊 Estadísticas')

        # Configurar cada pestaña
        self._setup_tab_citas()
        self._setup_tab_historial()
        self._setup_tab_stats()

    def _setup_tab_citas(self):
        """Configura la pestaña de gestión de citas"""
        # Frame principal con padding
        main_content = ttk.Frame(self.tab_citas, style='Card.TFrame')
        main_content.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        self.tab_citas.columnconfigure(0, weight=1)
        
        # Título de la sección
        ttk.Label(main_content, text='Gestión de Citas', style='Header.TLabel').grid(row=0, column=0, columnspan=2, sticky='w', padx=15, pady=(15,5))
        ttk.Label(main_content, text='Introduzca los datos de la cita', style='Caption.TLabel').grid(row=1, column=0, columnspan=2, sticky='w', padx=15, pady=(0,15))

        # Grid para el formulario
        form_grid = ttk.Frame(main_content, style='Card.TFrame')
        form_grid.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=15, pady=5)
        
        # Campos del formulario con más espacio
        campos = [
            ("Fecha", "fecha_var", "DD/MM/YYYY"),
            ("Hora", "hora_var", "HH:MM"),
            ("Paciente", "paciente_var", "Nombre completo"),
            ("Teléfono", "telefono_var", "Número de contacto"),
            ("Estado", "estado_var", None)
        ]
        
        for i, (label, var, placeholder) in enumerate(campos):
            # Label
            ttk.Label(form_grid, text=label + ":", style='Caption.TLabel').grid(row=i, column=0, sticky='w', padx=(0,10), pady=10)
            
            # Campo
            setattr(self, var, tk.StringVar())
            if var == "estado_var":
                # Combobox para estado
                estados = ['Programada', 'Atendida', 'Cancelada', 'No presentada', 'Reprogramada']
                cb = ttk.Combobox(form_grid, values=estados, textvariable=getattr(self, var), state='readonly', width=30)
                cb.set('Programada')
                cb.grid(row=i, column=1, sticky='ew', pady=10)
                setattr(self, 'estado_cb', cb)
            else:
                # Entry normal
                entry = ttk.Entry(form_grid, textvariable=getattr(self, var), width=32)
                if placeholder:
                    entry.insert(0, placeholder)
                    entry.bind('<FocusIn>', lambda e, entry=entry, ph=placeholder: self._on_entry_click(entry, ph))
                    entry.bind('<FocusOut>', lambda e, entry=entry, ph=placeholder: self._on_focus_out(entry, ph))
                entry.grid(row=i, column=1, sticky='ew', pady=10)
                setattr(self, f"{var.split('_')[0]}_entry", entry)

        # Descripción
        ttk.Label(form_grid, text="Descripción:", style='Caption.TLabel').grid(row=len(campos), column=0, sticky='w', padx=(0,10), pady=10)
        self.desc_text = tk.Text(form_grid, height=4, width=30, font=('Segoe UI', 10))
        self.desc_text.grid(row=len(campos), column=1, sticky='ew', pady=10)

        # Frame de botones con mejor espaciado
        btn_frame = ttk.Frame(main_content)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20, padx=15)

        ttk.Button(btn_frame, text="✚ Nueva Cita", 
                  command=self._nueva_cita, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✎ Actualizar", 
                  command=self._actualizar_cita, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", 
                  command=self._cancelar_cita, style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑 Eliminar",
                  command=self._eliminar_cita, style='Danger.TButton').pack(side=tk.LEFT, padx=5)

        # Lista de citas - título
        ttk.Label(main_content, text='Listado de Citas', style='Header.TLabel').grid(
            row=4, column=0, columnspan=2, sticky='w', padx=15, pady=(20,5))

        # Controles de filtrado (búsqueda, estado, fecha)
        filter_frame = ttk.Frame(main_content)
        filter_frame.grid(row=5, column=0, columnspan=2, sticky='ew', padx=15, pady=(0,10))
        filter_frame.columnconfigure(0, weight=1)
        filter_frame.columnconfigure(1, weight=0)
        filter_frame.columnconfigure(2, weight=0)
        filter_frame.columnconfigure(3, weight=0)

        # Campo de búsqueda
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=40)
        search_entry.grid(row=0, column=0, sticky='w', padx=(0,10))
        search_entry.insert(0, 'Buscar por paciente, teléfono o descripción')
        search_entry.bind('<FocusIn>', lambda e, entry=search_entry: entry.delete(0, tk.END) if entry.get().startswith('Buscar') else None)
        self.search_var.trace_add('write', lambda *args: self._on_search_change())

        # Filtro por estado
        estados = ['Todos', 'Programada', 'Atendida', 'Cancelada', 'No presentada', 'Reprogramada']
        self.state_filter_var = tk.StringVar(value='Todos')
        state_cb = ttk.Combobox(filter_frame, values=estados, textvariable=self.state_filter_var, state='readonly', width=22)
        state_cb.grid(row=0, column=1, sticky='e', padx=(0,10))
        state_cb.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())

        # Filtro por fecha exacta
        self.date_filter_var = tk.StringVar()
        date_entry = ttk.Entry(filter_frame, textvariable=self.date_filter_var, width=15)
        date_entry.grid(row=0, column=2, sticky='e', padx=(0,10))
        date_entry.insert(0, 'DD/MM/YYYY')
        date_entry.bind('<FocusIn>', lambda e, entry=date_entry: entry.delete(0, tk.END) if entry.get().startswith('DD') else None)
        date_entry.bind('<FocusOut>', lambda e: self._apply_filters())

        # Botón para limpiar filtros
        ttk.Button(filter_frame, text='Limpiar filtros', command=self._clear_filters).grid(row=0, column=3, sticky='e')
        # Import / Export
        ttk.Button(filter_frame, text='Exportar', command=self._export_dialog).grid(row=0, column=4, sticky='e', padx=(10,5))
        ttk.Button(filter_frame, text='Importar', command=self._import_dialog).grid(row=0, column=5, sticky='e')

        # Frame contenedor para la lista con borde y fondo (abajo)
        list_container = ttk.Frame(main_content, style='Card.TFrame')
        list_container.grid(row=6, column=0, columnspan=2, sticky='nsew', padx=15, pady=(0,15))
        main_content.rowconfigure(6, weight=1)
        main_content.columnconfigure(0, weight=1)

        # Treeview con mejor diseño
        cols = ('id', 'fecha', 'hora', 'paciente', 'telefono', 'estado', 'desc')
        self.tree = ttk.Treeview(list_container, columns=cols, show='headings', height=10)
        self.tree.grid(row=0, column=0, sticky='nsew', padx=(2,0), pady=2)
        list_container.rowconfigure(0, weight=1)
        list_container.columnconfigure(0, weight=1)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns', pady=2)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Asegurar que el scrollbar tenga suficiente altura
        list_container.grid_propagate(False)
        list_container.configure(height=250)

        # Configurar columnas con mejor ancho
        self.tree.column('id', width=0, stretch=False)
        self.tree.column('fecha', width=100)
        self.tree.column('hora', width=80)
        self.tree.column('paciente', width=200)
        self.tree.column('telefono', width=120)
        self.tree.column('estado', width=120)
        self.tree.column('desc', width=250)

        # Cabeceras más descriptivas y clicables para ordenar
        headers = {
            'id': '#',
            'fecha': 'Fecha',
            'hora': 'Hora',
            'paciente': 'Paciente',
            'telefono': 'Teléfono',
            'estado': 'Estado',
            'desc': 'Descripción'
        }
        for col in cols:
            # cada cabecera llamará a _on_heading_click
            self.tree.heading(col, text=headers.get(col, col.title()), command=lambda c=col: self._on_heading_click(c))

        # Enlazar selección del Treeview moderno
        self.tree.bind('<<TreeviewSelect>>', self._on_select)


    def _on_select(self, event):
        """Maneja la selección de una cita en el TreeView"""
        seleccion = self.tree.selection()
        if not seleccion:
            return
            
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        # Actualizar campos del formulario
        self.fecha_var.set(valores[1])  # fecha
        self.hora_var.set(valores[2])   # hora
        self.paciente_var.set(valores[3])  # paciente
        self.telefono_var.set(valores[4])  # teléfono
        # estado
        if hasattr(self, 'estado_var'):
            self.estado_var.set(valores[5])
        # descripción
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert('1.0', valores[6])  # descripción


    def _setup_tab_stats(self):
        """Configura la pestaña de estadísticas"""
        # Frame superior para estadísticas numéricas
        stats_frame = ttk.LabelFrame(self.tab_stats, text='Resumen de Actividad', padding=10)
        stats_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.tab_stats.columnconfigure(0, weight=1)

        # Variables para estadísticas
        self.stats_vars = {
            'total': tk.StringVar(value="0"),
            'programadas': tk.StringVar(value="0"),
            'atendidas': tk.StringVar(value="0"),
            'canceladas': tk.StringVar(value="0"),
            'reprogramadas': tk.StringVar(value="0"),
            'tiempo_espera': tk.StringVar(value="0")
        }

        # Mostrar estadísticas
        row = 0
        for key, label in [
            ('total', 'Total de Citas:'),
            ('programadas', 'Citas Programadas:'),
            ('atendidas', 'Citas Atendidas:'),
            ('canceladas', 'Citas Canceladas:'),
            ('reprogramadas', 'Citas Reprogramadas:'),
            ('tiempo_espera', 'Tiempo Medio de Espera (días):')
        ]:
            ttk.Label(stats_frame, text=label).grid(row=row, column=0, sticky='w', padx=5)
            ttk.Label(stats_frame, textvariable=self.stats_vars[key]).grid(row=row, column=1, padx=5)
            row += 1

        # Frame para visualización
        visual_frame = ttk.LabelFrame(self.tab_stats, text='Visualización de Estados', padding=10)
        visual_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.tab_stats.rowconfigure(1, weight=1)

        # Canvas para visualización simple de barras
        self.stats_canvas = tk.Canvas(visual_frame, width=400, height=200, bg='white')
        self.stats_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Botón para actualizar estadísticas
        ttk.Button(self.tab_stats, text="↻ Actualizar Estadísticas",
                  command=self._actualizar_estadisticas).grid(row=2, column=0, pady=10)

    def _actualizar_estadisticas(self):
        """Calcula y muestra estadísticas usando el servicio (si está disponible)."""
        stats = {}
        try:
            stats = self.service.obtener_estadisticas() if hasattr(self, 'service') else {}
        except Exception:
            stats = {}

        # Actualizar variables (usar 0 por defecto si falta)
        self.stats_vars['total'].set(str(stats.get('total', 0)))
        estados = stats.get('estados', {})
        self.stats_vars['programadas'].set(str(estados.get('Programada', 0)))
        self.stats_vars['atendidas'].set(str(estados.get('Atendida', 0)))
        self.stats_vars['canceladas'].set(str(estados.get('Cancelada', 0)))
        self.stats_vars['reprogramadas'].set(str(stats.get('reprogramaciones', 0)))
        self.stats_vars['tiempo_espera'].set(str(round(stats.get('tiempo_medio_espera', 0), 2)))

        # Dibujar una visualización simple en el canvas
        try:
            self.stats_canvas.delete('all')
            labels = ['Programada', 'Atendida', 'Cancelada']
            vals = [estados.get(k, 0) for k in labels]
            total = sum(vals) if sum(vals) > 0 else 1
            w = 300
            h = 150
            x = 10
            y = 10
            bar_w = (w - 20) / len(vals)
            colors = ['#007bff', '#28a745', '#dc3545']
            for i, v in enumerate(vals):
                bh = int((v / total) * h)
                self.stats_canvas.create_rectangle(x + i*bar_w, y + (h-bh), x + (i+1)*bar_w - 5, y + h, fill=colors[i])
                self.stats_canvas.create_text(x + i*bar_w + bar_w/2 - 5, y + h + 12, text=f"{labels[i]} ({v})")
        except Exception:
            pass

    def _nueva_cita(self):
        """Crea una nueva cita usando los datos del formulario.

        Antes esta función limpiaba los campos; ahora valida y crea la cita
        persistida a través del servicio, actualizando la vista.
        """
        fecha = self.fecha_var.get().strip() if hasattr(self, 'fecha_var') else ''
        hora = self.hora_var.get().strip() if hasattr(self, 'hora_var') else ''
        paciente = self.paciente_var.get().strip() if hasattr(self, 'paciente_var') else ''
        telefono = self.telefono_var.get().strip() if hasattr(self, 'telefono_var') else ''
        descripcion = self.desc_text.get('1.0', tk.END).strip() if hasattr(self, 'desc_text') else ''
        estado = self.estado_var.get().strip() if hasattr(self, 'estado_var') else 'Programada'

        # Validaciones básicas
        if not (fecha and hora and paciente and descripcion):
            messagebox.showerror('Error', 'Complete los campos obligatorios (fecha, hora, paciente, descripción).')
            return
        if not v_fecha(fecha):
            messagebox.showerror('Error', 'Fecha inválida. Use DD/MM/YYYY.')
            return
        if not v_hora(hora):
            messagebox.showerror('Error', 'Hora inválida. Use HH:MM.')
            return
        if telefono and not v_telefono(telefono):
            messagebox.showerror('Error', 'Teléfono inválido (9 dígitos).')
            return

        # Asegurar servicios
        if not hasattr(self, 'service'):
            try:
                self.initialize_services()
            except Exception as e:
                messagebox.showerror('Error', f'No se pudo inicializar el servicio: {e}')
                return

        # Crear y guardar la cita
        a = Appointment.new(fecha, hora, 30, paciente, telefono, descripcion, estado)
        try:
            self.service.crear(a)
        except ValueError as e:
            messagebox.showerror('Error', f'No se pudo crear la cita: {e}')
            return

        messagebox.showinfo('Cita creada', 'La cita se ha creado correctamente.')
        # Refrescar la lista
        try:
            self._refrescar()
        except Exception:
            pass

    def _actualizar_cita(self):
        """Actualiza la cita seleccionada usando `self.service.editar`.

        Recoge los campos del formulario (soporta tanto variables nuevas como widgets antiguos)
        y llama al servicio para actualizar la cita persistida.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning('Actualizar Cita', 'Por favor, seleccione una cita para actualizar.')
            return

        # obtener id seleccionado
        item = self.tree.item(seleccion[0])
        vals = item.get('values', [])
        if not vals:
            messagebox.showerror('Error', 'No se pudo obtener la cita seleccionada.')
            return
        id_ = vals[0]

        # leer campos (compatibilidad con viejos y nuevos widgets)
        fecha = self.fecha_var.get().strip()
        hora = self.hora_var.get().strip()
        paciente = self.paciente_var.get().strip()
        telefono = self.telefono_var.get().strip()
        descripcion = self.desc_text.get('1.0', tk.END).strip()
        dur = 30  # valor por defecto
        estado = self.estado_var.get().strip()

        # validaciones
        if not (fecha and hora and paciente and descripcion):
            messagebox.showerror('Error', 'Complete los campos obligatorios (fecha, hora, paciente, descripción).')
            return
        if not v_fecha(fecha):
            messagebox.showerror('Error', 'Fecha inválida. Use DD/MM/YYYY.')
            return
        if not v_hora(hora):
            messagebox.showerror('Error', 'Hora inválida. Use HH:MM.')
            return
        if telefono and not v_telefono(telefono):
            messagebox.showerror('Error', 'Teléfono inválido (9 dígitos).')
            return

        # crear objeto y editar
        a = Appointment.new(fecha, hora, dur, paciente, telefono, descripcion, estado)
        try:
            self.service.editar(id_, a)
        except ValueError as e:
            messagebox.showerror('Error', f'No se pudo actualizar la cita: {e}')
            return

        messagebox.showinfo('Cita actualizada', 'La cita se ha actualizado correctamente.')
        try:
            self._refrescar()
        except Exception:
            pass

    def _cancelar_cita(self):
        """Cancela la cita seleccionada usando `self.service.cancelar`.

        Pide motivo opcional al usuario y actualiza la vista.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning('Cancelar Cita', 'Por favor, seleccione una cita para cancelar.')
            return

        item = self.tree.item(seleccion[0])
        vals = item.get('values', [])
        if not vals:
            messagebox.showerror('Error', 'No se pudo obtener la cita seleccionada.')
            return
        id_ = vals[0]

        if not messagebox.askyesno('Cancelar Cita', '¿Está seguro de que desea cancelar esta cita?'):
            return

        motivo = simpledialog.askstring('Motivo de cancelación', 'Ingrese motivo (opcional):') or ''
        try:
            self.service.cancelar(id_, motivo)
        except ValueError as e:
            messagebox.showerror('Error', f'No se pudo cancelar la cita: {e}')
            return

        messagebox.showinfo('Cita cancelada', 'La cita ha sido cancelada.')
        try:
            self._refrescar()
        except Exception:
            pass

        

    # Eliminar referencias a 'frm' y usar un frame propio si es necesario
    # Este bloque parece duplicado respecto a la interfaz principal, así que lo comentamos o adaptamos según la estructura real
    # Si necesitas estos widgets, crea un frame adecuado, por ejemplo:
    # lab = ttk.LabelFrame(self.tab_citas, text='Cita')
    # ...
    pass

    def _on_sel(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], 'values')
        # columnas: (id, fecha, hora, paciente, telefono, estado, descripcion)
        self.sel_id = vals[0]
        # actualizar campos
        self.fecha_var.set(vals[1])
        self.hora_var.set(vals[2])
        self.paciente_var.set(vals[3])
        self.telefono_var.set(vals[4])
        self.estado_var.set(vals[5])
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert('1.0', vals[6])

    def _eliminar_cita(self):
        """Elimina permanentemente la cita seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning('Eliminar Cita', 'Por favor, seleccione una cita para eliminar.')
            return

        item = self.tree.item(seleccion[0])
        vals = item.get('values', [])
        if not vals:
            messagebox.showerror('Error', 'No se pudo obtener la cita seleccionada.')
            return
        id_ = vals[0]

        if not messagebox.askyesno('Eliminar Cita', 
                                 '¿Está seguro de que desea ELIMINAR permanentemente esta cita?\n' +
                                 'Esta acción no se puede deshacer.'):
            return

        try:
            self.service.eliminar(id_)
            messagebox.showinfo('Cita eliminada', 'La cita ha sido eliminada permanentemente.')
            self._refrescar()
            self._limpiar_formulario()
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo eliminar la cita: {e}')

    def _refrescar(self):
        """Actualiza la lista de citas desde el servicio"""
        # Verificar que tenemos servicio
        if not hasattr(self, 'service'):
            try:
                self.initialize_services()
            except Exception as e:
                messagebox.showerror('Error', f'No se pudo inicializar el servicio: {e}')
                return

        # Cargar citas en cache y aplicar filtros/ordenación
        try:
            self._all_citas = self.service.listar()
            self._apply_filters()
        except Exception as e:
            messagebox.showerror('Error', f'No se pudieron cargar las citas: {e}')

    def _render_tree(self, items):
        """Rellena el TreeView con la lista de objetos Appointment proporcionada"""
        # Limpiar TreeView
        for i in self.tree.get_children():
            self.tree.delete(i)
        for a in items:
            self.tree.insert('', tk.END, values=(a.id, a.fecha, a.hora, a.paciente, a.telefono, a.estado, a.descripcion))

    def _apply_filters(self):
        """Aplica filtros de búsqueda/estado/fecha sobre self._all_citas y renderiza el resultado."""
        items = list(self._all_citas)
        q = getattr(self, 'search_var', tk.StringVar()).get().strip().lower() if hasattr(self, 'search_var') else ''
        state = getattr(self, 'state_filter_var', tk.StringVar()).get() if hasattr(self, 'state_filter_var') else 'Todos'
        datef = getattr(self, 'date_filter_var', tk.StringVar()).get().strip() if hasattr(self, 'date_filter_var') else ''

        # Filtrar por estado
        if state and state != 'Todos':
            items = [a for a in items if (getattr(a, 'estado', '') == state)]

        # Filtrar por fecha exacta si se proporciona y es válida
        if datef:
            try:
                from datetime import datetime as _dt
                _dt.strptime(datef, '%d/%m/%Y')
                items = [a for a in items if getattr(a, 'fecha', '') == datef]
            except Exception:
                # Si la fecha no es válida, no aplicar filtro por fecha
                pass

        # Filtrar por consulta de texto (paciente, telefono, descripcion)
        if q and not q.startswith('buscar'):
            items = [a for a in items if q in (getattr(a, 'paciente', '') or '').lower() or q in (getattr(a, 'telefono', '') or '').lower() or q in (getattr(a, 'descripcion', '') or '').lower()]

        # Ordenar según columna seleccionada
        items = self._sort_items(items)

        # Render
        self._render_tree(items)

    def _sort_items(self, items):
        """Devuelve la lista ordenada según self._sort_col y self._sort_reverse"""
        col = self._sort_col
        if not col:
            return items

        def key_fn(a):
            try:
                if col == 'fecha':
                    return datetime.strptime(getattr(a, 'fecha', ''), '%d/%m/%Y')
                if col == 'hora':
                    return datetime.strptime(getattr(a, 'hora', ''), '%H:%M')
                # cadenas
                return getattr(a, col, '') or ''
            except Exception:
                return getattr(a, col, '') or ''

        try:
            return sorted(items, key=key_fn, reverse=self._sort_reverse)
        except Exception:
            return items

    def _on_heading_click(self, col):
        """Maneja clic en cabecera: alterna orden asc/desc y reaplica filtros"""
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False
        self._apply_filters()

    def _on_search_change(self):
        # callback cuando cambia el contenido del campo de búsqueda
        self._apply_filters()

    def _clear_filters(self):
        if hasattr(self, 'search_var'):
            self.search_var.set('')
        if hasattr(self, 'state_filter_var'):
            self.state_filter_var.set('Todos')
        if hasattr(self, 'date_filter_var'):
            self.date_filter_var.set('')
        self._apply_filters()

    # ----------------- Import / Export -----------------
    def _export_dialog(self):
        try:
            # Carpeta backups junto al script
            backup_dir = Path(__file__).parent / 'backups'
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Timestamp y paciente (si hay selección)
            ts = datetime.now().strftime('%Y-%m-%d-%H-%M')
            paciente = 'all'
            sel = getattr(self, 'tree', None).selection() if hasattr(self, 'tree') else []
            if sel:
                vals = self.tree.item(sel[0]).get('values', [])
                if len(vals) > 3 and vals[3]:
                    paciente = vals[3]
            # sanear paciente para filename
            paciente_safe = re.sub(r'[^A-Za-z0-9_-]', '_', paciente.strip()) if paciente else 'all'
            base = f"{ts}-{paciente_safe}"

            json_path = str(backup_dir / (base + '.json'))
            csv_path = str(backup_dir / (base + '.csv'))

            # Exportar ambos formatos
            self._export_json(json_path, show_msg=False)
            self._export_csv(csv_path, show_msg=False)

            messagebox.showinfo('Exportar', f'Exportadas citas a:\n{json_path}\n{csv_path}')
        except Exception as e:
            messagebox.showerror('Error', f'Error al exportar: {e}')

    def _import_dialog(self):
        path = filedialog.askopenfilename(filetypes=[('JSON', '*.json'), ('CSV', '*.csv')])
        if not path:
            return
        try:
            if path.lower().endswith('.csv'):
                self._import_csv(path)
            else:
                self._import_json(path)
        except Exception as e:
            messagebox.showerror('Error', f'Error al importar: {e}')

    def _export_json(self, path: str, show_msg: bool = True):
        citas = self.service.listar() if hasattr(self, 'service') else self.repo.all()
        data = [a.to_dict() for a in citas]
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if show_msg:
            messagebox.showinfo('Exportar', f'Exportadas {len(data)} citas a {path}')

    def _export_csv(self, path: str, show_msg: bool = True):
        citas = self.service.listar() if hasattr(self, 'service') else self.repo.all()
        fieldnames = ['id', 'fecha', 'hora', 'duracion_min', 'paciente', 'telefono', 'descripcion', 'estado', 'created_at', 'updated_at']
        with open(path, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for a in citas:
                d = a.to_dict() if hasattr(a, 'to_dict') else a.__dict__
                row = {k: d.get(k, '') for k in fieldnames}
                w.writerow(row)
        if show_msg:
            messagebox.showinfo('Exportar', f'Exportadas {len(citas)} citas a {path}')

    def _import_json(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            messagebox.showerror('Importar', 'El fichero JSON debe contener una lista de citas')
            return
        if not messagebox.askyesno('Importar', f'Se importarán {len(data)} citas. Las que coincidan por id serán sobrescritas. ¿Continuar?'):
            return
        existing = {a.id: a for a in self.repo.all()}
        imported = 0
        for d in data:
            try:
                a = Appointment.from_dict(d)
                existing[a.id] = a
                imported += 1
            except Exception:
                # intentar crear desde campos mínimos
                try:
                    a = Appointment.from_dict(d)
                    existing[a.id] = a
                    imported += 1
                except Exception:
                    continue
        self.repo.save_many(list(existing.values()))
        self._refrescar()
        messagebox.showinfo('Importar', f'Importadas {imported} citas desde {path}')

    def _import_csv(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            r = csv.DictReader(f)
            rows = list(r)
        if not rows:
            messagebox.showwarning('Importar', 'No se encontraron filas en el CSV')
            return
        if not messagebox.askyesno('Importar', f'Se importarán {len(rows)} filas del CSV. Las que coincidan por id serán sobrescritas. ¿Continuar?'):
            return
        existing = {a.id: a for a in self.repo.all()}
        imported = 0
        for row in rows:
            try:
                d = {
                    'id': row.get('id') or str(uuid.uuid4()),
                    'fecha': row.get('fecha',''),
                    'hora': row.get('hora',''),
                    'duracion_min': int(row.get('duracion_min') or 30),
                    'paciente': row.get('paciente',''),
                    'telefono': row.get('telefono',''),
                    'descripcion': row.get('descripcion',''),
                    'estado': row.get('estado','Programada')
                }
                a = Appointment.from_dict(d)
                existing[a.id] = a
                imported += 1
            except Exception:
                continue
        self.repo.save_many(list(existing.values()))
        self._refrescar()
        messagebox.showinfo('Importar', f'Importadas {imported} filas desde {path}')

    def _on_entry_click(self, entry, placeholder):
        """Maneja el evento de click en un entry con placeholder"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def _on_focus_out(self, entry, placeholder):
        """Maneja el evento de pérdida de foco en un entry con placeholder"""
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(foreground='grey')

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.fecha_var.set('')
        self.hora_var.set('')
        self.paciente_var.set('')
        self.telefono_var.set('')
        self.estado_var.set('Programada')
        self.desc_text.delete('1.0', tk.END)

    def setup_window(self):
        """Configura la ventana principal"""
        self.root.geometry("1200x700")
        self.root.minsize(800, 600)
        self.root.configure(bg='#f0f0f0')
        # Hacer que la ventana sea redimensionable
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def initialize_services(self):
        """Inicializa los servicios de la aplicación"""
        self.repo = JsonAppointmentRepo()
        self.service = AgendaService(
            self.repo, 
            SlotEngine(inicio='09:00', fin='17:00', duracion_min=30)
        )
        self.selected_appointment_id = None

if __name__ == '__main__':
    root = tk.Tk()
    ModernAppointmentApp(root)
    root.mainloop()