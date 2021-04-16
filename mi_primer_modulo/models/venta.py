# -*- coding:utf-8 -*-

from odoo import  api, fields , models

from odoo.exceptions import  UserError

class Venta(models.Model):
    _name ='venta'
    name = fields.Char(string='Numero')
    cliente = fields.Char(string='Nombre cliente')
    fch_venta = fields.Date(string='Fecha')
    fch_vencimiento = fields.Datetime(string='Fecha vencimiento')
    cliente_frecuente = fields.Boolean(string='cliente frecuente')
    sexo = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino'),

    ], string='Sexo')

    edad = fields.Integer(string='Edad')
    peso = fields.Float(string='Peso')
    image = fields.Binary(string='foto')
    archivo = fields.Binary(string='archivo')

    socio =fields.Many2one(
        comodel_name='res.partner',
        string='Socio'
    )

    producto = fields.Many2one(
        comodel_name='productos.especializados',
        string='Producto'
    )

    categorias = fields.Many2many(
        comodel_name='productos.especializados',
        string='Categoria'
    )

    comentario = fields.Text(string='Comentario')


    state = fields.Selection([
        ('draft','Borrador'),
        ('done','Emitido'),
        ('cancel','Cancelado'),
        ('personalizado','Personalizado')
    ], string='Estado',default='draft')

    correlativo = fields.Char(string='Correlativo')
    detalles_ids = fields.One2many('venta.detalle' ,'venta_id', string='Detalles')
    currency_id = fields.Many2one('res.currency', 'Moneda')
    total_final = fields.Monetary(string='Total', compute='_compute_total')


    @api.depends('detalles_ids')

    def _compute_total(self):
        sub_total = 0

        for linea in self.detalles_ids:
            sub_total += linea.total
        self.total_final = sub_total


    def confirmar(self):
        self.state = 'done'

    def cancelar(self):
        self.state = 'cancel'
        self.comentario='esto es testing'
        ##self.cliente='testing'

    def unlink(self):
        print("HOLA MUNDO")

        if self.state != 'cancel':
            raise UserError("NO SE PUEDE ELIMINAR PORQUE NO ESTA EN ESTADO CANCELADO")

        else:
            return super(Venta, self).unlink()

    @api.model
    def create(self, variables):
        variables['cliente'] = variables['cliente'] + '!!!!!'
        secuencia_obj = self.env['ir.sequence']
        numero = secuencia_obj.next_by_code('mi_secuencia')
        variables['correlativo'] = numero
        return super(Venta, self).create(variables)

    def write(self, variables):
        print(variables)
        return super(Venta, self).write(variables)

    @api.onchange('cliente_frecuente')
    def _onchange_cliente_frecuente(self):
        self.peso += 1



class VentaDetalle(models.Model):
    _name = "venta.detalle"
    venta_id = fields.Many2one(comodel_name='venta',string='venta')
    producto = fields.Many2one('productos.especializados','Producto')
    precio = fields.Float(string='Precio')
    cantidad = fields.Float(string='Cantidad')
    total = fields.Monetary(string='Total')
    currency_id = fields.Many2one(related='venta_id.currency_id', string='Moneda')


    @api.onchange('precio','cantidad')
    def _onchange_total(self):
        self.total = self.precio * self.cantidad





















