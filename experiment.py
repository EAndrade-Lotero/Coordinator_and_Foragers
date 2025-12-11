# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
from markupsafe import Markup

import psynet.experiment
from psynet.timeline import Timeline
from psynet.utils import get_logger
from psynet.page import InfoPage

from .custom_node import CustomNode
from .forager_classes import ForagerTrial
from .coordinator_classes import CoordinatorTrial
from .custom_trialmaker import CreateAndRateTrialMaker
from .text_variables import WELCOME_TEXT
from .game_parameters import (
    NUM_FORAGERS,
    INITIAL_POSITIONS,
    STARTING_SLIDERS,
    WORLD_PATHS,
    IMAGE_PATHS,
)

logger = get_logger()

##########################################################################################
# Experiment
##########################################################################################


def get_trial_maker():

    start_nodes = [
        CustomNode(
            context=IMAGE_PATHS,
            seed={
                # World with coins
                "world_path": world_path,
                # Settings of the social contract
                "sliders": STARTING_SLIDERS,
                # Default initial positions of foragers in the world
                "positions": INITIAL_POSITIONS,
            }
        ) for world_path in WORLD_PATHS
    ]

    return CreateAndRateTrialMaker(
        n_creators=1,
        n_raters=NUM_FORAGERS,
        node_class=CustomNode,
        creator_class=CoordinatorTrial,
        rater_class=ForagerTrial,
        # mixin params
        include_previous_iteration=True,
        rate_mode="rate",
        target_selection_method="all",
        verbose=True,  # for the demo
        # trial_maker params
        id_="coordinator_and_foragers_trial_maker",
        chain_type="across",
        expected_trials_per_participant=len(start_nodes),
        max_trials_per_participant=len(start_nodes),
        start_nodes=start_nodes,
        chains_per_experiment=len(start_nodes),
        balance_across_chains=False,
        check_performance_at_end=True,
        check_performance_every_trial=False,
        propagate_failure=False,
        recruit_mode="n_trials",
        target_n_participants=None,
        wait_for_networks=False,
        max_nodes_per_chain=10,
    )

class Exp(psynet.experiment.Experiment):
    label = "Coordinators and Foragers Experiment"
    initial_recruitment_size = 1

    timeline = Timeline(
        # InfoPage(
        #     Markup(WELCOME_TEXT),
        #     time_estimate=5
        # ),
        get_trial_maker()
    )
