# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
import psynet.experiment
from psynet.timeline import (
    Timeline,
    CodeBlock,
)
from psynet.utils import get_logger

from .custom_classes import CoordinatorTrial, ForagerTrial
from .custom_trialmaker import CreateAndRateTrialMaker
from .custom_node import CustomNode
from .game_parameters import (
    NUM_FORAGERS,
    OVERHEADS,
    POWER_ROLES,
    ASSETS_PATHS,
    MAX_NODES_PER_CHAIN,
    NUMBER_OF_TRIALS,
    RNG,
)

logger = get_logger()

##########################################################################################
# Experiment
##########################################################################################

START_NODES = [
    CustomNode(
        context=ASSETS_PATHS,
        seed={
            "overhead": overhead,
        },
        participant_group=participant_group
    )
    for overhead in OVERHEADS
    for participant_group in POWER_ROLES
]


def get_trial_maker():

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
        expected_trials_per_participant=NUMBER_OF_TRIALS,
        max_trials_per_participant=NUMBER_OF_TRIALS,
        start_nodes=START_NODES,
        chains_per_experiment=len(START_NODES),
        balance_across_chains=False,
        check_performance_at_end=True,
        check_performance_every_trial=False,
        propagate_failure=False,
        recruit_mode="n_trials",
        target_n_participants=None,
        wait_for_networks=False,
        max_nodes_per_chain=MAX_NODES_PER_CHAIN,
        choose_participant_group=lambda participant: participant.var.participant_group,
    )

class Exp(psynet.experiment.Experiment):
    label = "Coordinators and Foragers Experiment"
    initial_recruitment_size = 1

    timeline = Timeline(
        ############################################
        # Experiment starts here
        ############################################
        CodeBlock(
            lambda participant: participant.var.set(
                "participant_group",
                POWER_ROLES[RNG.choice(len(POWER_ROLES))],
            )
        ),
        # Start the game with trial maker
        get_trial_maker()
    )


