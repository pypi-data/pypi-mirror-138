from importlib import import_module, reload
from typing import Tuple

import matplotlib.patches as mpatches


def load_style(style: str) -> Tuple[dict, dict, dict]:

    try:
        style_module = reload(import_module(f"pltflow.styles.{style}")).style  # type: ignore

    except ModuleNotFoundError as no_module_with_that_name:
        raise ModuleNotFoundError(f"Style {style} not found") from no_module_with_that_name

    return style_module["rcParams"], style_module["styleParams"], style_module["colors"]


def create_legend_patches(colors: dict, grayed_color: str = "") -> list:
    """
    This function creates a legend for the chart.
    """

    patches = [mpatches.Patch(color=colors[key], label=key) for key in colors if colors[key] != grayed_color]

    return patches
