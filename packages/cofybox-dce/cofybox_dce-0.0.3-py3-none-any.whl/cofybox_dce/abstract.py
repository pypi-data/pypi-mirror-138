from abc import ABC
from enum import Enum
from typing import Optional

import pandas as pd


class CollectorType(Enum):
    """Enum of types of collectors"""
    PRICE = 'price'


class Collector(ABC):
    """
    Abstract class.
    Represents a connection to an external service where data is gathered.
    """
    def get_data(
            self,
            interval: Optional[pd.Interval] = None,
    ) -> pd.DataFrame:
        """
        Method to request data and return it as Pandas DataFrame with
        DateTimeIndex.

        If no interval is specified, "current" data (eg. "today"), should be
        returned.
        Dates should never be timezone naive.

        If a geographic region is known, the returned DataFrame should have
        a timezone-localised index.
        """
        raise NotImplementedError('To be implemented by subclass')


class PricingCollector(Collector, ABC):
    """Abstract collector for pricing data"""
    country: str = NotImplemented
    supplier: str = NotImplemented
    timezone: str = NotImplemented
    unit: str = NotImplemented
