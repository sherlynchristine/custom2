{
    'name': 'Idea', #nama modul yang dibaca user di UI
    'version': '1.0',
    'author': 'Sherlyn',
    'summary': 'Modul Idea SIB UK Petra', #deskripsi singkat dari modul
    'description': 'Ideas management module', #bisa menampilkan gambar/deskripsi dalam bentuk html.
    #di idea/static/description, bisa kasih icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base'], #list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/idea_views.xml',
        'views/voting_views.xml'
    ],
    'qweb': [], #untuk memberi tahu static file, misal css
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False, #indikasi install, saat buat database baru
}