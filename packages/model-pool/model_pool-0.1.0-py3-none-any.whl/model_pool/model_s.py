"""Load model_s."""
# pylint: disable=invalid-name, wrong-import-position, wrong-import-order, duplicate-code

from install import install

_ = [
    *map(
        install,
        ["sentence-transformers", "huggingface-hub", "alive-progress", "logzero"],
    )
]

from pathlib import Path

from alive_progress import alive_bar
from huggingface_hub import hf_hub_url, cached_download  # hf_hub_download,
import joblib
from logzero import logger


def load_model_s(alive_bar_on=True):
    """Load local model_s if present, else fetch from hf.co."""
    file_loc = "radiobee/model_s"
    if Path(file_loc).exists():
        # raise Exception(f"File {file_loc} does not exist.")

        if alive_bar_on:
            with alive_bar(
                1, title=" Loading model_s, takes ~30 secs ...", length=3
            ) as progress_bar:
                model = joblib.load(file_loc)

                # model_s = pickle.load(open(file_loc, "rb"))
                progress_bar()  # pylint: disable=not-callable
        else:
            logger.info("Loading local model, it may take a while")
            model = joblib.load(file_loc)

        return model

    logger.info(
        "Fetching and caching model_s from huggingface.co... "
        "The first time may take a while depending on your net."
    )
    if alive_bar_on:
        with alive_bar(
            1, title=" Subsequent loading takes ~20 secs ...", length=3
        ) as progress_bar:
            model = joblib.load(
                cached_download(hf_hub_url("mikeee/model_s", "model_s"))
            )
            progress_bar()  # pylint: disable=not-callable
    else:
        logger.info("Loading model from hf-hub, it may take a while")
        model = joblib.load(cached_download(hf_hub_url("mikeee/model_s", "model_s")))
    return model


# model_s = load_model_s()
