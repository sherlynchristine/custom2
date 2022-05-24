from odoo import models, fields, api, _

class buku(models.Model):
    _name= 'perpus.buku'
    _description= 'class untuk menyimpan data buku'
    _order = 'name desc'

    #atribute field
    name = fields.Char('ID Buku', size=64, required=True, index=True,
                       readonly=True,states={'draft': [('readonly', False)]})
    judul = fields.Char('Judul Buku', size=64, required=True,
                        readonly=True,states={'draft': [('readonly', False)]})
    penulis = fields.Char('Penulis', size=64, required=True,
                        readonly=True, states={'draft': [('readonly', False)]})
    tahun = fields.Char("Tahun", size=15, required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    biaya = fields.Integer("Biaya Pinjam", size=15, required=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    status = fields.Boolean('Available', readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    description = fields.Text('Description', readonly=True,states={'draft': [('readonly', False)]})
    detailt_ids = fields.One2many('perpus.detailtransaksi', 'buku_ids', string='BUKUU')
    _sql_constraints = [('name_unik', 'unique(name)', _('ID buku sudah ada!!'))]

    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_settodraft(self):
        self.state = 'draft'