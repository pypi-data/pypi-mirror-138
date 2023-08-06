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

from infima_client.core.models.core.factor_date import CoreFactorDate
from infima_client.core.types import UNSET, Unset

T = TypeVar("T", bound="CoreFactorDateRange")


@define(auto_attribs=True)
class CoreFactorDateRange:
    """
    Attributes:
        end (Union[Unset, CoreFactorDate]):
        start (Union[Unset, CoreFactorDate]):
    """

    end: Union[Unset, CoreFactorDate] = UNSET
    start: Union[Unset, CoreFactorDate] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        end: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.to_dict()

        start: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if end is not UNSET:
            field_dict["end"] = end
        if start is not UNSET:
            field_dict["start"] = start

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _end = d.pop("end", UNSET)
        end: Union[Unset, CoreFactorDate]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = CoreFactorDate.from_dict(_end)

        _start = d.pop("start", UNSET)
        start: Union[Unset, CoreFactorDate]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = CoreFactorDate.from_dict(_start)

        core_factor_date_range = cls(
            end=end,
            start=start,
        )

        core_factor_date_range.additional_properties = d
        return core_factor_date_range

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
