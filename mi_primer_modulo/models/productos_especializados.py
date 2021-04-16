# -*- coding:utf-8 -*-

from odoo import  api, fields , models

class ProductosEspecializados(models.Model):
    _name ='productos.especializados'
    name = fields.Char(string='Descripcion')
    active = fields.Boolean(string='Activo' , default=True)
