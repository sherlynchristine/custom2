from odoo import models, fields, api, _


class gaji(models.Model):
    _name = 'gaji.gaji'
    _description = 'class menyimpan data slip gaji pegawai'
    _rec_name = 'name'

    # atribute field
    name = fields.Char(compute="_compute_name", store=True, recursive=True)
    periode = fields.Selection([('January', 'January'),
                                ('Febuary', 'Febuary'),
                                ('March', 'March'),
                                ('April', 'April'),
                                ('May', 'May'),
                                ('June', 'June'),
                                ('July', 'July'),
                                ('August', 'August'),
                                ('September', 'September'),
                                ('October', 'October'),
                                ('November', 'November'),
                                ('December', 'December')], required=True)
    tahun = fields.Char("Tahun", default='2022', required=True)
    bonus = fields.Integer("Bonus", required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    date = fields.Date('Date', default=fields.Date.context_today,
                       required=True)
    emp_ids = fields.Many2one('gaji.employee', string='Employee ID', ondelete="cascade")
    emp_nama = fields.Char('Employee Name', related='emp_ids.nama')
    dept_ids = fields.Many2one(related='emp_ids.dept_ids', string='Employee Department')
    gaji_pokok = fields.Integer('Gaji Pokok',
                                related='dept_ids.gaji_pokok')

    terlambat_ = fields.Integer(related='emp_ids.total_terlambat', string='Total terlambat')
    absen_ = fields.Integer(related='emp_ids.total_absen', string='Total absen')
    totalterlambat = fields.Integer("Pengurangan 1", compute="_compute_sub", store=True, default=0)
    totalabsen = fields.Integer("Pengurangan 2", compute="_compute_sub", store=True, default=0)
    sub1 = fields.Integer("Subtotal 1", compute="_compute_sub", store=True)

    pinjaman_ = fields.Integer(related='emp_ids.total_pinjaman', string="Total Pinjaman")
    #sts_pinjam = fields.Char(related='pinjaman_.status')
    sub2 = fields.Integer("Subtotal 2", compute="_compute_sub", store=True, default=0)
    total = fields.Integer("TOTAL GAJI", compute="_compute_sub", store=True, default=0)
    #pinjaman_ids = fields.One2many('gaji.pinjaman', 'emp_ids', string='Pinjaman', ondelete="cascade")

    @api.depends("emp_ids", "bonus")
    def _compute_sub(self):
        if self.terlambat_ > 0:
            self.totalterlambat = self.terlambat_ * -20000
        if self.absen_ > 0:
            self.totalabsen = self.absen_ * -100000
        self.sub1 = self.gaji_pokok + self.bonus + self.totalterlambat + self.totalabsen
        if self.pinjaman_ > 0:
            self.sub2 = self.sub1 - self.pinjaman_
        self.total = self.sub1 + self.sub2

    @api.depends('emp_ids.name', 'periode', 'tahun')
    def _compute_name(self):
        for a in self:
            a.name = '%a - %a - %a' % (a.emp_ids.name, a.periode ,a.tahun)

    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_confirmed(self):
        self.state = 'confirmed'
    def action_settodraft(self):
        self.state = 'draft'
