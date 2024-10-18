# Working with the Template
This section of the tutorial guides you through the development steps of an image processing and analysis project using the [IPA Project Template](https://fmi-faim.github.io/ipa-project-template/). We will start by copying the template to a new project directory and then build up this example-project step-by-step. The point of this tutorial is to show you how to work with the template and specifically how to separate workflow development from applying the workflow to data.

!!! attention Prerequisites
    Follow the [installation instructions](https://fmi-faim.github.io/ipa-project-template/) for pixi and copier before your continue here.

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

!!! success
    Congratulations! You have created your first project from the [IPA Project Template](https://fmi-faim.github.io/ipa-project-template/)!

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

## Convert Routine to Reproducible Processing Steps
Code moves to `source`.

## Run Processing Steps

## Bundle Processing Steps into a Workflow

## Add Visualization Notebook

## Finalize Documentation
