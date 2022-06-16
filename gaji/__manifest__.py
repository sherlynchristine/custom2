{
    'name': 'Gaji', #nama modul yang dibaca user di UI
    'version': '1.0',
    'author': 'Sherlyn',
    'summary': 'Modul Gaji SIB UK Petra', #deskripsi singkat dari modul
    'description': 'Ideas management module', #bisa menampilkan gambar/deskripsi dalam bentuk html.
    #di idea/static/description, bisa kasih icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'], #list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/department_views.xml',
        'views/cuti_views.xml',
        'views/pinjaman_views.xml',
        'views/absen_views.xml',
        'views/gaji_views.xml',
        'views/wiz_employee_pinjaman_views.xml'
    ],
    'qweb': [], #untuk memberi tahu static file, misal css
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False, #indikasi install, saat buat database baru
}