import json
import subprocess
import sys


def test_cli(tmp_path):  # tmp_path - создать временный файл для тестов
    input_file = tmp_path / "input.csv"
    input_file.write_text(
        "timestamp,level,source,message\n2026-10-06T10:00:00+00:00,ERROR,api,Ошибка прямо тут",
        encoding="utf-8",
    )
    output_file = tmp_path / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(input_file),
            "--format",
            "csv",
            "--output",
            str(output_file),
        ],
        check=False,  # код не упадет при ошибке
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["total"] == 1
        assert data["levels"]["ERROR"] == 1
