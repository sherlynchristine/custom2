from odoo import models, fields, api, _

class employee(models.Model):
    _name= 'gaji.employee'
    _description= 'class menyimpan data employee'
    _order = 'name desc'
    _rec_name = 'name'

    #atribute field
    name = fields.Char('ID', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    nama = fields.Char('Full Name', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    kontak = fields.Char('Contact Number', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    status = fields.Char("Status", compute="_compute_status", store=True,
                             default='Aktif', ondelete="cascade")
    date = fields.Date('date', default=fields.Date.context_today,
                                 readonly=True)
    #status = fields.Selection([('Aktif', 'Aktif'),
                              #('Cuti', 'Cuti'),
                              #('Resign', 'Resign')],
                              #'Status Pegawai', required=True, Readonly=False,
                              #default='Aktif', compute="_compute_status")
    #confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)

    dept_ids = fields.Many2one('gaji.department', string='Department', ondelete="cascade",
                              domain="[('state', '=', 'done')]")
    gaji_ids = fields.One2many('gaji.gaji', 'emp_ids', string='Gaji', ondelete="cascade")
    cuti_ids = fields.One2many('gaji.cuti', 'emp_ids', string='Cuti', ondelete="cascade")
    total_cuti = fields.Integer("Total Hari Cuti", compute="_compute_cuti", store=True, default=0)
    pinjaman_ids = fields.One2many('gaji.pinjaman', 'emp_ids', string='Pinjaman', ondelete="cascade")
    total_pinjaman = fields.Integer("Total Pinjaman", compute="_compute_pinjaman", store=True, default=0)
    absen_ids = fields.One2many('gaji.absen', 'emp_ids', string='Absensi', ondelete="cascade")
    total_hadir = fields.Integer("Jumlah Hadir", compute="_compute_absen", store=True, default=0)
    total_terlambat = fields.Integer("Jumlah Terlambat", compute="_compute_absen", store=True, default=0)
    total_absen = fields.Integer("Jumlah Absen", compute="_compute_absen", store=True, default=0)

    line_ids = fields.One2many('gaji.employee.lines', 'employee_id', string='Data Pinjaman')

    @api.depends("pinjaman_ids", "pinjaman_ids.nominal", "pinjaman_ids.state")
    def _compute_pinjaman(self):
        for a in self.filtered(lambda s:s.state=='done'):
            val = {
                "total_pinjaman": 0
            }
            for rec in a.pinjaman_ids.filtered(lambda s:s.state=='approve'):
                val['total_pinjaman'] += rec.nominal
            a.update(val)

    @api.depends("cuti_ids", "cuti_ids.durasi", "cuti_ids.state")
    def _compute_cuti(self):
        for a in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total_cuti": 0
            }
            for rec in a.cuti_ids.filtered(lambda s: s.state == 'approve'):
                val['total_cuti'] += rec.durasi
            a.update(val)

    @api.depends("absen_ids", "absen_ids.keterangan", "absen_ids.state")
    def _compute_absen(self):
        for a in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total_hadir": 0,
                "total_absen": 0,
                "total_terlambat": 0
            }
            for rec in a.absen_ids.filtered(lambda s: s.state != 'draft'):
                if rec.keterangan == 'Hadir':
                    val['total_hadir'] += 1
                elif rec.keterangan == 'Terlambat':
                    val['total_terlambat'] += 1
                elif rec.keterangan == 'Absen':
                    val['total_absen'] += 1
            a.update(val)

    @api.depends("cuti_ids")
    def _compute_status(self):
        #if self.filtered(lambda s:s.state=='approve'):
        if self.filtered(lambda s:s.state=='approve'):
            tmp2 = self.cuti_ids.tanggal_kembali
            hariini = fields.Datetime.from_string(self.date)
            tgl_kembali = fields.Datetime.from_string(tmp2)
            if hariini > tgl_kembali:
                self.status = 'Resign'
            elif hariini < tgl_kembali:
                self.status = 'Cuti'
            else:
                self.status = 'Aktif'




    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_confirmed(self):
        self.state = 'confirmed'
    def action_settodraft(self):
        self.state = 'draft'

    def action_wiz_employee(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Pinjaman Employee'),
            'res_model': 'wiz.employee.pinjaman',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

class employee_lines(models.Model):
    _name = 'gaji.employee.lines'
    _description = 'class untuk menyimpan data'

    employee_id = fields.Many2one('gaji.employee', string='Employee', ondelete="cascade")
    pinjaman_id = fields.Many2one('gaji.pinjaman', string='Pinjaman', ondelete="restrict")
    nominal = fields.Integer('Nominal', related='pinjaman_id.nominal')
    status = fields.Selection([('belumlunas', 'Belum Lunas'),
                               ('lunas', 'Lunas')])
    _sql_constraints = [('name_unik', 'unique(employee_id, pinjaman_id)',
                         _("Pinjaman sudah pernah didata!"))]