from odoo import models, fields, api, _

class wizkelas(models.TransientModel):
    _name = 'wiz.employee.pinjaman'
    _description = 'class untuk menyimpan data employee dan pinjaman'
    employee_id = fields.Many2one('gaji.employee', string="Employee")
    employee_name = fields.Char('Employee Name', related='employee_id.nama')

    line_ids = fields.One2many('wiz.employee.pinjaman.lines', 'wiz_header_id', string='Data')

    @api.model
    def default_get(self,
                    fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wizkelas, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['employee_id'] = self.env.context['active_id']
        return res

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if not self.employee_id:
            return
        vals = []
        line_ids = self.env['wiz.employee.pinjaman.lines']
        for rec in self.employee_id.line_ids:
            line_ids += self.env['wiz.employee.pinjaman.lines'].new({
                'wiz_header_id': self.id,
                'pinjaman_id': rec.pinjaman_id.id,
                'ref_employee_lines_id': rec.id
            })
            # cara membuat record baru di m2m atau o2m
        self.line_ids = line_ids

    def action_confirm(self):
        for rec in self.line_ids:
            rec.ref_employee_lines_id.status = rec.status

class employee_lines_wiz(models.TransientModel):
    _name = 'wiz.employee.pinjaman.lines'
    _description = 'class untuk menyimpan data pinjaman'

    wiz_header_id = fields.Many2one('wiz.employee.pinjaman', string='Pinjaman')
    pinjaman_id = fields.Many2one('gaji.pinjaman', string="Pinjaman", ondelete="restrict")
    nominal = fields.Integer('Nominal', related='pinjaman_id.nominal')
    status = fields.Selection([('belumlunas', 'Belum Lunas'),
                               ('lunas', 'Lunas')])
    ref_employee_lines_id = fields.Many2one('gaji.employee.lines')
