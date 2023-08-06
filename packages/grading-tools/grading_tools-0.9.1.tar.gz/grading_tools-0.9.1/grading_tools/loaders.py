"""Functions to help load fixtures."""

import os
import traceback
from pathlib import Path

import pandas as pd
from joblib import load
from PIL import Image


def _get_fixture_path(fixture):
    """Given the name of a fixture file, returns path to `../fixtures/fixture`."""
    stack = traceback.extract_stack()
    # Name of file where function was called
    filename = stack[-2].filename
    # Get path to dir two levels up
    my_dir = str(Path(filename).parents[1].resolve())
    # Create absolute path to fixture file
    fixture_path = os.path.join(my_dir, "fixtures", fixture)
    return fixture_path


def load_csv(
    filepath, fixture_path=True, index_tz=None, inferred_freq=False, **kwargs
):
    """Load CSV file into DataFrame.

    Wrapper function for ``pandas.read_csv()``.

    Parameters
    ----------
    filepath: str
        Location of the file

    fixture_path: bool, default=True
        Whether or not to prepend ``../fixtures/`` to filepath. In production, should
        always be ``True``. In development and testing, should be ``False``.

    index_tz: str, default=None
        Localize the index of the DataFrame or Series to timezone given. Note that
        you'll need to include the ``parse_datetime`` and ``index_col`` arguments.

    inferred_freq: bool, default=False
        Infer the frequency of the DataFrame or Series index. This is necessary for
        some time series models. Note that you'll need to include the ``parse_datetime``
         and ``index_col`` arguments.

    **kwargs:
        Additional arguments you want to pass to ``pandas.read_csv()``.

    """
    if fixture_path:
        filepath = _get_fixture_path(filepath)
    df = pd.read_csv(filepath, **kwargs)
    try:
        if inferred_freq:
            df.index.freq = df.index.inferred_freq
        if index_tz:
            df.index.tz_convert(index_tz)
    except AttributeError:
        raise AttributeError(
            "In order to perform frequency and timezone alterations on DataFrame "
            "index, the index must be parsed as datetime. Include the `parse_dates` "
            "and `index_col` arguments."
        )
    return df


def load_sklearn(filepath, fixture_path=True, **kwargs):
    """Load pickled model.

    Wrapper function for ``joblib.load()``. Works with any pickled file.

    Parameters
    ----------
    filepath: str
        Location of the file

    fixture_path: bool, default=True
        Whether or not to prepend ``../fixtures/`` to filepath. In production, should
        always be ``True``. In development and testing, should be ``False``.

    **kwargs:
        Additional arguments you want to pass to ``joblib.load()``.

    """
    if fixture_path:
        filepath = _get_fixture_path(filepath)
    model = load(filepath, **kwargs)
    return model


def load_image(filepath, fixture_path=True, **kwargs) -> Image:
    """Load image file.

    Wrapper function for ``PIL.Image.open()``.

    Parameters
    ----------
    filepath: str
        Location of the file

    fixture_path: bool, default=True
        Whether or not to prepend ``../fixtures/`` to filepath. In production, should
        always be ``True``. In development and testing, should be ``False``.

    **kwargs:
        Additional arguments you want to pass to ``PIL.Image.open()``.

    """
    if fixture_path:
        filepath = _get_fixture_path(filepath)
    img = Image.open(filepath, **kwargs)
    return img
