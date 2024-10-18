import argparse
from os import scandir
from pathlib import Path

from faim_ipa.utils import get_git_root, create_logger
import sys

from rich.pretty import pretty_repr
from skimage.measure import label
from tifffile import imread, imwrite

from skimage import filters, measure, morphology, segmentation


sys.path.append(str(get_git_root()))

from source.s01_segment.config import AcquisitionConfig
from source.s02_measure.config import MeasureConfig


def main(config: AcquisitionConfig):
    logger = create_logger("segmentation")
    logger.info(pretty_repr(config))

    output_dir = config.output_dir / config.raw_data_dir.name / "s01_segmentation"
    output_dir.mkdir(parents=True, exist_ok=True)

    for item in scandir(config.raw_data_dir):
        logger.info(f"Processing item: {item.name}")
        if item.name.endswith(config.suffix):
            name = item.name.split(config.suffix)[0]
            image = imread(item.path)

            threshold_value = filters.threshold_otsu(image)
            binary_image = image > threshold_value

            binary_image_cleaned = morphology.remove_small_objects(
                binary_image, min_size=64
            )

            binary_image_filled = morphology.remove_small_holes(
                binary_image_cleaned, area_threshold=64
            )

            labeled_image = label(
                segmentation.clear_border(measure.label(binary_image_filled))
            )

            seg_file_name = output_dir / f"{name}_labeled.tiff"
            imwrite(seg_file_name, labeled_image)

    measure_config = MeasureConfig(
        raw_data_dir=config.raw_data_dir,
        suffix=config.suffix,
        segmentation_dir=output_dir,
        output_dir=output_dir.parent,
    )
    measure_config.save()

    logger.info("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()

    config = AcquisitionConfig.load(args.config)
    main(config)
