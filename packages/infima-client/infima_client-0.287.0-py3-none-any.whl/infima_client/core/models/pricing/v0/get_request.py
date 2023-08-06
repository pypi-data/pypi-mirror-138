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
from infima_client.core.types import UNSET, Unset

T = TypeVar("T", bound="PricingV0GetRequest")


@define(auto_attribs=True)
class PricingV0GetRequest:
    """
    Attributes:
        as_of (Union[Unset, CoreDate]):
        symbols (Union[Unset, List[str]]): CUSIPs or cohorts to fetch individual pricing predictions. Example:
            ['31417EUD1'].
    """

    as_of: Union[Unset, CoreDate] = UNSET
    symbols: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        as_of: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.as_of, Unset):
            as_of = self.as_of.to_dict()

        symbols: Union[Unset, List[str]] = UNSET
        if not isinstance(self.symbols, Unset):
            symbols = self.symbols

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if as_of is not UNSET:
            field_dict["asOf"] = as_of
        if symbols is not UNSET:
            field_dict["symbols"] = symbols

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

        symbols = cast(List[str], d.pop("symbols", UNSET))

        pricing_v0_get_request = cls(
            as_of=as_of,
            symbols=symbols,
        )

        pricing_v0_get_request.additional_properties = d
        return pricing_v0_get_request

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
