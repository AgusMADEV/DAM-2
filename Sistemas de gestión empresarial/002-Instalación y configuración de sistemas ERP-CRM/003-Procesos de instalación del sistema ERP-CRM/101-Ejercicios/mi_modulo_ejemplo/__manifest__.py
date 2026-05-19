{
    'name': 'Módulo de Ejemplo',
    'version': '1.0',
    'summary': 'Un módulo básico de ejemplo para Odoo 18 Community',
    'author': 'Jose Vicente Carratala',
    'category': 'Tutorial',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ejemplo_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

