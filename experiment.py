# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
from cProfile import label
from typing import Union, Optional, List

from markupsafe import Markup

import psynet.experiment
from psynet.timeline import (
    Timeline,
    CodeBlock,
    join,
    PageMaker,
)
from psynet.page import InfoPage
from psynet.modular_page import (
    ModularPage,
    PushButtonControl,
    Control,
    Prompt,
)
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
    WORLD_WIDTH,
    WORLD_HEIGHT,
    NUM_ROUNDS,
)
from .variable_handler import VariableHandler

logger = get_logger()
variable_handler = VariableHandler()

##########################################################################################
# Prompt
##########################################################################################
class CustomPrompt(Prompt):

    macro = "timeout"
    external_template = "custom-prompt-with-timer.html"

    def __init__(
        self,
        timeout:int,
        timeout_answer:str='No answer',
        text: Union[None, str, Markup] = None,
        text_align: str = "left",
        buttons: Optional[List] = None,
        loop: bool = False,
    ):
        super().__init__(
            text=text,
            text_align=text_align,
            buttons=buttons,
            loop=loop,
        )
        self.timeoutSeconds = 10
        self.timeoutAnswer = timeout_answer


##########################################################################################
# Control
##########################################################################################
class CustomControl(Control):

    macro = "locating_foragers"
    external_template = "position-foragers-control.html"

    def __init__(self):
        super().__init__()
        self.test = "This is a new test"


##########################################################################################
# Pages
##########################################################################################
class CustomPage(ModularPage):

    def __init__(
        self,
        label,
        time_estimate:int,
        timeout: int=10,
        timeout_answer: str='No answer',
    ) -> None:

        # Initialize the modular page
        super().__init__(
            label=label,
            prompt=CustomPrompt(
                timeout=timeout,
                timeout_answer=timeout_answer,
                text="Please drag the icon you prefer on the right rectangle:",
            ),
            # prompt="Please drag the icon you prefer on the right rectangle:",
            control=CustomControl(),
            time_estimate=time_estimate,
            save_answer=label,
        )

    def format_answer(self, raw_answer, **kwargs):
        logger.info(f"Page Raw answer: {raw_answer}")

        raw_positions = raw_answer['placements']
        positions = dict()
        for dict_position in raw_positions:
            placed = dict_position['placed']
            forager_id = dict_position['id'][-1]
            if placed:
                positions[forager_id] = (dict_position['x'], dict_position['y'])
            else:
                positions[forager_id] = (
                    RNG.integers(0, WORLD_WIDTH, 1),
                    RNG.integers(0, WORLD_HEIGHT, 1)
                )  # <= modify depending on expected performance

        logger.info(f"Positions: {positions}")
        return positions


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
            #---------------------------------------
            # INSTRUCTIONS
            #---------------------------------------
            InfoPage(
                "This is the INSTRUCTIONS",
                time_estimate=self.time_estimate,
            ),
            #---------------------------------------
            # ROUNDS
            #---------------------------------------
            self.get_rounds(),
            #---------------------------------------
            # DEBRIEF
            #---------------------------------------
            ModularPage(
                label="locations",
                prompt="This is all folks!",
                control=PushButtonControl(
                    labels=["Next"],
                    choices=["[pos1, pos2]"]
                ),
                time_estimate=self.time_estimate,
            )
        ])

    def get_rounds(self):
        # ---------------------------------------
        # LIST OF ROUNDS
        # ---------------------------------------
        list_of_lists = [
            # ---------------------------------------
            # SINGLE ROUND
            # ---------------------------------------
            [
                CustomPage(
                    label=f"positions-{i}",
                    time_estimate=20,
                ),
                CodeBlock(
                    lambda participant: logger.info(f"Answer accumulators: {participant.answer_accumulators}"),
                ),
                InfoPage(
                    f"{self.get_value_from_last_answer()}",
                    time_estimate=5
                ),
            ]
            for i in range(NUM_ROUNDS)
        ]
        list_of_lists = [page for list_ in list_of_lists for page in list_]
        return join(list_of_lists)

    def get_value_from_last_answer(self):
        logger.info(f"Answer accumulators: {self.participant.answer_accumulators}")
        if len(self.participant.answer_accumulators) > 0:
            last_answer = self.participant.answer_accumulators[-1]
            logger.info(f"Last answer: {last_answer}")
            answers = []
            for key, value in last_answer.items():
                answers.append(value)
            if len(answers) > 0:
                return answers[-1]
        return "Hang tight!"

##########################################################################################
# Forager Trial
##########################################################################################
class ForagerTrial(RateTrialMixin, ImitationChainTrial):
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
                    choices=[0]
                ),
                time_estimate=self.time_estimate,
            )
        ])

    def format_answer(self, raw_answer, **kwargs):
        answer = raw_answer['locations']
        return answer


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
        target_selection_method="one",
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


