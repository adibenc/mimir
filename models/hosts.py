# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Hosts(models.Model):
    _name = 'mimir.hosts'
    _description = 'mimir.hosts'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(name="Name", required=True, )
    ip = fields.Char(name="Ip", required=True, tracking=True)
    ports = fields.Char(name="Ports", required=True, default="22")
    username = fields.Char(name="Username")
    
    # wip related
    gateway = fields.Char(name="Gateway")
    subnet = fields.Char(name="Subnet")
    parent = fields.Char(name="Parent")

    # wip
    vendor = fields.Many2one("res.partner", string="Vendor", help="Vendor of the host who manage the host")
    vendor_pic = fields.Many2one("res.partner", string="Vendor PIC")
    owner = fields.Many2one("res.partner", string="Owner", help="Owner of the host")
    owner_pic = fields.Many2one("res.partner", string="Owner PIC", help="Owner's PIC of the host")
    pic = fields.Many2one("res.partner", string="PIC", help="In house pic of the host relative to your company")

    internal_note = fields.Char(name="Internal Note")
    tag = fields.Char(name="Tag")
    os = fields.Char(name="OS", help="Operating system")
    project = fields.Char(name="Project")
    cpu = fields.Integer(name="Cpu")
    ram = fields.Integer(name="Ram")
    disk = fields.Integer(name="Disk")

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

