"""
Pinned external data used for mapping between AMR databases
(see DatabaseMapping.py).  These files are downloaded into
hAMRonization/data/ when the package is built/installed (see setup.py).

This module must only use the standard library as it is also run by setup.py.
To update a source, change its ref and update the sha256 checksums.
"""

import os
import hashlib
import urllib.request

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# set to skip the download at install time (e.g. offline builds)
SKIP_DOWNLOAD_ENV = "HAMRONIZATION_SKIP_DATA_DOWNLOAD"

CHAMREDB_REF = "7acabd38fb87497e250be99e830074775060f6c3"  # graph 2026-11-09
CHAMREDB_VERSION = "chamredb graph 2026-11-09"
ARGNORM_REF = "v1.1.0"
ARGNORM_VERSION = f"argnorm {ARGNORM_REF.lstrip('v')}"

_CHAMREDB_URL = f"https://raw.githubusercontent.com/antunderwood/chamredb/{CHAMREDB_REF}/chamredb/data"
_ARGNORM_URL = f"https://raw.githubusercontent.com/BigDataBiology/argNorm/{ARGNORM_REF}/argnorm/data"

CHAMREDB_GRAPH = "chamredb/graph.json"
ARGNORM_DIR = "argnorm"

# path relative to DATA_DIR -> (url, sha256)
DATA_FILES = {
    CHAMREDB_GRAPH: (
        f"{_CHAMREDB_URL}/graph.json",
        "1c7f0f080de1faf854ba5e6247c3bf2a9fced864b17670e87fd0efb0fc32b74e",
    ),
    f"{ARGNORM_DIR}/ncbi_ARO_mapping.tsv": (
        f"{_ARGNORM_URL}/ncbi_ARO_mapping.tsv",
        "c0b6cc60d72c411e0c34ec4341606f8d182bab5dad163aa8fc3220d1ee075538",
    ),
    f"{ARGNORM_DIR}/resfinder_ARO_mapping.tsv": (
        f"{_ARGNORM_URL}/resfinder_ARO_mapping.tsv",
        "7aeeb43e1b6eebff9c24598a4705c52493759f3ed12672b33caedb58170577c9",
    ),
    f"{ARGNORM_DIR}/manual_curation/ncbi_curation.tsv": (
        f"{_ARGNORM_URL}/manual_curation/ncbi_curation.tsv",
        "6462255d9be54c75753800376ef68c4fc911bafa0a4fbd987708ede465e7c20a",
    ),
    f"{ARGNORM_DIR}/manual_curation/resfinder_curation.tsv": (
        f"{_ARGNORM_URL}/manual_curation/resfinder_curation.tsv",
        "741c0aaa927b4ce314ffcf963a254f02f60713bfaf74699e22aaaf7c98c1b95a",
    ),
}


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_data(data_dir=DATA_DIR, files=None, log=print):
    """
    Download the pinned data files into data_dir, verifying checksums.
    Files already present with the right checksum are not downloaded again.
    Raises RuntimeError if a download fails or a checksum does not match.
    """
    files = DATA_FILES if files is None else files
    for rel_path, (url, sha256) in files.items():
        dest = os.path.join(data_dir, rel_path)
        if os.path.exists(dest) and _sha256(dest) == sha256:
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        log(f"hAMRonization: downloading {url}")
        tmp = dest + ".part"
        try:
            with urllib.request.urlopen(url, timeout=120) as response, open(tmp, "wb") as out:
                while chunk := response.read(1 << 20):
                    out.write(chunk)
            if _sha256(tmp) != sha256:
                raise RuntimeError(f"checksum mismatch for {url}")
            os.replace(tmp, dest)
        except Exception as e:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise RuntimeError(
                f"Failed to download {url}: {e}. Set {SKIP_DOWNLOAD_ENV}=1 to "
                "install without the database mapping data."
            ) from e
