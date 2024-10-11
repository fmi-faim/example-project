from pathlib import Path

import questionary
from faim_ipa.utils import IPAConfig, get_git_root


class AcquisitionConfig(IPAConfig):
    raw_data_dir: Path = get_git_root() / "raw_data"
    suffix: str = ".TIF"
    output_dir: Path = get_git_root() / "processed_data"

    def config_name(self) -> str:
        return "acquisition_config.yaml"

    def prompt(self):
        self.raw_data_dir = Path(
            questionary.path(
                "Select the raw_data dir:",
                default=str(get_git_root() / "raw_data"),
            ).ask()
        )
        self.suffix = questionary.text(
            "Enter the suffix of the files to process:", default=".TIF"
        ).ask()
        self.output_dir = Path(
            questionary.path(
                "Select the output dir:",
                default=str(get_git_root() / "processed_data"),
            ).ask()
        )

        self.save()


if __name__ == "__main__":
    config = AcquisitionConfig()
    config.prompt()
