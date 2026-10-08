import csv
import datetime
import hashlib
import urllib.request
from pathlib import Path

URL = (
    "https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo"
    "/download/verkehrszaehlungen_werte_fussgaenger_velo_alle_jahre.parquet"
)
MANIFEST_COLUMNS = ["url", "date", "size_bytes", "sha256"]


def download(url: str, raw_dir: Path, force: bool = False) -> Path:
    """Fetch url into raw_dir and append a row to raw_dir/manifest.csv.

    Skips the download when the file is already there, unless force is set.
    """
    target = raw_dir / url.rsplit("/", 1)[-1]
    if target.exists() and not force:
        print(f"download: skipped, {target} already exists")
        return target

    raw_dir.mkdir(parents=True, exist_ok=True)
    # Write to a .part file first so an interrupted download never looks complete.
    part = target.with_name(target.name + ".part")
    sha256 = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(url) as response, part.open("wb") as out:
        while chunk := response.read(1 << 20):
            out.write(chunk)
            sha256.update(chunk)
            size += len(chunk)
    part.replace(target)

    manifest = raw_dir / "manifest.csv"
    is_new = not manifest.exists()
    with manifest.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(MANIFEST_COLUMNS)
        writer.writerow([url, datetime.date.today().isoformat(), size, sha256.hexdigest()])

    print(f"download: wrote {target} ({size} bytes, sha256 {sha256.hexdigest()[:12]}…)")
    return target
