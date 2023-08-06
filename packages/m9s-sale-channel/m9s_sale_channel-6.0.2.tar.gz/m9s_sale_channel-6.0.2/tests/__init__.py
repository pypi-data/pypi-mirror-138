# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.sale_channel.tests.test_sale_channel import (
        create_channel_sale, create_sale_channels, suite)
except ImportError:
    from .test_sale_channel import (
        create_channel_sale, create_sale_channels, suite)

__all__ = ['suite', 'create_sale_channels', 'create_channel_sale']
