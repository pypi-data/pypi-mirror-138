# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from . import invoice, stock

__all__ = ['register']


def register():
    Pool.register(
        stock.CreateSaleShippingStart,
        invoice.Invoice,
        module='stock_package_shipping_sale_wizard', type_='model')
    Pool.register(
        stock.CreateSaleShipping,
        module='stock_package_shipping_sale_wizard', type_='wizard')
