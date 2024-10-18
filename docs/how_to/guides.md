# How-to Guides
This section is dedicated to experienced users. If you are new to this project, please take a look at the [tutorial](../tutorial/run_processing_steps.md) section first.

!!! important
    All commands are run from within the project root directory.

## Documentation
### Build Documentation
An offline version of the documentation can be built with the following command:
```bash
pixi run build_docs
```

### Serve Documentation
A mkdocs server can be started to serve the documentation website. This is useful if you are actively working on the documentation and want to see live changes. Use the following command:
```bash
pixi run show_docs
```

## Data Processing
### Build Config
Build the `acquisition_config.yaml` file and store it in the working directory `WD`:
```bash
WD=runs/dataset-name pixi run build_config
```

Replace `dataset-name` with the name of the dataset you would like to process.

### Run Segment
Run the segmentation step, with the `acquisition_config.yaml` stored in `WD`, manually:
```bash
WD=runs/dataset-name pixi run segment
```

### Run Measure
Run the measure step, with the `measure_config.yaml` stored in `WD`, manually:
```bash
WD=runs/dataset-name pixi run measure
```

### Visualize Results
Run jupyter lab with the visualization jupyter notebook inside `WD`:
```bash
WD=runs/dataset-name pixi run visualize
```

### Run Workflow
Instead of calling the processing steps manually, you can call the nextflow workflow with:
```bash
WD=runs/dataset-name pixi run nextflow
```

## Development
### Jupyter Lab
Run jupyter lab to develop new notebooks:
```bash
pixi run jupyter
```

### Napari
Run napari to visualize data:
```bash
pixi run napari
```

### Lint
Clean up code formatting:
```bash
pixi run lint
```
