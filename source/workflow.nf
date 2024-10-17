
params.config = "config.yaml"

process SEGMENT {
    label 'cpu'

    input:
    path config

    output:
    path "measure_config.yaml"

    script:
    """
    pixi run --no-lockfile-update python $baseDir/s01_segment/run.py --config $config
    """
}

process MEASURE {
    label 'cpu'

    input:
    path config

    output:
    path "measure_outputs.yaml"

    script:
    """
    pixi run --no-lockfile-update python $baseDir/s02_measure/run.py --config $config
    """
}

workflow {
    measure_config = SEGMENT(params.config)
    measurements = MEASURE(measure_config)
}
