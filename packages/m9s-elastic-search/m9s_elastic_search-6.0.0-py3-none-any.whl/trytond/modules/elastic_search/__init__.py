# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from . import configuration, index, ir

__all__ = ['register']


def register():
    Pool.register(
        configuration.Configuration,
        index.IndexBacklog,
        index.DocumentType,
        ir.Cron,
        module='elastic_search', type_='model')
