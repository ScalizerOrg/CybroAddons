# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Bhagyadev KP (odoo@cybrosys.com)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
################################################################################
from odoo import api, fields, models, _


class AccountMove(models.Model):
    """
    Extend the base ResPartner model to include additional features.

    This class inherits from the base AccountMove model and adds functionality
    to mark customers as blacklisted.
    """
    _inherit = 'account.move'

    partner_blacklist_warning = fields.Text(
        compute='_compute_partner_blacklist_warning', help="warning message",
        string="warning"
    )

    @api.depends('partner_id')
    def _compute_partner_blacklist_warning(self):
        """Add warning message on invoice if the customer is blacklisted"""
        for rec in self:
            if rec.partner_id.blacklisted_partner:
                rec.partner_blacklist_warning = _(
                    'The %s is marked as blacklisted' % rec.partner_id.name
                )
            else:
                rec.partner_blacklist_warning = ''
