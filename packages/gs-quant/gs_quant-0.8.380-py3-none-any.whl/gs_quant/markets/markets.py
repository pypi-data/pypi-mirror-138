"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
from abc import ABC
import datetime as dt
from gs_quant.base import Market, RiskKey
from gs_quant.common import PricingLocation
from gs_quant.context_base import do_not_serialise
from gs_quant.datetime.date import prev_business_date
from gs_quant.target.common import CloseMarket as _CloseMarket, LiveMarket as _LiveMarket, \
    OverlayMarket as _OverlayMarket, RelativeMarket as _RelativeMarket, TimestampedMarket as _TimestampedMarket, \
    RefMarket as _RefMarket
from gs_quant.target.data import MarketDataCoordinate as __MarketDataCoordinate, \
    MarketDataCoordinateValue as __MarketDataCoordinateValue
import re
from typing import Mapping, Optional, Tuple, Union


def historical_risk_key(risk_key: RiskKey) -> RiskKey:
    market = LocationOnlyMarket(risk_key.market.location)
    return RiskKey(risk_key.provider, None, market, risk_key.params, risk_key.scenario, risk_key.risk_measure)


def market_location(location: Optional[PricingLocation] = None) -> PricingLocation:
    """Determine PricingLocation and ensure passed optional 'location' does not
    conflict with the current PricingContext's market_data_location

    :param location: optional PricingLocation
    :return: PricingLocation
    """
    from .core import PricingContext
    default = PricingContext.current.market_data_location

    if location is None:
        return default or PricingLocation.LDN
    elif default and default != location:
        raise ValueError(f'Inconsistent market locations of {default} and {location} specified')
    else:
        return location


def close_market_date(_location: Optional[Union[PricingLocation, str]] = None,
                      date: Optional[dt.date] = None) -> dt.date:
    """Determine market data date based on current location (to infer calendar)
    and current pricing date

    :param _location: location (deprecated)
    :param date: pricing date
    :return: close market date
    """
    from .core import PricingContext
    date = date or PricingContext.current.pricing_date

    if date == dt.date.today():
        # Don't use the calendars argument here as external users do not (yet) have access to that dataset
        date = prev_business_date(date)

    return date


class MarketDataCoordinate(__MarketDataCoordinate):

    def __repr__(self):
        ret = "_".join(f or '' for f in (self.mkt_type, self.mkt_asset, self.mkt_class))

        if self.mkt_point:
            ret += '_' + ','.join(self.mkt_point)

        if self.mkt_quoting_style:
            ret += f'.{self.mkt_quoting_style}'

        return ret

    @classmethod
    def from_string(cls, value: str):
        from gs_quant.api.gs.data import GsDataApi
        ret = GsDataApi._coordinate_from_str(value)
        if len(ret.__mkt_point) == 1:
            # Unfortunately _,; have all been used as delimiters in various places
            ret.__mkt_point = tuple(re.split('[,_;]', ret.__mkt_point[0]))

        return ret


class MarketDataCoordinateValue(__MarketDataCoordinateValue):

    def __repr__(self):
        return f'{self.coordinate} --> {self.value}'


Coordinates = Tuple[MarketDataCoordinate, ...]
MarketDataMap = Mapping[MarketDataCoordinate, float]


class MarketWithData(Market, ABC):

    def __init__(self, market_data: Optional[MarketDataMap] = None):
        super().__init__()
        if market_data:
            self.__redact(market_data)
        else:
            self.__market_data = {}
            self.__redacted_coordinates = ()

    @property
    @do_not_serialise
    def market_data_dict(self) -> MarketDataMap:
        return self.__market_data

    @property
    @do_not_serialise
    def market_data(self) -> Tuple[MarketDataCoordinateValue, ...]:
        # Market data that should be supplied in pricing requests. For close and timestamped markets this will be
        # empty but for live it should be supplied (as a new live market will return different values)
        return ()

    @property
    @do_not_serialise
    def redacted_coordinates(self) -> Coordinates:
        return self.__redacted_coordinates

    def clone_with_market_data(self, market_data: MarketDataMap):
        ret = self.clone()
        ret.__redact(market_data)
        return ret

    def __redact(self, market_data: MarketDataMap):
        # filter market_data map input to separate permissioned and redacted coordinates. redacted coordinates have
        # 'redacted' as their coordinate value
        self.__market_data = dict(filter(lambda elem: elem[1] != 'redacted', market_data.items()))
        self.__redacted_coordinates = tuple(key for (key, value) in market_data.items() if value == 'redacted')


class LocationOnlyMarket(Market):

    def __init__(self, location: Optional[Union[str, PricingLocation]]):
        super().__init__()
        self.__location = location

    @property
    def location(self) -> PricingLocation:
        return self.__location


class CloseMarket(_CloseMarket, MarketWithData):
    """Market Object which captures market data based on market_location
    and close_market_date
    """
    __date_cache = {}

    def __init__(self,
                 date: Optional[dt.date] = None,
                 location: Optional[Union[str, PricingLocation]] = None,
                 check: Optional[bool] = True,
                 market_data: Optional[MarketDataMap] = None):
        _CloseMarket.__init__(self, date=date, location=location)
        MarketWithData.__init__(self, market_data=market_data)
        self.check = check

    def __repr__(self):
        return f'{self.date} ({self.location.value})'

    @_CloseMarket.location.getter
    def location(self) -> PricingLocation:
        location = super().location
        if location is not None and not self.check:
            return location
        else:
            return market_location(super().location)

    @_CloseMarket.date.getter
    def date(self) -> dt.date:
        date = super().date
        if date is not None and not self.check:
            return date
        else:
            return close_market_date(self.location, super().date)


class TimestampedMarket(_TimestampedMarket, MarketWithData):
    """Market Object which captures market data based on location
    and timestamp
    """

    def __init__(self,
                 timestamp: dt.datetime,
                 location: Optional[Union[str, PricingLocation]] = None,
                 market_data: Optional[MarketDataMap] = None):
        _TimestampedMarket.__init__(self, timestamp=timestamp, location=location)
        MarketWithData.__init__(self, market_data=market_data)

    def __repr__(self):
        return f'{self.timestamp} ({self.location.value})'

    @_TimestampedMarket.location.getter
    def location(self) -> PricingLocation:
        return market_location(super().location)


class LiveMarket(_LiveMarket, MarketWithData):
    """Market Object which captures market data based on location
    and time at runtime
    """

    def __init__(self,
                 location: Optional[Union[str, PricingLocation]] = None,
                 market_data: Optional[MarketDataMap] = None):
        _LiveMarket.__init__(self, location=location)
        MarketWithData.__init__(self, market_data=market_data)

    def __repr__(self):
        return f'Live ({self.location.value})'

    @MarketWithData.market_data.getter
    @do_not_serialise
    def market_data(self) -> Tuple[MarketDataCoordinateValue, ...]:
        return tuple(MarketDataCoordinateValue(coordinate=c, value=v) for c, v in self.market_data_dict.items())

    @_LiveMarket.location.getter
    def location(self) -> PricingLocation:
        return market_location(super().location)


class OverlayMarket(_OverlayMarket, Market):
    """Market Object which overlays a base Market object (eg: CloseMarket, LiveMarket or
    TimestampedMarket) with a MarketDataMap (a map of market coordinate to float)
    """

    def __init__(self, market_data: Optional[MarketDataMap] = None, base_market: Optional[Market] = None):
        super().__init__(base_market=base_market or CloseMarket(), market_data=())
        self.__market_data = market_data or {}

    def __getitem__(self, item):
        if isinstance(item, str):
            item = MarketDataCoordinate.from_string(item)

        value = self.__market_data.get(item)
        if value is None:
            value = self.base_market.market_data_dict[item]

        return value

    def __setitem__(self, key, value):
        if isinstance(key, str):
            key = MarketDataCoordinate.from_string(key)

        if key in self.redacted_coordinates:
            raise KeyError(f'{key} cannot be overridden')

        current_value = self.__market_data.get(key)
        base_value = self.base_market.market_data_dict.get(key)

        if current_value is not None:
            if value == base_value:
                self.__market_data.pop(key)
                Market._property_changed(self, 'market_data')
        elif value != base_value:
            self.__market_data[key] = value
            Market._property_changed(self, 'market_data')

    def __repr__(self):
        return f'Overlay ({id(self)}): {repr(self.base_market)}'

    @_OverlayMarket.market_data.getter
    def market_data(self) -> Tuple[MarketDataCoordinateValue, ...]:
        return tuple(MarketDataCoordinateValue(coordinate=c, value=v) for c, v in self.__market_data.items()) +\
            self.base_market.market_data

    @property
    @do_not_serialise
    def market_data_dict(self) -> MarketDataMap:
        return {**{p.coordinate: p.value for p in self.market_data}, **self.base_market.market_data_dict}

    @Market.location.getter
    @do_not_serialise
    def location(self) -> PricingLocation:
        return self.base_market.location

    @property
    @do_not_serialise
    def coordinates(self) -> Coordinates:
        return tuple(self.__market_data.keys()) + tuple(self.base_market.market_data_dict.keys())

    @property
    @do_not_serialise
    def redacted_coordinates(self) -> Coordinates:
        return self.base_market.redacted_coordinates


class RefMarket(_RefMarket, Market):
    """Market Object which represents a Reference to a Market
    """

    def __init__(self, market_ref: str):
        super().__init__(market_ref='')
        self.__market_ref = market_ref

    def __repr__(self):
        return f'Market Ref ({id(self)})'

    @Market.location.getter
    def location(self) -> PricingLocation:
        return market_location(super().location)


class RelativeMarket(_RelativeMarket, Market):
    """Market Object which captures the change between two Market Objects
    (to_market and from_market)
    """

    def __init__(self, from_market: Market, to_market: Market):
        super().__init__(from_market=from_market, to_market=to_market)

    def __repr__(self):
        return f'{repr(self.from_market)} -> {repr(self.to_market)}'

    @Market.location.getter
    def location(self) -> PricingLocation:
        return self.from_market.location if self.from_market.location == self.to_market.location else None
