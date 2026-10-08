import csv
import datetime
import hashlib

from ds_projekt_2026_tutorial.download import download

# A file:// URL lets urllib read from disk, so the test needs no network.


def read_manifest(raw_dir):
    with (raw_dir / "manifest.csv").open(newline="") as f:
        return list(csv.reader(f))


def test_download_writes_skips_and_forces(tmp_path, capsys):
    content = b"not really parquet\n" * 1000
    source = tmp_path / "source" / "counts.parquet"
    source.parent.mkdir()
    source.write_bytes(content)
    url = source.as_uri()
    raw_dir = tmp_path / "data" / "raw"

    target = download(url, raw_dir)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "wrote" in out[0]
    assert target == raw_dir / "counts.parquet"
    assert target.read_bytes() == content
    assert not (raw_dir / "counts.parquet.part").exists()
    assert read_manifest(raw_dir) == [
        ["url", "date", "size_bytes", "sha256"],
        [url, datetime.date.today().isoformat(), str(len(content)), hashlib.sha256(content).hexdigest()],
    ]

    download(url, raw_dir)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "skipped" in out[0]
    assert len(read_manifest(raw_dir)) == 2

    download(url, raw_dir, force=True)
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and "wrote" in out[0]
    assert len(read_manifest(raw_dir)) == 3
