from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    _name = "school.student"
    _inherit='mail.thread'
    _description = "Students Record"

    name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    is_child = fields.Boolean(string="IS Child ?", tracking=True)
    notes = fields.Text(string="Notes")
    gender = fields.Selection([('male',"Male"),('female',"Female"),('others','Others')],string="Gender", tracking=True)
    capitalized_name = fields.Char(string="Capitalized Name", compute='_compute_capitalizes_name', store=True)
    ref=fields.Char(string="Refrence", default=lambda self: _('New'))
    teacher_id = fields.Many2one('school.teacher',string="Teacher")
    active = fields.Boolean(default=True)
    tag_ids=fields.Many2many('res.partner.category','school_student_tag_rel', 'student_id', 'tag_id', string="Tags")



    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'] .next_by_code('School.Student')
        return super(SchoolStudent, self).create(vals_list)

    @api.constrains('is_child', 'age')
    def _check_child_age(self):
        for rec in self:
            if rec.is_child and rec.age == 0:
                raise ValidationError(_("Age has to be recorded !"))

    @api.depends('name')
    def _compute_capitalizes_name(self):
        for rec in self:
            if self.name:
                self.capitalized_name = self.name.upper()
            else:
                self.capitalized_name=''


    @api.onchange('age')
    def _onchange_age(self):
        if self.age <=10:
            self.is_child = True
        else:
            self.is_child = False