from odoo import models, fields, api, _

class cuti(models.Model):
    _name= 'gaji.cuti'
    _description= 'class menyimpan data cuti pegawai'
    _rec_name = 'name'

    #atribute field
    name = fields.Integer('ID', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    keterangan = fields.Char('Keterangan', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    tanggal_mulai = fields.Date('Tanggal Cuti', default=fields.Date.context_today,
                       readonly=True, states={'draft': [('readonly', False)]})
    tanggal_kembali = fields.Date('Tanggal Kembali', default=fields.Date.context_today,
                                readonly=True, states={'draft': [('readonly', False)]})
    #tanggal_kembali = fields.Date('Tanggal kembali', compute="_compute_kembali", store=True,
                             #default=fields.Date.context_today)
    durasi = fields.Integer('Durasi (hari)', size=64, required=True, index=True, readonly=True,
                          states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('submitted', 'Submitted'),
                              ('approve', 'Approve'),
                              ('rejected', 'Rejected'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    #confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)
    emp_ids = fields.Many2one('gaji.employee', string='Employee ID', ondelete="cascade")
    emp_nama = fields.Char('Employee Name', related='emp_ids.nama')
    emp_dept = fields.Many2one(related='emp_ids.dept_ids', string='Employee Department')

    #@api.depends("tanggal_mulai")
    #def _compute_kembali(self):
        #dt = fields.Datetime.from_string(self.tanggal_mulai).days
        #kembali = dt + self.durasi
        #self.tanggal_kembali =

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