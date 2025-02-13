# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Vishnu KP (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MealsPlanning(models.Model):
    """By using this model user can specify the time range and pos session"""
    _name = 'meals.planning'
    _description = "Product Planning"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True,
                       help='Name for Product Planning', copy=False)
    pos_ids = fields.Many2many('pos.session', string='Shops',
                               copy=False, help='Choose PoS Sessions',
                               required=True)
    time_from = fields.Float(string='From', required=True,
                             help='Add from time(24hr)')
    time_to = fields.Float(string='To', required=True, help='Add to time(24hr)')
    menu_product_ids = fields.Many2many('product.product',
                                       string='Product',
                                       domain=[('available_in_pos', '=', True)])

    state = fields.Selection([('activated', 'Activated'),
                              ('deactivated', 'Deactivated')],
                             default='deactivated')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    @api.constrains('time_from', 'time_to')
    def _check_time_range(self):
        """Validation for from time and to time"""
        if self.time_from >= self.time_to:
            raise ValidationError('From time must be less than to time!')
        elif self.time_from > 24.0 or self.time_to > 24.0:
            raise ValidationError(
                'Time value greater than 24 is not valid!')

    def action_activate_meals_plan(self):
        """Change state to activate"""
        self.write({
            'state': 'activated'})

    def action_deactivate_meals_plan(self):
        """Change state to deactivate"""
        self.write({
            'state': 'deactivated'})


