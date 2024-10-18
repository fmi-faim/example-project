import argparse
from os import scandir
from pathlib import Path

import pandas as pd
import yaml
from faim_ipa.utils import get_git_root, create_logger
import sys
from rich.pretty import pretty_repr
from skimage import measure
from tifffile import imread

sys.path.append(str(get_git_root()))
from source.s02_measure.config import MeasureConfig


def main(config: MeasureConfig):
    logger = create_logger("measurement")
    logger.info(pretty_repr(config))

    output_dir = config.output_dir / "s02_measurement"
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = []
    for item in scandir(config.raw_data_dir):
        logger.info(f"Processing item: {item.name}")
        if item.name.endswith(config.suffix):
            name = item.name.split(config.suffix)[0]
            image = imread(item.path)
            labeled_image = imread(config.segmentation_dir / f"{name}_labeled.tiff")

            properties = measure.regionprops_table(
                labeled_image,
                intensity_image=image,
                properties=["label", "area", "mean_intensity"],
            )

            properties_df = pd.DataFrame(properties)

            measure_file_name = output_dir / f"{name}_measurements.csv"
            properties_df.to_csv(measure_file_name, index=False)
            outputs.append(str(measure_file_name))

    with open("measure_outputs.yaml", "w") as f:
        yaml.dump(outputs, f, indent=4, sort_keys=False)

    logger.info("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()

    config = MeasureConfig.load(args.config)
    main(config)
