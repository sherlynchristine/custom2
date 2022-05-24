from odoo import models, fields, api, _
#_ untuk translate

class mahasiswa(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.mahasiswa' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel
        # (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk mahasiswa'
    _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.

    name = fields.Char('NRP', size=64, required=True, index=True)
    nama = fields.Char('Nama', size=64, required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    status = fields.Selection([('active', 'Active'),
                              ('cuti', 'Cuti')], 'Status', required=True, readonly=False,
                              default='active')
    ipk = fields.Float("IPK", compute="_compute_ipk", store=True, default=0)
    #_sql_constraints = [('nrp unik', 'Unique(name)', ('NRP must be Unique!'))]

    def _compute_ipk(self):
        pass
    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_settodraft(self):
        self.state = 'draft'
