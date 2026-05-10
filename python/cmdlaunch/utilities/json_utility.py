import json
from typing import Any, Dict


class JsonUtility:
    """JSON処理汎用クラス"""

    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """JSONファイルの読込"""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_json(filepath: str, data: Any, indent: int = 2):
        """JSONファイルの保存"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
