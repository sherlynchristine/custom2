from odoo import models, fields, api, _
#_ untuk translate

class detail_khs(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.detail_khs' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel
        # (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan DETAIL KHS'
    _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.

    #name = fields.Char('name', size=64, index=True)
    #name = fields.Char('Name apa ya', size=64, required=True, index=True)
    name = fields.Char(compute="_compute_name2", store=True, recursive=True)
    grade = fields.Selection([('A', 'A'),
                              ('B+', 'B+'),
                              ('B', 'B'),
                              ('C+', 'C+'),
                              ('C', 'C'),
                              ('D', 'D'),
                              ('E', 'E')], 'Grade', required=True, Readonly=False)
    total = fields.Float("Total", compute="_compute_total", store=True, default=0)
    mk_id = fields.Many2one('nilai.mk', string='Mata Kuliah',
                            domain="[('state', '=', 'done'),('active', '=', 'true')]")
    #sks_id = fields.Many2one("SKS MK", related='mk_id.sks')
    khs_id = fields.Many2one('nilai.khs', string="kahaes", readonly=True, ondelete="cascade")

    def _compute_total(self):
        pass

    @api.depends('khs_id.name', 'mk_id.name')
    def _compute_name(self):
        for a in self:
            a.name = '%a - %a' % (a.khs_id.name, a.mk_id.name)