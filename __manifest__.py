{
    'name': 'Mimir',
    'version': '17.0',
    'category': 'Administration',
    'author': "PT Perush",
    'website': "https://www.example.com",
    'license': 'LGPL-3',
    'images': ['static/'],
    'summary': 'Administration',
    'depends': ['base', 'mail'],
    'description': """
stock analysis go brr
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
	'images': ['static/description/pt-tsbm-sq100.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
