import argparse
from os import scandir
from pathlib import Path

from faim_ipa.utils import get_git_root, create_logger
import sys

from rich.pretty import pretty_repr
from tifffile import imread, imwrite
import pandas as pd

from skimage import filters, measure, morphology, segmentation

sys.path.append(str(get_git_root()))

from source.s01_segment_and_measure.config import AcquisitionConfig


def main(config: AcquisitionConfig):
    logger = create_logger("image-analysis")
    logger.info(pretty_repr(config))

    config.output_dir.mkdir(parents=True, exist_ok=True)

    suffix = ".TIF"
    for item in scandir(config.raw_data_dir):
        logger.info(f"Processing item: {item.name}")
        if item.name.endswith(suffix):
            name = item.name.split(suffix)[0]
            image = imread(item.path)

            # Step 1: Apply Otsu's thresholding
            threshold_value = filters.threshold_otsu(image)
            binary_image = image > threshold_value

            # Step 2: Remove small objects/noise if necessary
            binary_image_cleaned = morphology.remove_small_objects(
                binary_image, min_size=64
            )
            # Step 3: Fill holes within the binary mask
            binary_image_filled = morphology.remove_small_holes(
                binary_image_cleaned, area_threshold=64
            )

            # Step 4: Label the connected components (nuclei)
            labeled_image = segmentation.clear_border(
                measure.label(binary_image_filled)
            )

            imwrite(config.output_dir / f"{name}_labeled.tiff", labeled_image)

            properties = measure.regionprops_table(
                labeled_image,
                intensity_image=image,
                properties=["label", "area", "mean_intensity"],
            )

            # Convert to pandas DataFrame for easy export
            properties_df = pd.DataFrame(properties)

            properties_df.to_csv(
                config.output_dir / f"{name}_measurements.csv", index=False
            )

    logger.info("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()

    config = AcquisitionConfig.load(args.config)
    main(config)
