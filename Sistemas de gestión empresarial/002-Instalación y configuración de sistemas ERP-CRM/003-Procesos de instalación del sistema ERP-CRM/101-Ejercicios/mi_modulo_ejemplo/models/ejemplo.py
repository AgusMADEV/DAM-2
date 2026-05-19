from odoo import models, fields

class NotaEjemplo(models.Model):
    _name = 'mi_modulo_ejemplo.nota'
    _description = 'Nota de Ejemplo'

    name = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción')
    fecha = fields.Date(string='Fecha')

