# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.transaction import Transaction


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def search_rec_name(cls, name, clause):
        res = super(Invoice, cls).search_rec_name(name, clause)
        if Transaction().context.get('short_rec_name'):
            if clause[1].startswith('!') or clause[1].startswith('not '):
                bool_op = 'AND'
            else:
                bool_op = 'OR'
            return [bool_op,
                ('number',) + tuple(clause[1:]),
                ]
        return res
