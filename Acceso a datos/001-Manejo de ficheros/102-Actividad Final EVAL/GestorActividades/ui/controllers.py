import logging
import tkinter as tk
from ui.views import MainView
from ui.styles import apply_theme
from services.activity_service import ActivityService
from services.reporting import count_by_category
from services.import_export import export_csv
from domain.models import Activity


class AppController:
    def __init__(self):
        self.logger = logging.getLogger('AppController')
        self.service = ActivityService()
        self.view = MainView()
        apply_theme(self.view)
        self._bind()
        self._refresh_list()

    def _bind(self):
        self.view.set_on_add(self.on_add)
        self.view.set_on_update(self.on_update)
        self.view.set_on_delete(self.on_delete)

    def run(self):
        self.view.mainloop()

    def _refresh_list(self):
        for i in self.view.tree.get_children():
            self.view.tree.delete(i)
        for a in self.service.list_all():
            self.view.tree.insert('', tk.END, values=(a.id, a.title, a.category, a.date, a.duration_min))

    def on_add(self):
        a = Activity(title=self.view.title_var.get().strip(),
                     category=self.view.cat_var.get().strip() or 'general',
                     date=self.view.date_var.get().strip(),
                     duration_min=int(self.view.dur_var.get()),
                     notes=self.view.notes_text.get('1.0', tk.END).strip())
        try:
            self.service.create(a)
            self._refresh_list()
            tk.messagebox.showinfo('OK', 'Actividad guardada')
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))

    def on_update(self):
        sel = self.view.tree.selection()
        if not sel:
            tk.messagebox.showwarning('Aviso', 'Seleccione una actividad')
            return
        vals = self.view.tree.item(sel[0], 'values')
        aid = vals[0]
        a = Activity(id=aid,
                     title=self.view.title_var.get().strip(),
                     category=self.view.cat_var.get().strip() or 'general',
                     date=self.view.date_var.get().strip(),
                     duration_min=int(self.view.dur_var.get()),
                     notes=self.view.notes_text.get('1.0', tk.END).strip())
        try:
            self.service.update(aid, a)
            self._refresh_list()
            tk.messagebox.showinfo('OK', 'Actividad actualizada')
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))

    def on_delete(self):
        sel = self.view.tree.selection()
        if not sel:
            tk.messagebox.showwarning('Aviso', 'Seleccione una actividad')
            return
        vals = self.view.tree.item(sel[0], 'values')
        aid = vals[0]
        self.service.delete(aid)
        self._refresh_list()
        tk.messagebox.showinfo('OK', 'Actividad eliminada')

    def export_csv(self, dest: str = 'data/export/activities.csv'):
        activities = self.service.list_all()
        export_csv(activities, dest)
        self.logger.info(f'Exported CSV to {dest}')

    def draw_stats(self):
        data = count_by_category(self.service.list_all())
        canvas = self.view.stats_canvas
        canvas.delete('all')
        if not data:
            return
        width = int(canvas.winfo_width() or 600)
        height = int(canvas.winfo_height() or 300)
        maxv = max(data.values())
        bar_w = max(20, width // (len(data) * 2))
        x = 10
        for k, v in data.items():
            h = int((v / maxv) * (height - 40)) if maxv else 0
            canvas.create_rectangle(x, height - h - 20, x + bar_w, height - 20, fill='#1976d2')
            canvas.create_text(x + bar_w/2, height - 10, text=f'{k} ({v})', anchor='n')
            x += bar_w + 20
