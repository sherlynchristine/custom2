from odoo import models, fields, api, _

class pinjaman(models.Model):
    _name= 'gaji.pinjaman'
    _description= 'class menyimpan data pinjaman pegawai'
    _rec_name = 'name'

    #atribute field
    name = fields.Integer('ID', size=64, required=True, index=True)
    date = fields.Date('Tanggal', default=fields.Date.context_today)
    nominal = fields.Integer('Nominal Pinjaman', size=64, required=True, index=True)
    #status = fields.Selection([('belumlunas', 'Belum Lunas'),
                               #('lunas', 'Lunas')],
                              #required=True, readonly=False,
                             #default='belumlunas')
    keterangan = fields.Char('Keterangan', required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('submitted', 'Submitted'),
                              ('approve', 'Approve'),
                              ('rejected', 'Rejected'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    #confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)
    emp_ids = fields.Many2one('gaji.employee', string='Employee ID', ondelete="cascade")
    emp_nama = fields.Char('Employee Name', related='emp_ids.nama')

    def action_approve(self):
        self.state = 'approve'
    def action_canceled(self):
        self.state = 'canceled'
    def action_submitted(self):
        self.state = 'submitted'
    def action_settodraft(self):
        self.state = 'draft'
    def action_rejected(self):
        self.state = 'rejected'