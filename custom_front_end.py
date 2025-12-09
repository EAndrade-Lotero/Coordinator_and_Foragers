# Module with custom prompts and controls

##########################################################################################
# Imports
##########################################################################################
import numpy as np

from pathlib import Path
from typing import Dict

from psynet.modular_page import (
    Control,
)
from psynet.utils import get_logger

from .helper_classes import (
    World,
)
from .game_parameters import INITIAL_POSITIONS

logger = get_logger()

###########################################
# Custom prompts
###########################################


###########################################
# Custom controls
###########################################

class PositioningControl(Control):
    macro = "positioning_area"
    external_template = "custom-controls.html"

    def __init__(
        self,
        world:Dict[str, float],
        context:Dict[str, Path],
        investment:float,
    ) -> None:
        super().__init__()
        # Create world
        logger.info(f"World parameters: {world}")
        world = World(**world)
        world.map_path = context["map_url"]
        world.coin_path = context["coin_url"]
        world.forager_path = context["forager_url"]
        assert investment is not None
        logger.info(f"Investment on my end is: {investment}")
        # assert investment > 0
        # map_numpy = world.render(
        #     show=False,
        #     coin_percentage=investment,
        #     coin_zoom=1e-2
        # )
        map_numpy = np.array(World.generate_rgba_array(w=10, h=10))
        logger.info(f"{map_numpy.shape=}")
        self.map = map_numpy.tolist()
        l = np.where(map_numpy != 255)
        logger.info(f"Num of non-white arguments in RGBA array: {l[0].shape[0]}")
        # assert l[0].shape[0] > 0, f"{investment=} {l=}"
        self.forager_url = context["forager_url"]
        self.map_url = context["map_url"]
        self.num_foragers = world.num_foragers

    def format_answer(self, raw_answer, **kwargs):
        try:
            # assert raw_answer is not None
            # assert isinstance(raw_answer, dict)
            return INITIAL_POSITIONS
        except (ValueError, AssertionError):
            return f"INVALID_RESPONSE"

###########################################
