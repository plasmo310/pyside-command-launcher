from dataclasses import dataclass
from typing import Any, Dict, List

from .interface import IJsonData


@dataclass
class CommandItemInfo(IJsonData):
    """コマンドアイテム情報"""

    name: str
    icon_color: str = ""
    icon_path: str = ""
    description: str = ""
    script_path: str = ""
    args: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Name": self.name,
            "IconColor": self.icon_color,
            "IconPath": self.icon_path,
            "Description": self.description,
            "ScriptPath": self.script_path,
            "Args": self.args,
        }

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "CommandItemInfo":
        return cls(
            name=data_dict["Name"],
            icon_color=data_dict.get("IconColor", ""),
            icon_path=data_dict.get("IconPath", ""),
            description=data_dict["Description"],
            script_path=data_dict["ScriptPath"],
            args=data_dict.get("Args", ""),
        )


@dataclass
class CategoryItemInfo(IJsonData):
    """カテゴリアイテム情報"""

    name: str
    icon_color: str
    icon_path: str
    command_item_info_list: List[CommandItemInfo]

    def item_count(self) -> int:
        return len(self.command_item_info_list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Name": self.name,
            "IconColor": self.icon_color,
            "IconPath": self.icon_path,
            "Items": [
                command_item_info.to_dict()
                for command_item_info in self.command_item_info_list
            ],
        }

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "CategoryItemInfo":
        return cls(
            name=data_dict["Name"],
            icon_color=data_dict["IconColor"],
            icon_path=data_dict["IconPath"],
            command_item_info_list=[
                CommandItemInfo.from_dict(command_item_info_dict)
                for command_item_info_dict in data_dict.get("Items", [])
            ],
        )


def load_category_item_info_list_from_dict(
    root_data_dict: Dict[str, Any],
) -> List[CategoryItemInfo]:
    """CategoryItemInfoリストの読込"""
    return [
        CategoryItemInfo.from_dict(category_item_info_dict)
        for category_item_info_dict in root_data_dict.get("Categories", [])
    ]
