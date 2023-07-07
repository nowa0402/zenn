import tempfile
from pathlib import Path
from typing import Any, Generator

import pytest
from pydantic import ValidationError

from csv_read import CSVReader


@pytest.fixture(scope="function")
def json_file() -> Generator[Path, Any, None]:
    """json一時ファイル作成

    Yields:
        Generator[Path, Any, None]: json一時ファイルパス
    """
    path = Path(tempfile.NamedTemporaryFile(suffix=".json", delete=False).name)
    yield path
    # テスト終了後にファイルを削除
    path.unlink()


@pytest.fixture(scope="function")
def csv_file() -> Generator[Path, Any, None]:
    """csv一時ファイル作成

    Yields:
        Generator[Path, Any, None]: csv一時ファイルパス
    """
    path = Path(tempfile.NamedTemporaryFile(suffix=".csv", delete=False).name)
    yield path
    # テスト終了後にファイルを削除
    path.unlink()


def test_not_exists_path() -> None:
    """バリデーションチェックエラー
    ファイルが存在しない
    """
    path = Path(tempfile.NamedTemporaryFile(suffix=".csv", delete=True).name)
    with pytest.raises(ValidationError) as e:
        _ = CSVReader(path=path)

    msg = e.value.errors()[0]["msg"]
    assert msg == f"ファイルが存在しません:{path}"


def test_not_suffix_csv(json_file: Path) -> None:
    """バリデーションエラー
    拡張子不正

    Args:
        json_file (Path): json一時ファイルパス
    """
    with pytest.raises(ValidationError) as e:
        _ = CSVReader(path=json_file)

    msg = e.value.errors()[0]["msg"]
    assert msg == f"拡張子に誤りがあります:{json_file.name}"


def test_validate_ok(csv_file: Path) -> None:
    """バリデーションチェック通過

    Args:
        csv_file (Path): csv一時ファイルパス
    """
    reader = CSVReader(path=csv_file)
    assert reader.path == csv_file
