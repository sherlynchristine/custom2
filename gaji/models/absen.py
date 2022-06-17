from odoo import models, fields, api, _

class absen(models.Model):
    _name= 'gaji.absen'
    _description= 'class menyimpan absen pegawai'
    _rec_name = 'name'

    #atribute field
    name = fields.Char('ID', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    date = fields.Datetime('Tanggal Masuk', default=fields.Datetime.now,
                       readonly=True, required=True)
    date2 = fields.Datetime('Tanggal Keluar', readonly=True , required=True, default=fields.Datetime.now()
                            )
    state = fields.Selection([('draft', 'Draft'),
                              ('absenmasuk', 'Absen Masuk'),
                              ('absenkeluar', 'Absen Keluar'),
                              ('done', 'Done')], 'State', required=True, readonly=True,
                             default='draft')

    keterangan = fields.Char("Keterangan Hadir", compute="_compute_keterangan", store=True,
                             default=0, ondelete="set null")
    #keterangan = fields.Selection([('Hadir', 'Hadir'),
                                   #('Terlambat', 'Terlambat'),
                                   #('Absen', 'Absen')], "Keterangan Hadir")
    #keterangan2 = fields.Selection([('Lembur', 'Lembur'),
                                   #('Tidaklembur', 'Tidak Lembur')], "Keterangan Lembur")
    keterangan2 = fields.Char("Keterangan Lembur", compute="_compute_keterangan2", store=True,
                             default='Tidak Lembur', ondelete="set null")
    emp_ids = fields.Many2one('gaji.employee', string='Employee ID', ondelete="cascade")
    emp_nama = fields.Char('Employee Name', related='emp_ids.nama')

    @api.depends("emp_ids")
    def _compute_keterangan(self):
        import datetime
        dt = fields.Datetime.from_string(self.date).time().hour + 8
        jam = fields.Datetime.from_string('2023-01-01 14:00:14').time().hour
        dt_hrs = abs(dt - jam)
        #self.keterangan = (dt + jam) + dt_hrs
        if dt_hrs == 1 or dt_hrs == 0:
            self.keterangan = 'Hadir'
        elif dt_hrs > 1 and dt_hrs < 3:
            self.keterangan = 'Terlambat'
        else:
            self.keterangan = 'Absen'

    @api.depends("state")
    def _compute_keterangan2(self):
        self.date2 = fields.Datetime.now()
        if self.keterangan != 'Absen':
            jam = fields.Datetime.from_string('2023-01-01 18:00:18').time().hour
            dt = self.date2.hour + 8
            if dt > jam:
                self.keterangan2 = 'Lembur'
        elif self.keterangan == 'Absen':
            self.state = 'done'


    def action_done(self):
        self.state = 'done'
    def action_settodraft(self):
        self.state = 'draft'
    def action_absenmasuk(self):
        self.state = 'absenmasuk'
    def action_absenkeluar(self):
        self.state = 'absenkeluar'