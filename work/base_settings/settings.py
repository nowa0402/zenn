import os

import boto3
from pydantic import BaseSettings, Field

# class Settings(BaseSettings):
#     sample: str | None = Field(default=None)


# # 基本形
# # 環境変数なし
# print(Settings().dict())
# # {'sample': None}

# # 環境変数設定
# os.environ["sample"] = "settings_sample"
# print(Settings().dict())

# # 大文字でも可
# os.environ["SAMPLE"] = "SETTINGS_SAMPLE"
# print(Settings().dict())


class ENVSettings(BaseSettings):
    api_key: str | None = Field(default=None, env="api_sample")


# 設定無し
print(ENVSettings().dict())
# {"api_key": None}

# envを指定するとenvの環境変数のみに対応されます。
os.environ["api_key"] = "aaaaabbbbbccccc"
print(ENVSettings().dict())
# {'api_key': None}


os.environ["api_sample"] = "dddddeeeeefffff"
print(ENVSettings().dict())
# {'api_key': 'dddddeeeeefffff'}

# 大文字も反映
os.environ["API_SAMPLE"] = "DDDDDEEEEEFFFFF"
print(ENVSettings().dict())
# {'api_key': 'DDDDDEEEEEFFFFF'}


class SettingsCase(BaseSettings):
    name: str | None = Field(default=None, env="NAME_KEY")

    class Config:
        # 小文字・大文字区別を行う
        case_sensitive = True


os.environ["name_key"] = "xxxxxyyyyyzzzzz"
print(SettingsCase().dict())
# envが大文字のため対応しない
# {'name': None}


os.environ["NAME_KEY"] = "XXXXXYYYYYZZZZZ"
print(SettingsCase().dict())
# {'name': 'XXXXXYYYYYZZZZZ'}


# dot_env
class DotSettings(BaseSettings):
    dot_env: str = Field(default=None)

    class Config:
        env_file = "./work/base_settings/.env"


print(DotSettings().dict())


# 具体例
class ProfileSettings(BaseSettings):
    profile_name: str | None = Field(default=None, env="AWS_PROFILE_NAME")

    class Config:
        env_file = ".env"
        case_sensitive = True


print(ProfileSettings().dict(exclude_none=True))
# {}

# None以外の項目をアンパックして渡す
session = boto3.Session(**ProfileSettings().dict(exclude_none=True))
