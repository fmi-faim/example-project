# References

## Acquisition Config
The acquisition config must be generated by the user by running the [build_config]() task, which will write the `acquisition_config.yaml` file.

__Content__

__`raw_data_dir`__

:    The path to the raw data directory containing the acquired microscopy images. The path in the yaml file is relative to the project root directory.

__`suffix`__

:    Suffix of the raw data files e.g. `.tif`.

__`output_dir`__

:    The path to the directory where the processed outputs are stored. The processing will create a new output directory in this location, with the name of the selected raw data directory. Within this output directory, each processing step will create a dedicated output directory to write intermediate results.

## Measure Config
The `measure_config.yaml` file is created by the `s01_segment` processing step.

__`raw_data_dir`__

:    This entry is copied from the acquisition config.

__`suffix`__

:    Suffix of the raw data files, copied from the acquisition config.

__`segmentation_dir`__

:    Path to the directory where the segmentation masks generated by `s01_segmet` are stored.

__`output_dir`__

:    Path to the output directory, copied from the acquisition config.

## Measurement Outputs
The `s02_measure` step collects all paths to the written measurement csv files and writes them into the `measure_outputs.yaml` file.
