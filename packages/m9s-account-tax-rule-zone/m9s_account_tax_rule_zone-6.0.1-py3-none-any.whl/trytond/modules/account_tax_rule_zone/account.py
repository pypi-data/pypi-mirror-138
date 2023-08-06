# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta


class TaxZone(ModelSQL, ModelView):
    'Tax Zone'
    __name__ = 'account.tax.zone'
    name = fields.Char('Name', required=True, translate=True,
           help='The name of the tax zone', select=True)
    countries = fields.One2Many('country.country', 'tax_zone', 'Countries')


class TaxRuleLineTemplate(metaclass=PoolMeta):
    __name__ = 'account.tax.rule.line.template'
    from_zone = fields.Many2One('account.tax.zone', 'From Zone',
        ondelete='RESTRICT')
    to_zone = fields.Many2One('account.tax.zone', 'To Zone',
        ondelete='RESTRICT')

    def _get_tax_rule_line_value(self, rule_line=None):
        value = super(TaxRuleLineTemplate, self)._get_tax_rule_line_value(
            rule_line=rule_line)
        if not rule_line or rule_line.from_zone != self.from_zone:
            value['from_zone'] = (
                self.from_zone.id if self.from_zone else None)
        if not rule_line or rule_line.to_zone != self.to_zone:
            value['to_zone'] = (
                self.to_zone.id if self.to_zone else None)
        return value


class TaxRuleLine(metaclass=PoolMeta):
    __name__ = 'account.tax.rule.line'
    from_zone = fields.Many2One('account.tax.zone', 'From Zone',
        ondelete='RESTRICT')
    to_zone = fields.Many2One('account.tax.zone', 'To Zone',
        ondelete='RESTRICT')


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    def _get_tax_rule_pattern(self):
        pool = Pool()
        try:
            SaleLine = pool.get('sale.line')
        except KeyError as e:
            SaleLine = None
        try:
            PurchaseLine = pool.get('purchase.line')
        except KeyError as e:
            PurchaseLine = None
        try:
            Work = pool.get('project.work')
        except KeyError as e:
            Work = None

        pattern = super(InvoiceLine, self)._get_tax_rule_pattern()
        from_zone, to_zone = None, None
        if getattr(self, 'origin'):
            origin = self.origin
            if (SaleLine
                    and isinstance(origin, SaleLine)
                    and self.origin.id >= 0):
                if origin.warehouse.address:
                    from_zone = origin.warehouse.address.country.tax_zone
                to_zone = origin.sale.shipment_address.country.tax_zone
            elif (PurchaseLine
                    and isinstance(origin, PurchaseLine)
                    and self.origin.id >= 0):
                from_zone = origin.purchase.invoice_address.country.tax_zone
                if origin.purchase.warehouse.address:
                    to_zone = (
                        origin.purchase.warehouse.address.country.tax_zone)
            elif (Work
                    and isinstance(origin, Work)
                    and self.origin.id >= 0):
                from_address = origin.company.party.address_get('invoice')
                if from_address and from_address.country:
                    from_zone = from_address.country.tax_zone
                to_address = origin.party.address_get('invoice')
                if to_address and to_address.country:
                    to_zone = to_address.country.tax_zone
        else:
            from_address = self.invoice.company.party.address_get('invoice')
            if from_address and from_address.country:
                from_zone = from_address.country.tax_zone
            to_address = self.invoice.party.address_get('invoice')
            if to_address and to_address.country:
                to_zone = to_address.country.tax_zone

        pattern['from_zone'] = from_zone.id if from_zone else None
        pattern['to_zone'] = to_zone.id if to_zone else None
        return pattern

    @fields.depends('origin')
    def on_change_product(self):
        super(InvoiceLine, self).on_change_product()

    @fields.depends('origin')
    def on_change_account(self):
        super(InvoiceLine, self).on_change_account()
