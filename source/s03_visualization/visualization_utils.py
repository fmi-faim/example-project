from tifffile import imread

import numpy as np

import pandas as pd

from ipywidgets import widgets
from IPython.display import display
from faim_ipa.utils import get_git_root
from pathlib import Path
from glob import glob


def select_data():
    exp = widgets.Dropdown(
        options=[
            Path(p).name
            for p in sorted(glob(str(get_git_root() / "processed_data" / "*")))
            if Path(p).is_dir()
        ],
        description="Experiment:",
        disabled=False,
        layout=widgets.Layout(width="400px"),
    )

    img_id = widgets.Dropdown(
        options=[
            Path(p).stem.replace("_labeled", "")
            for p in glob(f"../../processed_data/{exp.value}/s01_segmentation/*.tiff")
        ],
        description="File:",
        disabled=False,
        layout=widgets.Layout(width="400px"),
    )

    def on_exp_change(change):
        img_id.options = [
            Path(p).stem.replace("_labeled", "")
            for p in glob(f"../../processed_data/{exp.value}/s01_segmentation/*.tiff")
        ]

    exp.observe(on_exp_change, names="value")
    centered_layout = widgets.VBox([exp, img_id])
    display(centered_layout)
    return exp, img_id


def load_data(exp_widget, img_widget):
    raw_dirs = [
        Path(p)
        for p in glob(str(get_git_root() / "raw_data" / "**"), recursive=True)
        if Path(p).is_dir()
    ]
    for p in raw_dirs:
        if p.name == exp_widget.value:
            raw_data_dir = p

    raw_img_path = Path(glob(str(raw_data_dir / f"{img_widget.value}.*"))[0])
    seg_path = (
        get_git_root()
        / "processed_data"
        / exp_widget.value
        / "s01_segmentation"
        / f"{img_widget.value}_labeled.tiff"
    )
    measurements_path = (
        get_git_root()
        / "processed_data"
        / exp_widget.value
        / "s02_measurement"
        / f"{img_widget.value}_measurements.csv"
    )

    img = imread(raw_img_path)
    seg = imread(seg_path)
    measurements = pd.read_csv(measurements_path, index_col=False)
    bg_label = pd.DataFrame(
        {"label": [0], "area": [np.nan], "mean_intensity": [np.nan]}
    )
    measurements = pd.concat([bg_label, measurements]).reset_index(drop=True)

    return img, seg, measurements
