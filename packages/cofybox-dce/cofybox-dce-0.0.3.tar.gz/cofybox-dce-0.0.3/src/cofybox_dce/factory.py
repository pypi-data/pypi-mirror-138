from typing import Dict

from .abstract import CollectorType, Collector
from .pricing import Octopus


def create_collector(collector_type: CollectorType, body: Dict) -> Collector:
    if collector_type == CollectorType.PRICE:
        supplier = body['supplier']
        if supplier == 'Octopus':
            region_code = body['regionCode']
            collector = Octopus(region_code=region_code)
        else:
            raise LookupError(f'Supplier {supplier} not supported, or unknown')
    else:
        raise NotImplementedError(f'Collector Type {collector_type} not yet '
                                  f'supported')
    return collector
