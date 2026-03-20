# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
import psynet.experiment
from psynet.timeline import (
    Timeline,
    CodeBlock,
    join,
)
from psynet.page import InfoPage
from psynet.modular_page import ModularPage, PushButtonControl
from psynet.utils import get_logger
from psynet.trial.create_and_rate import CreateAndRateTrialMakerMixin
from psynet.trial.imitation_chain import ImitationChainTrialMaker
from psynet.trial import ChainNode
from psynet.trial.create_and_rate import CreateAndRateNodeMixin
from psynet.trial.create_and_rate import (
    CreateTrialMixin,
    RateTrialMixin,
)
from psynet.trial.imitation_chain import ImitationChainTrial

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
# Node
##########################################################################################
class CustomNode(CreateAndRateNodeMixin, ChainNode):

    def create_definition_from_seed(self, seed, experiment, participant):
        return seed

##########################################################################################
# TrialMaker
##########################################################################################
class CreateAndRateTrialMaker(CreateAndRateTrialMakerMixin, ImitationChainTrialMaker):
    pass

##########################################################################################
# Coordinator Trial
##########################################################################################
class CoordinatorTrial(CreateTrialMixin, ImitationChainTrial):

    time_estimate = 320
    accumulate_answers = True

    def show_trial(self, experiment, participant):
        return join([
            InfoPage(
                "This is the information investment page",
                time_estimate=self.time_estimate,
            ),
            ModularPage(
                label="locations",
                prompt="This assign the locations",
                control=PushButtonControl(
                    labels=["Next"],
                    choices=["[pos1, pos2]"]
                ),
                time_estimate=self.time_estimate,
            )
        ])

##########################################################################################
# Forager Trial
##########################################################################################
class ForgerTrial(RateTrialMixin, ImitationChainTrial):
    time_estimate = 320
    accumulate_answers = True

    def show_trial(self, experiment, participant):
        return join([
            InfoPage(
                "This is the fuel investment page",
                time_estimate=self.time_estimate,
            ),
            ModularPage(
                label="locations",
                prompt="This harvests the coins",
                control=PushButtonControl(
                    labels=["Next"],
                    choices=["[coin1, coin2, coin3]"]
                ),
                time_estimate=self.time_estimate,
            )
        ])


##########################################################################################
# Experiment
##########################################################################################

START_NODES = [
    CustomNode(
        context=ASSETS_PATHS,
        seed={
            "commission": 0.5,
        },
        participant_group="forager"
    )
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
                RNG.choice(POWER_ROLES),
            )
        ),
        # Start the game with trial maker
        get_trial_maker()
    )


