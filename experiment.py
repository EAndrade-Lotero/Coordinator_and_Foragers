# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
import json
from markupsafe import Markup

from psynet.consent import NoConsent # <= Don't use it but include the consent
import psynet.experiment
from psynet.page import InfoPage
from psynet.timeline import Timeline
from psynet.utils import get_logger
# from sqlalchemy.testing import assert_warns

from .coordinator_classes import CoordinatorTrial
from .forager_classes import ForagerTrial
from .custom_trialmaker import CreateAndRateTrialMaker
from .custom_node import CustomNode
from .game_parameters import (
    NUM_FORAGERS,
    INITIAL_WEALTH,
    STARTING_SLIDERS,
    WORLD_PATHS,
    IMAGE_PATHS,
)
from .text_variables import WELCOME_TEXT

logger = get_logger()


##########################################################################################
# Experiment
##########################################################################################


def get_trial_maker():

    start_nodes = [
        CustomNode(
            context=IMAGE_PATHS,
            seed={
                "sliders": STARTING_SLIDERS,
                "world_path": world_path,
                "n_coins": INITIAL_WEALTH,
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

def get_prolific_settings():
    with open("qualification_prolific_en.json", "r") as f:
        qualification = json.dumps(json.load(f))
    return {
        "recruiter": "prolific",
        "base_payment": 4.5,
        "prolific_estimated_completion_minutes": 30,
        "prolific_recruitment_config": qualification,
        "auto_recruit": False,
        "wage_per_hour": 9,
        "currency": "£",
        "show_reward": False,
        "show_progress_bar": True,
    }

class Exp(psynet.experiment.Experiment):
    label = "Coordinators and Foragers Experiment"
    initial_recruitment_size = 1

    config = {
        "recruiter": "hotair",
        "wage_per_hour": 9,
        "currency": "£",
        # **get_prolific_settings(),
        "title": "Coordinator and foragers",
        "description": "This is the experiment",
        'initial_recruitment_size': 1,
        "auto_recruit": False,
        "show_reward": True,
        "show_progress_bar": True,
    }

    timeline = Timeline(
        NoConsent(),
        # General instructions page
        InfoPage(
            Markup(WELCOME_TEXT),
            time_estimate=120
        ),
        # Start the game with trial maker
        get_trial_maker()
    )


