from pathlib import Path

from faim_ipa.utils import IPAConfig, get_git_root


class MeasureConfig(IPAConfig):
    raw_data_dir: Path = get_git_root() / "raw_data"
    suffix: str = "TIF"
    segmentation_dir: Path = get_git_root() / "processed_data"
    output_dir: Path = get_git_root() / "processed_data"

    def config_name(self) -> str:
        return "measure_config.yaml"
