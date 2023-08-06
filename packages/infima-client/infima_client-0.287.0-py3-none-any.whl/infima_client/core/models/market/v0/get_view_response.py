from typing import (
    Any,
    BinaryIO,
    Dict,
    List,
    Optional,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from attr import define, field

from infima_client.core.models.core.date import CoreDate
from infima_client.core.models.core.period import CorePeriod
from infima_client.core.models.market.v0.market_view_row import MarketV0MarketViewRow
from infima_client.core.types import UNSET, Unset

T = TypeVar("T", bound="MarketV0GetViewResponse")


@define(auto_attribs=True)
class MarketV0GetViewResponse:
    """
    Attributes:
        as_of (Union[Unset, CoreDate]):
        historical_periods (Union[Unset, List[CorePeriod]]):
        predicted_periods (Union[Unset, List[CorePeriod]]):
        rows (Union[Unset, List[MarketV0MarketViewRow]]):
    """

    as_of: Union[Unset, CoreDate] = UNSET
    historical_periods: Union[Unset, List[CorePeriod]] = UNSET
    predicted_periods: Union[Unset, List[CorePeriod]] = UNSET
    rows: Union[Unset, List[MarketV0MarketViewRow]] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        as_of: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.as_of, Unset):
            as_of = self.as_of.to_dict()

        historical_periods: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.historical_periods, Unset):
            historical_periods = []
            for historical_periods_item_data in self.historical_periods:
                historical_periods_item = historical_periods_item_data.to_dict()

                historical_periods.append(historical_periods_item)

        predicted_periods: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.predicted_periods, Unset):
            predicted_periods = []
            for predicted_periods_item_data in self.predicted_periods:
                predicted_periods_item = predicted_periods_item_data.to_dict()

                predicted_periods.append(predicted_periods_item)

        rows: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data.to_dict()

                rows.append(rows_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if as_of is not UNSET:
            field_dict["asOf"] = as_of
        if historical_periods is not UNSET:
            field_dict["historicalPeriods"] = historical_periods
        if predicted_periods is not UNSET:
            field_dict["predictedPeriods"] = predicted_periods
        if rows is not UNSET:
            field_dict["rows"] = rows

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _as_of = d.pop("asOf", UNSET)
        as_of: Union[Unset, CoreDate]
        if isinstance(_as_of, Unset):
            as_of = UNSET
        else:
            as_of = CoreDate.from_dict(_as_of)

        historical_periods = []
        _historical_periods = d.pop("historicalPeriods", UNSET)
        for historical_periods_item_data in _historical_periods or []:
            historical_periods_item = CorePeriod.from_dict(historical_periods_item_data)

            historical_periods.append(historical_periods_item)

        predicted_periods = []
        _predicted_periods = d.pop("predictedPeriods", UNSET)
        for predicted_periods_item_data in _predicted_periods or []:
            predicted_periods_item = CorePeriod.from_dict(predicted_periods_item_data)

            predicted_periods.append(predicted_periods_item)

        rows = []
        _rows = d.pop("rows", UNSET)
        for rows_item_data in _rows or []:
            rows_item = MarketV0MarketViewRow.from_dict(rows_item_data)

            rows.append(rows_item)

        market_v0_get_view_response = cls(
            as_of=as_of,
            historical_periods=historical_periods,
            predicted_periods=predicted_periods,
            rows=rows,
        )

        market_v0_get_view_response.additional_properties = d
        return market_v0_get_view_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
