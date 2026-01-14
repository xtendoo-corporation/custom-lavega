{
    'name': 'Sincronizar Costes e Impuestos entre compañías',
    'version': '1.0',
    'depends': ['product', 'account'],
    'author': 'Tu Nombre',
    'category': 'Tools',
    'description': 'Propaga costes e impuestos de productos de una compañía a otra.',
    'data': [
        'security/ir.model.access.csv',
        'views/sync_wizard_view.xml'
    ],
    'installable': True,
    'application': False,
}
