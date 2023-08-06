from pollination.five_phase.entry import RecipeEntryPoint
from queenbee.recipe.dag import DAG


def test_five_phase():
    recipe = RecipeEntryPoint().queenbee
    assert recipe.name == 'recipe-entry-point'
    assert isinstance(recipe, DAG)
