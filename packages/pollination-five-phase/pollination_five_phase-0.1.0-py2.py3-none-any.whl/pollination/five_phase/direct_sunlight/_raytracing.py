"""Raytracing DAG for two phase studies."""

from pollination_dsl.dag import Inputs, DAG, task
from dataclasses import dataclass

from pollination.honeybee_radiance.contrib import DaylightContribution


@dataclass
class DirectSunlightRayTracing(DAG):

    radiance_parameters = Inputs.str(
        description='The radiance parameters for ray tracing',
        default='-ab 2 -ad 5000 -lw 2e-05'
    )

    octree = Inputs.file(
        description='A Radiance octree file with suns.',
        extensions=['oct']
    )

    grid_name = Inputs.str(
        description='Sensor grid file name. This is useful to rename the final result '
        'file to {grid_name}.ill'
    )

    sensor_grid = Inputs.file(
        description='Sensor grid file.',
        extensions=['pts']
    )

    sensor_count = Inputs.int(
        description='Number of sensors in the input sensor grid.'
    )

    sun_modifiers = Inputs.file(
        description='A file with sun modifiers.'
    )

    bsdfs = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        optional=True
    )

    @task(template=DaylightContribution)
    def direct_sunlight(
        self,
        name=grid_name,
        radiance_parameters=radiance_parameters,
        fixed_radiance_parameters='-aa 0.0 -I -ab 0 -dc 1.0 -dt 0.0 -dj 0.0 -dr 0',
        sensor_count=sensor_count,
        modifiers=sun_modifiers,
        sensor_grid=sensor_grid,
        output_format='a',  # make it ascii so we expose the file as a separate output
        scene_file=octree,
        bsdf_folder=bsdfs
    ):
        return [
            {
                'from': DaylightContribution()._outputs.result_file,
                'to': '../direct/{{self.name}}.ill'
            }
        ]
