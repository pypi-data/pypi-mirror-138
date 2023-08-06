from pollination_dsl.dag import Inputs, DAG, task
from pollination_dsl.dag.inputs import ItemType
from dataclasses import dataclass
from pollination.honeybee_radiance.grid import MergeFolderData

from ._raytracing import DirectSunlightRayTracing


@dataclass
class DirectSunlightEntryPoint(DAG):
    """Direct sunlight simulation entry point.

    This is the fifth phase step in a five phase recipe.
    """

    # inputs
    identifier = Inputs.str(
        description='Identifier for this two-phase study. This value is usually the '
        'identifier of the aperture group or is set to __static__ for the static '
        'apertures in the model.', default='__static__'
    )

    radiance_parameters = Inputs.str(
        description='The radiance parameters for ray tracing.',
        default='-ab 0 -ad 5000 -lw 2e-05'
    )

    sensor_grids_info = Inputs.list(
        description='A list with sensor grids information.',
        items_type=ItemType.JSONObject
    )

    sensor_grids_folder = Inputs.folder(
        description='Corresponding sensor grid folder to sensor grids info.'
    )

    octree = Inputs.file(
        description='A blacked out octree that includes the sunpath. This octree is '
        'used for calculating the contribution from direct sunlight.'
    )

    sun_modifiers = Inputs.file(
        description='The list of sun modifiers that are included in octree_direct_sun.'
    )

    bsdf_folder = Inputs.folder(
        description='The folder from Radiance model folder that includes the BSDF files.'
        'You only need to include the in-scene BSDFs for the two phase calculation.',
        optional=True
    )

    results_folder = Inputs.str(
        description='An optional string to define the folder that the outputs should be '
        'copied to. You can use this input to copy the final results to a folder other '
        'then the subfolder for this DAG', default='results'
    )

    @task(
        template=DirectSunlightRayTracing,
        loop=sensor_grids_info,
        # create a subfolder for each grid
        sub_folder='initial_results/{{item.full_id}}',
        # sensor_grid sub_path
        sub_paths={'sensor_grid': '{{item.full_id}}.pts'}
    )
    def direct_sunlight_raytracing(
        self,
        radiance_parameters=radiance_parameters,
        octree=octree,
        grid_name='{{item.full_id}}',
        sensor_grid=sensor_grids_folder,
        sensor_count='{{item.count}}',
        sun_modifiers=sun_modifiers,
        bsdfs=bsdf_folder
    ):
        pass

    @task(
        template=MergeFolderData,
        needs=[direct_sunlight_raytracing],
        sub_paths={
            'dist_info': '_redist_info.json'
        }
    )
    def restructure_results(
        self, identifier=identifier,
        input_folder='initial_results/direct',
        extension='ill', dist_info=sensor_grids_folder,
        results_folder=results_folder
    ):
        return [
            {
                'from': MergeFolderData()._outputs.output_folder,
                'to': '{{self.results_folder}}/{{self.identifier}}'
            }
        ]
