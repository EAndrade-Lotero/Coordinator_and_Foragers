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
from .game_parameters import (
    NUM_FORAGERS,
)

logger = get_logger()

###########################################
# Custom prompts
###########################################


###########################################
# Custom controls
###########################################

class PositioningControl(Control):
    macro = "positioning_area"
    external_template = "positioning-control.html"

    def __init__(
        self,
        world:Dict[str, float],
        context:Dict[str, Path],
        investment:float,
    ) -> None:
        super().__init__()
        # Create world
        logger.info(f"World parameters: {world}")
        self.world = World(**world)
        # world.map_path = context["map_url"]
        # world.coin_path = context["coin_url"]
        # world.forager_path = context["forager_url"]
        # Check investment (used in probability of showing a coin)
        assert investment is not None
        self.map = world.generate_rgba_array()
        self.forager_url = context["forager_url"]
        self.map_url = context["map_url"]
        self.num_foragers = NUM_FORAGERS

    def format_answer(self, raw_answer, **kwargs):
        try:
            assert raw_answer is not None
            assert isinstance(raw_answer, list)
            positions_and_coins ={
                'positions': raw_answer,
                'coins': self.world.coin_positions()
            }
            return positions_and_coins
        except (ValueError, AssertionError):
            return f"INVALID_RESPONSE"

###########################################

class ForagingControl(Control):
    macro = "foraging_area"
    external_template = "foraging-control.html"

    def __init__(
        self,
        world:Dict[str, float],
        context:Dict[str, Path],
    ) -> None:
        super().__init__()
        # Create world
        logger.info(f"World parameters: {world}")
        self.world = World(**world)
        self.map = self.world.generate_terrain()
        self.forager_url = context["forager_url"]
        self.map_url = context["map_url"]
        self.num_foragers = NUM_FORAGERS

    def format_answer(self, raw_answer, **kwargs):
        try:
            # assert raw_answer is not None
            # assert isinstance(raw_answer, list)
            # return raw_answer
            logger.info(f"Coins foraged: {raw_answer}")
            return raw_answer
        except (ValueError, AssertionError):
            return f"INVALID_RESPONSE"

###########################################
