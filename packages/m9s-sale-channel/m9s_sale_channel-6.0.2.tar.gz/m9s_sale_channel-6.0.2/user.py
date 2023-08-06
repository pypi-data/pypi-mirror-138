# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction


class User(metaclass=PoolMeta):
    __name__ = "res.user"

    current_channel = fields.Many2One('sale.channel', 'Current Channel',
        domain=[
            ('company', '=', Eval('company', -1)),
            ], depends=['company'],
        )

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._preferences_fields.extend([
            'current_channel',
        ])
        cls._context_fields.insert(0, 'current_channel')

    def get_default_channel(self):
        Channel = Pool().get('sale.channel')

        company_id = (Transaction().context.get('company')
            or self.company and self.company.id)
        channels = Channel.search([
                ('company', '=', company_id),
                ])
        if channels:
            return channels[0]

    @fields.depends('company')
    def on_change_company(self):
        super().on_change_company()
        self.current_channel = self.get_default_channel()

    def get_status_bar(self, name):
        status = super().get_status_bar(name)
        if self.current_channel:
            status += ' - %s' % (self.current_channel.name)
        return status
