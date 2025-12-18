# Module with custom prompts and controls

##########################################################################################
# Imports
##########################################################################################
from pathlib import Path
from typing import Dict, Union, List, Tuple

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
        world_path:str,
        context:Dict[str, Path],
        investment:float,
    ) -> None:
        super().__init__()
        # Create world
        self.world = World.generate_from_json(Path(world_path))
        # logger.info(f"Coins created at: {self.world.coin_positions()}")
        # Check investment (used in probability of showing a coin)
        assert investment is not None
        # Generate attributes
        logger.info(f"Trying rgb generation...")
        self.map = self.world.coordinator_view(investment)
        logger.info(f"Generated!")
        self.forager_url = context["forager_url"]
        self.map_url = self.world.map_path
        self.num_foragers = NUM_FORAGERS
        logger.info("World created successfully!")

    def format_answer(self, raw_answer, **kwargs):
        try:
            assert raw_answer is not None
            assert isinstance(raw_answer, list)
            positions_and_coins ={
                'positions': raw_answer,
                'coins': self.world.coin_positions()
            }
            logger.info(f"Coordinator decided positions: {positions_and_coins['positions']}")
            # logger.info(f"World contains coins in: {positions_and_coins['coins']}")
            return positions_and_coins
        except (ValueError, AssertionError):
            return f"INVALID_RESPONSE"

###########################################

class ForagingControl(Control):
    macro = "foraging_area"
    external_template = "foraging-control.html"

    def __init__(
        self,
        position: Tuple[int, int],
        coins: List[Tuple[int, int]],
        max_gear: int,
        context:Dict[str, Path],
    ) -> None:
        super().__init__()
        self.pos_x = position[0]
        self.pos_y = position[1]
        # Create world from json
        self.world = World.generate_from_coins(coins)
        # logger.info(f"Coins in world: {self.world.coin_positions()}")
        self.map = self.world.generate_terrain()
        self.forager_url = context["forager_url"]
        self.map_url = self.world.map_path
        self.num_foragers = NUM_FORAGERS
        assert 0 <= max_gear <=2 and isinstance(max_gear, int)
        self.max_gear = max_gear
        self.enabled = ['true' if i <= max_gear else 'false' for i in range(3)]

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
