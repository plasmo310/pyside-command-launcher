import abc
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="IJsonData")


class IJsonData(abc.ABC):
    """JSONデータ変換インターフェイス"""

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abc.abstractmethod
    def from_dict(cls: Type[T], data_dict: Dict[str, Any]) -> T:
        pass
