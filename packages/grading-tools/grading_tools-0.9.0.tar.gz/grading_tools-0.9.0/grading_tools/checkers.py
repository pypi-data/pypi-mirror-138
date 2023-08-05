"""Functions for turning a grader definition into a grader object, and evaluating it."""
from functools import reduce

from grading_tools import graders  # noQA F401,F403
from grading_tools.graders import *  # noQA F401,F403
from grading_tools.loaders import *  # noQA F401,F403


# https://tinyurl.com/ybsguzpm
def _nested_get(dictionary, keys, default=None):
    result = reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys,
        dictionary,
    )
    return result


# https://tinyurl.com/y8vfb3oq
def _nested_set(dictionary, keys, value):
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    dictionary[keys[-1]] = value


def check_submission(defaults, submission):
    """Load grader definition defaults, submission, answer, and executes grading."""
    # Check for grader key
    if "grader" not in defaults:
        raise AttributeError(
            "The definition for this task is missing the `'grader'` key."
        )

    # Check that grader has required keys and values
    for key in ["type", "answer", "method"]:
        if key not in defaults["grader"]:
            raise AttributeError(
                f"defaults['grader'] is missing a '{key}' key."
            )
        if not defaults["grader"].get(key, None):
            raise AttributeError(
                f"There is no value assigned to defaults['grader']['{key}']."
            )

    # Check that grader specified exists
    if not hasattr(graders, defaults["grader"]["type"]):
        raise NameError(f"There is no {defaults['grader']['type']} grader.")

    # Load any files that will be used
    if "loaders" in defaults:
        loaders = defaults["loaders"]
        if not isinstance(loaders, list):
            raise TypeError(
                "The value assigned to defaults['loaders'] must be a list, "
                f"not {type(loaders)}."
            )

        for loader in loaders:
            # Make sure the key-vals are there
            for key in ["file_key", "method"]:
                if key not in loader:
                    raise AttributeError(f"Loaders is missing a '{key}' key.")
                if not loader.get(key, None):
                    raise AttributeError(
                        f"There is no value assigned to the '{key}' key."
                    )

            # Get filename
            fn_keys = loader["file_key"].split("__")
            fn = _nested_get(defaults, fn_keys)
            if not fn:
                raise KeyError(
                    f"There's no filename at defaults.{'.'.join(fn_keys)}."
                )

            # Load object
            load_method = loader["method"]
            kwargs = loader.get("kwargs", {})  # noQA F841
            loaded_obj = eval(f"{load_method}('{fn}', **kwargs)")

            # Assign object to `defaults` dict
            _nested_set(defaults, fn_keys, loaded_obj)

    # Set up args for grader
    grader_dict = {
        "submission": submission,
        "answer": defaults["grader"]["answer"],
    }
    if "points" in defaults["grader"]:
        grader_dict["points"] = defaults["grader"].get("points", 1)

    # Create grader
    g_type = defaults["grader"]["type"]
    g = eval(f"{g_type}(**grader_dict)")

    # Execute grading
    params_dict = defaults["grader"].get("kwargs", {})  # noQA F841
    grade_method = defaults["grader"].get("method")
    eval(f"g.{grade_method}(**params_dict)")

    return g.return_feedback(html=defaults.get("feedback_html", True))
