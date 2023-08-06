from typing import Optional
import pandas as pd
from OctopusAgile import Agile
import warnings

from .abstract import PricingCollector
from .misc import iso8601z


class Octopus(PricingCollector):
    country = 'UK'
    supplier = 'Octopus'
    timezone = 'Europe/London'
    unit = 'p£/kWh'

    def __init__(self, region_code: str, **kwargs):
        self.agile = Agile(region_code)
        self.price_name = f'{self.supplier}_{region_code}'
        super(Octopus, self).__init__(**kwargs)

    def get_data(
            self,
            interval: Optional[pd.Interval] = None,
    ) -> pd.DataFrame:
        if not interval:
            rates = self.agile.get_new_rates()
        else:
            date_from = iso8601z(interval.left)
            date_to = iso8601z(interval.right)
            if interval.length.days > 2:
                warnings.warn(
                    'You requested an interval larger than 2 days, '
                    'be advised that the response may not be complete')
            rates = self.agile.get_rates(date_from, date_to)

        rates = pd.DataFrame.from_dict(rates['date_rates'], orient='index')
        # noinspection PyTypeChecker
        rates.index = pd.to_datetime(rates.index)
        rates.rename(columns={0: 'value_inc_vat'}, inplace=True)
        rates = rates.tz_convert(self.timezone)
        rates.sort_index(inplace=True)
        rates['Unit'] = self.unit
        return rates
