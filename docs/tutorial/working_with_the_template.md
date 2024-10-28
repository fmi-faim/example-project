# Working with the Template
This section of the tutorial guides you through the development steps of an image processing and analysis project using the [IPA Project Template](https://fmi-faim.github.io/ipa-project-template/). We will start by copying the template to a new project directory and then build up this example-project step-by-step. The point of this tutorial is to show you how to work with the template and specifically how to separate workflow development from applying the workflow to data.

!!! attention Prerequisites
    Follow the [installation instructions](https://fmi-faim.github.io/ipa-project-template/) for pixi and copier before your continue here.

!!! info "Issues & Feedback"
    In case you encounter any issues or have questions regarding our project template, please open an [issue](https://github.com/fmi-faim/example-project/issues).

## Copy the Template
First we need to create an instance of the template by running the copier command:

```bash
pixi x copier copy git+https://github.com/fmi-faim/ipa-project-template example-project
```

You will be asked a series of questions:

* What is your first and last name?</br>
    Your first and last name will be put into the pixi.toml file as author.
* What is your email address?</br>
    Your email address will be put into the pixi.toml file.
* What is your project name?</br>
    Answer `Example Project`.
* What is your organization name?</br>
    This information will be put into the pixi.toml file.
* Do you want to include the most common Python packages?</br>
    Answer `y`.
* Do you want to include Napari in your project?</br>
    Answer `y`.
* Do you want to include Nextflow in your project?</br>
    Answer `n`. We will add nextflow later.
* Do you want to add installation and initialization scripts for Unix systems?
    Answer `n`.
* Do you want to add a config and run demo?
    Answer `n`.

Next, we need to git initialize the project and enable versioning:
```bash
git init
git add .
git commit -m "Initial commit."
git branch -M main
```

Now, you can build the documentation page with:
```bash
pixi run build_docs
```

The very last setup step is to get some raw data. Please follow the instructions in [data](../data.md).

!!! success "Congratulations!"
    You have created your first project from the [IPA Project Template](https://fmi-faim.github.io/ipa-project-template/)!

## Develop Image Processing and Analysis Routine
Now it is time to prototype the image processing and analysis routine. The most interactive way to do this is with jupyter lab. You can start jupyter lab with the following command:

```bash
pixi run jupyter
```

This will open jupyter lab in your browser, and you should navigate to the sandbox. The sandbox is our prototyping place. Any results created by code in the sandbox are not expected to be reproducible. The reasoning behind this is, that we first want to explore what might work, before we focus on reproducible results.

We want to develop a workflow which

* segments the nuclei,
* measures mean intensity of each nucleus, and saves the result to csv.

Feel free to develop your own workflow or get inspired by [our jupyter notebook](https://github.com/fmi-faim/example-project/blob/85e6c52a8dd4f6349e11c9588f570a6f8cebd805/sandbox/Prototype-Image-Analysis.ipynb).

!!! tip "Commit your changes"
    Now would be a good time to [lint](https://en.wikipedia.org/wiki/Lint_(software)) your code and
    commit your changes into the git repository.
    ```
    pixi run lint
    git add .
    git commit -m "First draft"
    ```
    [Here](https://focalplane.biologists.com/2021/09/04/collaborative-bio-image-analysis-script-editing-with-git/) is a nice git tutorial you might want to look at to get started.


## Convert Routine to Reproducible Processing Steps
When you are done developing your image processing and analysis routine, it is time to convert it to a Python script. The Python script must be written, such that we can call it with a config file and apply it to an arbitrary raw data directory. We want to split up the processing routine into multiple sub-steps, where each step saves intermediate processing results to `processed_data`.

Converting a jupyter notebook into a series of standalone processing steps is an important step to make our research code reproducible. At this point in time we want to think carefully about how to split our jupyter notebook into a series of individual processing scripts. For this example-project we suggest to split the processing in two steps:

1. segment
2. measure

!!! info
    One could keep everything in a single big processing step. However, by splitting the code into sub-steps, we can recover from intermediate results in case a processing step fails.


To get started you can run the copier command again:

!!! danger
    Make sure you are in the parent directory of the `example-project` when you call the copier command.

```bash
pixi x copier copy git+https://github.com/fmi-faim/ipa-project-template example-project
```

This time answer `y` to the `Do you want to add a config and run demo?` question. This will add the following to your template:

```text
source
└── s01_demo
  ├── __init__.py
  ├── config.py
  └── run.tif
```

### Implement s01_segment
Rename `s01_demo` to `s01_segment` and then we want to think about the parameters we want to expose to the user. In our workflow we want to configure three parameters:

* `raw_data_dir`: The directory where the raw tiff files are stored.
* `suffix`: Suffix of the tiff files. Sometimes it is `.TIF` and sometimes it is `.tif`.
* `output_dir`: Where to store the segmentation masks.

Edit the `config.py` to match [our implementation](https://github.com/fmi-faim/example-project/blob/21b4b97141074c105b0852681609980f6768e9db/source/s01_segment/config.py).

We added a `prompt()` function to the `AcquisitionConfig`, which we can use to ask the user for input. Now we only need to add a pixi-task which will call the script. We do this by adding [this line](https://github.com/fmi-faim/example-project/blob/21b4b97141074c105b0852681609980f6768e9db/pixi.toml#L16) to our `pixi.toml` file.

!!! note "Uncommitted changes"
    If you make your pixi task depend on the `source_status` task that comes with the template,
    you can ensure that it warns you if there are any uncommitted changes, thereby ensuring
    that you always commit any changes and run on a clean, reproducible state of your repository.


Now that we can create config files, we will add the processing code to `run.py`. Edit the file until it matches [our implementation](https://github.com/fmi-faim/example-project/blob/21b4b97141074c105b0852681609980f6768e9db/source/s01_segment/run.py).

!!! note
    This script will not work at the moment, because we are using the `MeasureConfig` in [this line](https://github.com/fmi-faim/example-project/blob/21b4b97141074c105b0852681609980f6768e9db/source/s01_segment/run.py#L52). However, this file does not exist yet.

### Implement s02_segment
Create a new directory in `source` called `s02_measure` and add all the files from [our reference implementation](https://github.com/fmi-faim/example-project/tree/21b4b97141074c105b0852681609980f6768e9db/source/s02_measure).

Finally, we want to add the pixi-tasks to run the two processing steps. Edit your `pixi.toml` file and add [these two lines](https://github.com/fmi-faim/example-project/blob/21b4b97141074c105b0852681609980f6768e9db/pixi.toml#L17-L18).

!!! success "Congratulations!"
    You have converted your jupyter notebook to reproducible processing steps! To run them, follow the [step-by-step tutorial](run_processing_steps.md)

!!! tip "Commit your changes"
    Don't forget to commit your changes into the git repository.


## Bundle Processing Steps into a Workflow
So far, you can run your processing steps one-by-one. However, we can automate this and especially for larger projects it makes sense to explore workflow orchestrators, which take care of running one step after another. Furthermore, such workflow orchestrators can recover processing in case of failure or scale up processing to run in parallel on high performance computing or in the cloud. In our case we will use [nextflow](https://nextflow.io/). Unfortunately, nextflow is not available on Windows.

To get started you can run the copier command again:

!!! danger
    Make sure you are in the parent directory of the `example-project` when you call the copier command.

```bash
pixi x copier copy git+https://github.com/fmi-faim/ipa-project-template example-project
```

This time answer `y` to the `Do you want to include Nextflow in your project?` question.

This will add `nextflow.config` and `workflow.nf` to the `source` directory. Edit these files until they match [our reference implementation](https://github.com/fmi-faim/example-project/tree/706c41537895324ebef57a4086eeedee2d5a1039/source) and verify that the `pixi.toml` file matches [our `pixi.toml` file](https://github.com/fmi-faim/example-project/blob/706c41537895324ebef57a4086eeedee2d5a1039/pixi.toml).

!!! success "Congratulations!"
    You have added a nextflow workflow to your example-project! To run it, follow the [workflow tutorial](run_workflow.md)

## Add Visualization Notebook
It is good practice to provide some form of visualization of your processing results. We do this by adding a 3rd step `s03_visualization` to our `source` directory. In this directory we have the [`visualization_utils.py`](https://github.com/fmi-faim/example-project/blob/47f389e18a2850417cef607fa4a9803396fb0f90/source/s03_visualization/visualization_utils.py) file and the [`Visualize_Results.ipynb`](https://github.com/fmi-faim/example-project/blob/47f389e18a2850417cef607fa4a9803396fb0f90/source/s03_visualization/Visualize_Results.ipynb) notebook. You can copy these files from our reference implementation. Additionally, you need to add [these two](https://github.com/fmi-faim/example-project/blob/47f389e18a2850417cef607fa4a9803396fb0f90/pixi.toml#L65-L66) lines to your `pixi.toml`. Now you are ready to run the visualization as described [here](run_processing_steps.md#visualize-results).

## Finalize Documentation
Finally, we want to create all the necessary documentation for this project. Run the following command to get a live view of the website:
```bash
pixi run show_docs
```

Now you can edit the markdown files in `docs` and the website will be rendered fresh if any change is detected.

!!! success "Congratulations!"
    You finished the IPA Project Template tutorial!<br/>
    Don't forget to always commit your changes.
