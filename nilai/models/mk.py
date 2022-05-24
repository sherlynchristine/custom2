from odoo import models, fields, api, _
#_ untuk translate

class mk(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.mk' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel
        # (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk Mata Kuliah'
    _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.

    name = fields.Char('Nama MK', size=64, required=True, index=True,
                       readonly=True,states={'draft': [('readonly', False)]})
    kode = fields.Char('Kode MK', size=64, required=True, readonly=False)
    sks = fields.Integer('SKS', required=True, readonly=False)
    active = fields.Boolean('Active', readonly=True, states={'draft': [('readonly', False)]})
    #states={'draft': [('readonly', False)]}
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_settodraft(self):
        self.state = 'draft'
