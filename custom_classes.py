# Module with the coordinator classes
import ast

##########################################################################################
# Imports
##########################################################################################
from typing import (
    List, Union, Dict,
    Any, Tuple, Optional
)

from psynet.page import InfoPage
from psynet.utils import get_logger
from psynet.trial.create_and_rate import (
    CreateTrialMixin,
    RateTrialMixin,
)
from psynet.trial.imitation_chain import ImitationChainTrial
from psynet.timeline import (
    CodeBlock,
    PageMaker,
    for_loop,
    join,
)
from psynet.modular_page import (
    ModularPage,
    Prompt,
    PushButtonControl,
)

from .game_parameters import (
    COORDINATOR_INITIAL_ENDOWMENT,
    NUM_ROUNDS,
)
from .variable_handler import VariableHandler

variable_handler = VariableHandler(
    level="trial",
    use_vars=True,
)
variable_handler.debug = True

logger = get_logger()
Pos = Tuple[int, int]  # (x, y)


###########################################
# Coordinator
###########################################

class CoordinatorTrial(CreateTrialMixin, ImitationChainTrial):
    time_estimate = 320
    accumulate_answers = True

    def show_trial(self, experiment, participant):

        variable_handler.set_value(participant, "budget_dict", {0: COORDINATOR_INITIAL_ENDOWMENT})

        list_of_pages = [
            InfoPage(
                "This is going to be the instructions for the COORDINATOR.",
                time_estimate=1,
            ),
            # MAIN LOOP IS HERE
            for_loop(
                label="test_rounds",
                iterate_over=range(NUM_ROUNDS),
                logic=lambda number: join(
                    ModularPage(
                        label="answer",
                        prompt=Prompt(f"This is round {number}"),
                        control=PushButtonControl(
                            choices=[
                                f"{number}: {variable_handler.get_value(participant, 'budget_dict')}"
                            ],
                            labels=["Next"]
                        ),
                        time_estimate=5,
                    ),
                    CodeBlock(
                        lambda participant: variable_handler.set_dictionary_value(
                            participant=participant,
                            dictionary_name="budget_dict",
                            key=number,
                            value=number+1,
                        )
                    )
                ),
                time_estimate_per_iteration=5,
            ),
        ]

        return list_of_pages


###########################################
# Forager
###########################################

class ForagerTrial(RateTrialMixin, ImitationChainTrial):
    time_estimate = 181
    accumulate_answers = True

    def show_trial(self, experiment, participant):
        assert self.trial_maker.target_selection_method == "all"

        list_of_pages = [
            # Info movement
            InfoPage(
                "Here we go forager!",
                time_estimate=5,
            ),
        ]

        return list_of_pages

    def format_answer(self, raw_answer, **kwargs) -> Union[float, str]:
        logger.info(f"Entering forager format answer. Cross your fingers!")
        try:
            if isinstance(raw_answer, dict):
                if "reward" in raw_answer.keys():
                    answer = raw_answer["reward"]
                    return int(answer)
            return 0.0
        except (ValueError, AssertionError) as e:
            text = f"Something went wrong. Current trial doesn't have rewards.\n"
            text += f"raw_answer => {raw_answer}\n"
            text += f"Error: {e}"
            logger.info(text)
            return f"INVALID_RESPONSE"

###########################################
