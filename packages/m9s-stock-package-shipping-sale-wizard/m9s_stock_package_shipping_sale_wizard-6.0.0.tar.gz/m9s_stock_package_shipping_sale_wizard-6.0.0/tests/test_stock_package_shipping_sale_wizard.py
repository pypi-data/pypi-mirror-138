# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class StockPackageShippingSaleWizardTestCase(ModuleTestCase):
    'Test Stock Package Shipping Sale Wizard module'
    module = 'stock_package_shipping_sale_wizard'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            StockPackageShippingSaleWizardTestCase))
    return suite
