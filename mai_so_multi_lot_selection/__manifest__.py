{
    'name': 'Sales order multi lots selection',
    'version': '14.1.1.1',
    'category': 'Sales Management',
    'summary': 'Sales order multi lots selection',
    'description': """ Using this module you can select multiple lot in sale order line.
    """,
    'price': 7,
    'currency': 'EUR',
    "author" : "MAISOLUTIONSLLC",
    "email": 'apps@maisolutionsllc.com',
    "website":'http://maisolutionsllc.com/',
    'license': 'OPL-1',
    'depends': ['sale_stock','sale_management'],
    "live_test_url" : "",
    'data': [
        'views/sale_view.xml',
        'views/stock_view.xml',
    ],
    'qweb': [
        ],
    'images': ['static/description/main_screenshot.png'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
