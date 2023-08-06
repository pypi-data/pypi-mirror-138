# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from trytond.config import config
from trytond.exceptions import UserWarning
from trytond.i18n import gettext
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.pyson import Bool, Equal, Eval, If, Not, PYSONEncoder
from trytond.transaction import Transaction
from trytond.wizard import (
    Button, StateAction, StateTransition, StateView, Wizard)

try:
    from trytond.modules.printing.printing import (
        PRINT_USER, get_report_file, print_document)
except ImportError:
    print_document = None

# Module printing
_label_printer_uri_printing = config.get('printing', 'label_printer_uri',
    default='')
# Module printer_cups
_printer_cups = config.get('printer_cups', 'redirect_model', default=None)
_label_printer_uri_printer_cups = config.get(
    'printer_cups', 'label_printer_uri', default=None)


class CreateSaleShipping(Wizard):
    'Create Sale Shipping'
    __name__ = 'stock.shipment.sale.create_shipping'

    start = StateView('stock.shipment.sale.create_shipping.start',
        'stock_package_shipping_sale_wizard.create_shipping_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Create', 'create_', 'tryton-ok', default=True),
            ])
    create_ = StateTransition()

    def get_package(self):
        pool = Pool()
        Package = pool.get('stock.package')

        package = Package(
            shipment=self.start.shipment,
            type=self.start.package_type,
            )
        return package

    def transition_create_(self):
        pool = Pool()
        CreateShipping = pool.get('stock.shipment.create_shipping',
            type='wizard')

        shipment = self.start.shipment

        # Remove the old shipment reference in case another
        # label shall be fetched
        if shipment.reference:
            raise UserWarning(
                'already_shipped',
                gettext(
                    'stock_package_shipping_sale_wizard.already_shipped',
                    shipment=shipment.number))
            shipment.reference = None
            shipment.save()
        # Replace the shipment carrier if another was selected in this wizard,
        # otherwise the shipping wizard will not work correctly
        if shipment.carrier != self.start.carrier:
            shipment.carrier = self.start.carrier
            shipment.save()

        packages_to_send = [p for p in shipment.root_packages
            if not p.shipping_reference]
        if not packages_to_send:
            package = self.get_package()
            package.save()
        else:
            package = packages_to_send[0]
        shipment_context = {
            'active_model': 'stock.shipment.out',
            'active_id': shipment.id,
            'active_ids': [shipment.id],
            }

        session_id, _, _ = CreateShipping.create()
        create_shipping = CreateShipping(session_id)

        with Transaction().set_context(shipment_context):
            provider = create_shipping.transition_start()
            create_shipping.delete(session_id)
            model = 'stock.shipment.create_shipping.' + provider
            CreateShippingProvider = pool.get(model, type='wizard')
            session_id, _, _ = CreateShippingProvider.create()
            create_shipping_prov = CreateShippingProvider(session_id)
            create_shipping_prov.execute(session_id, {}, 'start')
            create_shipping_prov.delete(session_id)

        # Module printing
        if print_document and _label_printer_uri_printing:
            file_path = get_report_file(package.shipping_label, ext='pdf')
            print_document(file_path, print_user=PRINT_USER,
                printer_uri=_label_printer_uri_printing)

        # Module printer_cups
        try:
            Printer = pool.get('printer')
        except KeyError:
            Printer = None
        if Printer and _printer_cups:
            domain = []
            if _label_printer_uri_printer_cups:
                domain.append(('name', '=', _label_printer_uri_printer_cups))
            printers = Printer.search(domain)
            printer = printers[0]
            file_path = Printer.get_report_file(
                package.shipping_label, ext='pdf')
            printer.print_file(file_path, package.rec_name)

        return 'start'


class CreateSaleShippingStart(ModelView):
    'Create Sale Shipping Start'
    __name__ = 'stock.shipment.sale.create_shipping.start'
    company = fields.Many2One('company.company', 'Company', required=True,
        domain=[
            ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
            ])
    invoice = fields.Many2One('account.invoice', 'Invoice',
        domain=[
            ('state', 'in', ['posted', 'paid']),
            ('type', '=', 'out'),
            ('total_amount', '>', Decimal('0.0')),
            ],
        context={'short_rec_name': True})
    sales = fields.Function(fields.Text('Available Sales',
            depends=['invoice']), 'on_change_with_sales')
    sale = fields.Many2One('sale.sale', 'Sale',
        domain=[
            ('state', 'in', ['processing', 'done']),
            ])
    shipments = fields.Function(fields.Text('Available Shipments',
            depends=['sale', 'invoice']), 'on_change_with_shipments')
    shipment = fields.Many2One('stock.shipment.out', 'Shipment',
        required=True, depends=['sale', 'shipments'],
            domain=[
                ('state', 'in', ['packed', 'done']),
                ])
    carrier = fields.Many2One('carrier', 'Carrier',
        required=True, depends=['sale'])
    package_type = fields.Many2One('stock.package.type', 'Package Type')

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    @staticmethod
    def default_package_type():
        PackageType = Pool().get('stock.package.type')

        types = PackageType.search([])
        if types:
            return types[0].id

    @fields.depends('invoice', 'sale')
    def on_change_invoice(self):
        if self.invoice:
            invoice = self.invoice
            if len(invoice.sales) == 1:
                self.sale = invoice.sales[0].id
                self.on_change_sale()
                self.shipments = self.on_change_with_shipments()
            elif len(invoice.sales) == 0:
                    self.sale = None
                    self.shipment = None
                    self.shipments = ''
                    self.carrier = None
            elif len(invoice.sales) > 1:
                if self.sale:
                    if invoice not in self.sale.invoices:
                        self.sale = None
                        self.shipment = None
                        self.shipments = ''
                        self.carrier = None

    @fields.depends('invoice', 'sale')
    def on_change_sale(self):
        if self.sale:
            sale = self.sale
            if len(sale.shipments) == 1:
                self.shipment = sale.shipments[0].id
            self.carrier = sale.carrier
            if self.invoice not in sale.invoices:
                if len(sale.invoices) == 1:
                    self.invoice = sale.invoices[0].id
                    self.sales = self.on_change_with_sales()
                else:
                    self.invoice = None
        else:
            self.shipment = None
            self.shipments = ''
            self.carrier = None

    @fields.depends('carrier', 'shipment', 'sale')
    def on_change_shipment(self):
        if not self.carrier and self.shipment:
            self.carrier = self.shipment.carrier
        if self.shipment and self.sale:
            if self.shipment not in self.sale.shipments:
                self.invoice = None
                self.sale = None
                self.sales = ''
                self.shipments = ''

    @fields.depends('invoice')
    def on_change_with_sales(self, name=None):
        if self.invoice:
            return '\n'.join(
                [' '.join([s.number, s.party.rec_name])
                    for s in self.invoice.sales])
        else:
            return ''

    @fields.depends('sale')
    def on_change_with_shipments(self, name=None):
        if self.sale:
            return '\n'.join(
                [' '.join([s.rec_name, s.delivery_address.rec_name])
                    for s in self.sale.shipments])
        else:
            return ''
