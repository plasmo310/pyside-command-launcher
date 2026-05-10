from __future__ import annotations

import sys
from enum import Enum
from typing import Optional


class CommandType(Enum):
    """コマンドタイプ"""

    BAT = ".bat"
    PS1 = ".ps1"
    EXE = ".exe"
    SHELL = ".sh"
    COMMAND = ".command"
    APP = ".app"

    @classmethod
    def from_extension(cls, extention: str) -> Optional[CommandType]:
        """拡張子からコマンド種別を返却する"""
        for member in cls:
            if member.value == extention.lower():
                return member
        return None

    @classmethod
    def viewable_types(cls) -> set[CommandType]:
        """テキストとして表示可能なコマンド種別のセット"""
        return {cls.BAT, cls.SHELL, cls.PS1, cls.COMMAND}


class PlatformType(Enum):
    """プラットフォーム種別"""

    WINDOWS = "win32"
    MAC = "darwin"

    @classmethod
    def current(cls) -> PlatformType:
        """実行中のプラットフォーム種別を返却する"""
        for member in cls:
            if sys.platform.startswith(member.value):
                return member
        raise RuntimeError(f"Unsupported platform: {sys.platform}")
