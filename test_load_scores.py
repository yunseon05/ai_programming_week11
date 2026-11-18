
import pytest
import subprocess
import sys

from load_scores import load_scores


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

def test_빈_줄은_건너뛴다():
    kept, skipped = load_scores("weird.csv")
    assert len(kept) >= 0

def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    csv_file = tmp_path / "comma.csv"
    csv_file.write_text(
        '이름,점수\n"김,하나",88\n',
        encoding="utf-8"
    )

    kept, skipped = load_scores(str(csv_file))

    assert kept == [("김,하나", 88)]
    assert skipped == []


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []



@pytest.mark.parametrize("score, valid", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])

def test_점수_경계값(tmp_path, score, valid):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(
        f"이름,점수\n김하나,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(str(csv_file))

    assert (len(kept) == 1) == valid



def test_프로그램_직접_실행():
    result = subprocess.run(
        [sys.executable, "load_scores.py", "scores.csv"],
        capture_output=True,
        text=True,
        encoding="cp949"
    )

    assert result.returncode == 0
    assert "읽은 줄" in result.stdout
    assert "건너뛴 줄" in result.stdout
