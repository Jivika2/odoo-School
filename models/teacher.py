from odoo import api, fields, models

class SchoolTeacher(models.Model):
    _name="school.teacher"
    _inherits = {'school.student': 'related_student_id'}
    _description ="Teacher Recoder"
    _rec_name="ref"

    name=fields.Char(string="Name", required=True)
   
    gender = fields.Selection([('male','Male'), ('female','Female'), ('others','Others')], string="Gender", tracking=True)
    ref = fields.Char(string="Reference", required=True)
    active = fields.Boolean(default=True)
    related_student_id = fields.Many2many('school.student',string="Related Student ID")



    def name_get(self):
        res=[]
        for rec in self:
            name=f'{rec.ref} - {rec.name}'
            res.append((rec.id,name))
        return res 

