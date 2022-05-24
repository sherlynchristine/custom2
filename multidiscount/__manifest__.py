{
    'name': 'Multi Discount', #nama modul yang dibaca user di UI
    'version': '1.0',
    'author': 'Sherlyn',
    'summary': 'Modul Multi discount SIB UK Petra', #deskripsi singkat dari modul
    'description': 'Ideas management module', #bisa menampilkan gambar/deskripsi dalam bentuk html.
    #di idea/static/description, bisa kasih icon modul juga.
    'category': 'Sale',
    'website': 'http://sib.petra.ac.id',
    'depends': ['sale'], #list of dependencies, conditioning startup order
    'data': [
        'views/sale_order_views.xml'
    ],
    'qweb': [], #untuk memberi tahu static file, misal css
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False, #indikasi install, saat buat database baru
}