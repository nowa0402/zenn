import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    sample: str | None = Field(default=None)


# 基本形
# 環境変数なし
print(Settings().dict())
# {'sample': None}

# 環境変数設定
os.environ["sample"] = "settings_sample"
print(Settings().dict())

# 大文字でも可
os.environ["SAMPLE"] = "SETTINGS_SAMPLE"
print(Settings().dict())
