from odoo import models, fields, api, _

class transaksi(models.Model):
    _name= 'perpus.transaksi'
    _description= 'class untuk menyimpan transaksi'

    #atribute field
    name = fields.Char('ID transaksi', size=64, required=True, index=True,
                       readonly=True,states={'draft': [('readonly', False)]})
    peminjam = fields.Many2one('res.partner', 'Peminjam',
                            index=True, readonly=True, states={'draft': [('readonly', False)]})
    tanggal_pinjam = fields.Date('Tanggal Peminjaman', default=fields.Date.context_today,
                                 help='Please fill the date here',
                                 readonly=True, states={'draft': [('readonly', False)]})
    durasi = fields.Integer("Durasi Peminjaman", size=15, required=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    deadline_kembali = fields.Date("Batas Tanggal Pengembalian", help='Please fill batas pengembalian buku',
                                  readonly=True, states={'draft': [('readonly', False)]})
    tanggal_kembali = fields.Date("Tanggal Kembali", default=fields.Date.context_today,
                                  help='Masukan tanggal pengembalian',
                                  readonly=True, states={'confirmedpeminjaman': [('readonly', False)]})
    #denda = fields.Integer("denda", size=15, required=True, readonly=True, states={'confirmedpeminjaman': [('readonly', False)]})
    denda = fields.Integer("Total Denda", compute="_compute_denda", store=True, default=0)
    total = fields.Integer("Total Peminjaman", compute="_compute_total", store=True, default=0)
    detailtransaksi_ids = fields.One2many('perpus.detailtransaksi', 'transaksi_ids', string='Transaksi Nomor')
    _sql_constraints = [('name_unik', 'unique(name)', _('ID Transaksi sudah ada!!'))]

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmedpeminjaman', 'Confirmed Peminjaman'),
                              ('pengembalian', 'Confirm Pengembalian'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    @api.depends('detailtransaksi_ids.buku_biaya')
    def _compute_total(self):
        for a in self:
            val = {
                "total": 0
            }
            for b in a.detailtransaksi_ids:
                val['total'] += b.buku_biaya
            a.update(val)

    @api.depends('tanggal_kembali', 'deadline_kembali')
    def _compute_denda(self):
        if self.deadline_kembali and self.tanggal_kembali:
            deadline_kembali = fields.Datetime.from_string(self.deadline_kembali)
            tanggal_kembali = fields.Datetime.from_string(self.tanggal_kembali)
            if tanggal_kembali > deadline_kembali:
                self.denda = abs((tanggal_kembali - deadline_kembali).days) * (0.5 * self.total)


    def _compute_kembali(self):
        pass

    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'

    #@api.depends('state')
    def action_confirmedpeminjaman(self):
        self.state = 'confirmedpeminjaman'
        #for a in self:
            #for b in a.detailtransaksi_ids:
                #b.buku_status = 'False'

    def action_settodraft(self):
        self.state = 'draft'
    def action_pengembalian(self):
        self.state = 'pengembalian'