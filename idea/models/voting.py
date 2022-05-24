from odoo import models, fields, api, _
#_ untuk translate

class voting(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'idea.voting' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel
        # (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk berlatih ttg voting'
    _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.

    name = fields.Char('Voting Number', size=64, required=True, index=True)
    date = fields.Date('Voting Date', default=fields.Date.context_today, readonly=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('voted', 'Voted'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    vote = fields.Selection([('yes', 'Yes'),
                              ('no', 'No'),
                              ('abstain', 'Abstain')], required=True, readonly=False)
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade", default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea_id',
                              domain="[('state', '=', 'done'),('active', '=', 'true')]")
    idea_date = fields.Date("Idea date", related='idea_id.date')
    #readonly=True, ondelete="cascade", states={'draft': [('readonly', False)]},
    def action_voted(self):
        self.state = 'voted'
    def action_canceled(self):
        self.state = 'canceled'
    def action_settodraft(self):
        self.state = 'draft'
    def action_yes(self):
        self.vote = 'yes'
    def action_no(self):
        self.vote ='no'
    def action_abstain(self):
        self.vote = 'abstain'
