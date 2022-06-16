from odoo import models, fields, api, _

class department(models.Model):
    _name= 'gaji.department'
    _description= 'class menyimpan data department'
    _order = 'name desc'
    _rec_name = 'name'

    #atribute field
    name = fields.Char('Name', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    nama = fields.Char('ID Department', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    gaji_pokok = fields.Integer('Gaji Pokok', size=64, required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    daftar_emp_ids = fields.One2many('gaji.employee', 'dept_ids', string='Employees', ondelete="cascade")

    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_confirmed(self):
        self.state = 'confirmed'
    def action_settodraft(self):
        self.state = 'draft'