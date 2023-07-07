from pathlib import Path

from pydantic import BaseModel, Field, validator


class CSVReader(BaseModel):
    """CSV読み込みクラス"""

    path: Path = Field(..., description="CSVパス")

    @validator("path")
    def validate_path(cls, path: Path) -> Path:
        """パス検査

        Args:
            path (Path): CSVパス

        Raises:
            ValueError: 検証失敗

        Returns:
            Path: CSVパス
        """
        # ファイル存在検証
        if not path.exists():
            raise ValueError(f"ファイルが存在しません:{path}")

        # 拡張子検証
        if path.suffix != ".csv":
            raise ValueError(f"拡張子に誤りがあります:{path.name}")

        return path
