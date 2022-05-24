from odoo import models, fields, api, _
#_ untuk translate

class khs(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.khs' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel
        # (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan KHS'
    _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.

    name = fields.Char(compute="_compute_name", store=True, recursive=True)
    #name = fields.Char('nama compute', size=64, required=True, index=True)
    semester = fields.Selection([('Genap', 'Genap'),
                              ('Gasal', 'Gasal')], 'Semester', required=True, readonly=True,
                                default='Genap', states = {'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    ips = fields.Float("IPS", compute="_compute_ips", store=True, default=0)
    tahun = fields.Char("Tahun", size=15, default="2021/2022", required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    mhs_id = fields.Many2one('nilai.mahasiswa', string="Mahasiswa", readonly=True, ondelete="cascade",
                             domain="[('state', '=', 'done')]", states={'draft': [('readonly', False)]})
    detailKHS_ids = fields.One2many('nilai.detail_khs', 'khs_id' , string='Nilai')

    @api.depends('mhs_id.name', 'semester', 'tahun')
    def _compute_name(self):
        for a in self:
            a.name = '%a - %a - %a' % (a.mhs_id.name, a.semester, a.tahun)

    def _compute_ips(self):
        pass
    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_settodraft(self):
        self.state = 'draft'

