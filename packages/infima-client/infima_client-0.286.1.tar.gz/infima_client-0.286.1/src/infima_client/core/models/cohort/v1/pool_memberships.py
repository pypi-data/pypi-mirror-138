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

from infima_client.core.types import UNSET, Unset

T = TypeVar("T", bound="CohortV1PoolMemberships")


@define(auto_attribs=True)
class CohortV1PoolMemberships:
    """
    Attributes:
        cohorts (Union[Unset, List[str]]):
        cusip (Union[Unset, str]):
    """

    cohorts: Union[Unset, List[str]] = UNSET
    cusip: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cohorts: Union[Unset, List[str]] = UNSET
        if not isinstance(self.cohorts, Unset):
            cohorts = self.cohorts

        cusip = self.cusip

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cohorts is not UNSET:
            field_dict["cohorts"] = cohorts
        if cusip is not UNSET:
            field_dict["cusip"] = cusip

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cohorts = cast(List[str], d.pop("cohorts", UNSET))

        cusip = d.pop("cusip", UNSET)

        cohort_v1_pool_memberships = cls(
            cohorts=cohorts,
            cusip=cusip,
        )

        cohort_v1_pool_memberships.additional_properties = d
        return cohort_v1_pool_memberships

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
