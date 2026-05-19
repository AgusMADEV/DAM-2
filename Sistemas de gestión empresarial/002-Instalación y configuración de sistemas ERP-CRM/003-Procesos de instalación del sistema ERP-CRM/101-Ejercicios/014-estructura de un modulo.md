

## 🧱 1. Estructura básica del módulo

Por convención, los módulos se guardan en una carpeta personalizada, normalmente en:

```
/usr/lib/python3/dist-packages/odoo/addons/
```

o si prefieres mantenerlos aparte:

```
/opt/odoo/custom-addons/
```

Creemos ese directorio y nuestro módulo:

```bash
sudo mkdir -p /opt/odoo/custom-addons/mi_modulo_ejemplo
cd /opt/odoo/custom-addons/mi_modulo_ejemplo
```

---

## 📁 2. Estructura mínima de archivos

Crea esta jerarquía:

```
mi_modulo_ejemplo/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── ejemplo.py
└── views/
    └── ejemplo_views.xml
```

Crea los archivos así:

---

### **`__manifest__.py`**

Describe el módulo (nombre, versión, dependencias, etc.):

```python
{
    'name': 'Módulo de Ejemplo',
    'version': '1.0',
    'summary': 'Un módulo básico de ejemplo para Odoo 18 Community',
    'author': 'Jose Vicente Carratala',
    'category': 'Tutorial',
    'depends': ['base'],
    'data': [
        'views/ejemplo_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

---

### **`__init__.py`**

Importa los modelos:

```python
from . import models
```

---

### **`models/__init__.py`**

```python
from . import ejemplo
```

---

### **`models/ejemplo.py`**

Aquí definimos un modelo simple, por ejemplo una tabla de “Notas personales”:

```python
from odoo import models, fields

class NotaEjemplo(models.Model):
    _name = 'mi_modulo_ejemplo.nota'
    _description = 'Nota de Ejemplo'

    name = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción')
    fecha = fields.Date(string='Fecha')
```

Esto creará una nueva tabla SQL llamada `mi_modulo_ejemplo_nota`.

---

### **`views/ejemplo_views.xml`**

Diseñamos la vista (interfaz en Odoo):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record id="view_nota_form" model="ir.ui.view">
        <field name="name">nota.form</field>
        <field name="model">mi_modulo_ejemplo.nota</field>
        <field name="arch" type="xml">
            <form string="Nota de Ejemplo">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="descripcion"/>
                        <field name="fecha"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_nota_tree" model="ir.ui.view">
        <field name="name">nota.tree</field>
        <field name="model">mi_modulo_ejemplo.nota</field>
        <field name="arch" type="xml">
            <tree string="Notas de Ejemplo">
                <field name="name"/>
                <field name="fecha"/>
            </tree>
        </field>
    </record>

    <menuitem id="menu_mi_modulo_root" name="Notas de Ejemplo"/>

    <menuitem id="menu_mi_modulo_notas"
              name="Notas"
              parent="menu_mi_modulo_root"
              action="action_nota"/>

    <record id="action_nota" model="ir.actions.act_window">
        <field name="name">Notas de Ejemplo</field>
        <field name="res_model">mi_modulo_ejemplo.nota</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

---

## ⚙️ 3. Añadir el módulo al `addons_path`

Abre tu archivo de configuración de Odoo (normalmente `/etc/odoo/odoo.conf`) y añade tu ruta personalizada:

```ini
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/opt/odoo/custom-addons
```

Guarda y reinicia el servicio:

```bash
sudo systemctl restart odoo
```

---

## 🧩 4. Activar el modo desarrollador y cargar el módulo

1. Entra en Odoo:
   👉 `http://localhost:8069`
2. Crea o entra en una base de datos.
3. Ve a **Configuración → Activar Modo Desarrollador**.

-Entrar en modo desarrollo: http://localhost:8069?debug=1

4. Entra en **Aplicaciones**, pulsa “Actualizar lista de aplicaciones”.
5. Busca **“Módulo de Ejemplo”** y haz clic en **Instalar**.

---

## ✅ 5. Probar

Tras instalarlo, en el menú superior aparecerá una nueva entrada **“Notas de Ejemplo”**, donde podrás crear, editar y listar tus registros.



