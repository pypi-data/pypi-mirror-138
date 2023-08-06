"""Fetch and check aux file for modes-l.

Path('link-to-textfile.txt').symlink_to(Path('textfile.txt'))

fp_ = hf_hub_download(repo, filename)
Path(local_filepath).symlink_to(fp_)

assert hashlib.sha256(Path(local_filepath).read_bytes()).hexdigest() == sha256checksum

colab:

model_name = "model-l"
_ = cached_download(hf_hub_url("mikeee/model_s", model_name))

url = hf_hub_url("mikeee/model_s", model_name)
print(url)
_ = cached_download(url)
print(_)
clas = joblib.load(_)

# %time clas('test', ['test', 'test more', 'no test', 'on test', '测试', '测试测试', 'test测试', 'this', 'that test'], multi_lable=1)
"""
# pylint: disable=invalid-name, wrong-import-position, wrong-import-order

from install import install

_ = [
    *map(
        install, ["huggingface_hub", "alive-progress", "sentencepiece", "transformers"]
    )
]

from pathlib import Path
import hashlib
from logzero import logger

# import joblib

# from huggingface_hub import hf_hub_url, cached_download
from huggingface_hub import hf_hub_download


def fetch_check_aux(default="~"):
    """Fetch and check aux file for modes-l."""
    filename = "d23ec1d4898d7173d13994fbd662fa3243bf8a23744748d21115317316bd5e1b.a89eb3c0add0e1b04b46be11a1bc1a65b92fdae1bbb04124701ff2e6acfccc75"
    repo = "mikeee/model_s"
    local_dir = Path(f"{default}/.cache/huggingface/transformers").expanduser()
    local_dir.mkdir(parents=True, exist_ok=True)
    local_filepath = local_dir / filename

    sha256checksum = "13c8d666d62a7bc4ac8f040aab68e942c861f93303156cc28f5c7e885d86d6e3"

    if local_filepath.exists():
        if hashlib.sha256(local_filepath.read_bytes()).hexdigest() == sha256checksum:
            return True

    fp_ = hf_hub_download(repo, filename)
    local_filepath.symlink_to(fp_)

    try:
        _ = hashlib.sha256(local_filepath.read_bytes()).hexdigest()
        assert _ == sha256checksum
        return True
    except Exception as exc:
        logger.error(exc)
        raise
