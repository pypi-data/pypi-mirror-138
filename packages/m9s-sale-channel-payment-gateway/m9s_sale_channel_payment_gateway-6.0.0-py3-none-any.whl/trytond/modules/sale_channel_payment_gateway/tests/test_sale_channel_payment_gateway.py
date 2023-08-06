# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from trytond.tests.test_tryton import suite as test_suite

# We run the test suites of the dependent modules if anything changed on their
# behavior
from trytond.modules.sale_channel.tests.test_sale_channel import (
    SaleChannelTestCase)
from trytond.modules.sale_payment_gateway.tests.test_sale_payment_gateway import (
    SalePaymentGatewayTestCase)


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleChannelTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SalePaymentGatewayTestCase))
    return suite
