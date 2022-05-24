from odoo import models, fields, api, _

class detailtransaksi(models.Model):
    _name= 'perpus.detailtransaksi'
    _description= 'class untuk menyimpan detail transaksi'

    #atribute field
    name = fields.Char('ID detail transaksi', size=64, required=True, index=True)
    #name = fields.Integer("ID Detail Transaksi", compute="_compute_id", store=True, default=0)
    transaksi_ids = fields.Many2one('perpus.transaksi', string='ID transaksi', ondelete="cascade")
    transaksi_tanggalpinjam = fields.Date("Tanggal Peminjaman", related='transaksi_ids.tanggal_pinjam')
    buku_ids = fields.Many2one('perpus.buku', string='ID Buku',
                              ondelete="cascade", domain="[('status', '=', 'true')]")
    buku_biaya = fields.Integer("Biaya", related='buku_ids.biaya')
    #buku_status = fields.Boolean('Available', related='buku_ids.status')
    _sql_constraints = [('name_unik', 'unique(name)', _('ID detail sudah ada!!'))]
