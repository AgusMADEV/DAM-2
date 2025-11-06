from tkinter import ttk

def apply_theme(root):
    style = ttk.Style(root)
    try:
        style.theme_use('clam')
    except Exception:
        pass
    style.configure('.', background='#f8f9fa', foreground='#222222', font=('Segoe UI', 10))
    style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'), foreground='#0b5fb8')
    style.configure('Primary.TButton', background='#1976d2', foreground='white')
