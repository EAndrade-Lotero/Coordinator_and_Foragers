# Module with the coordinator classes

##########################################################################################
# Imports
##########################################################################################
import ast
from markupsafe import Markup
from typing import List, Union

from psynet.page import InfoPage
from psynet.utils import get_logger
from psynet.modular_page import (
    ModularPage,
    Prompt,
    PushButtonControl,
)
from psynet.trial.create_and_rate import RateTrialMixin
from psynet.trial.imitation_chain import ImitationChainTrial

from .custom_node import CustomNode
from .coordinator_classes import CoordinatorTrial
from .game_parameters import NUM_FORAGERS
from .text_variables import FORAGER_INSTRUCTIONS

logger = get_logger()

###########################################
# Forager classes
###########################################

########################
# Pages

# NO PAGES

########################
# Trial

class ForagerTrial(RateTrialMixin, ImitationChainTrial):
    time_estimate = 5

    def show_trial(self, experiment, participant):
        assert self.trial_maker.target_selection_method == "one"

        list_of_pages = [
            InfoPage(
                Markup(FORAGER_INSTRUCTIONS),
                time_estimate=self.time_estimate,
            ),
            ModularPage(
                "rate_trial",
                Prompt(text=f"You have been assigned to position: {self.get_trial_position(participant)}"),
                PushButtonControl(
                    choices=[1],
                    labels=["Next"],
                    arrange_vertically=False,
                ),
                time_estimate=self.time_estimate,
            )
        ]

        return list_of_pages

    def get_trial_position(self, participant):
        """
        Gets the position of the trial
        """
        positions = self.get_positions()
        forager_id = self.get_forager_id(participant)
        return positions[forager_id]

    def get_positions(self) -> List[int]:
        """
        Gets the positions of the foragers provided by the coordinator
        """
        assert len(self.targets) == 1
        target = self.targets[0]
        logger.info(f"First pass at target obtained type {type(target)}")
        if isinstance(target, CustomNode):
            target = self.get_target_answer(target)
            logger.info(f"A second pass was needed and obtained type {type(target)}")
        if isinstance(target, CoordinatorTrial):
            answers = self.get_target_answer(target)
        elif isinstance(target, dict):
            answers = target
        else:
            raise Exception(f"Unexpected type {type(target)}")
        assert isinstance(answers, dict), f"Error: Expected dict, got {type(answers)}."
        positions = answers["positions"]
        if isinstance(positions, str):
            try:
                positions = ast.literal_eval(positions)
            except Exception as e:
                logger.error(f"Error parsing {positions}")
                raise e
        logger.info(f"Positions obtained {positions}")
        return positions

    def get_forager_id(self, participant) -> int:
        """
        Checks if trial is assigned a forager id and, if not, give it one.

        The convention I'm following is:
            - trial ids must be coerced to strings
            - forager ids must be coerced to integers
        """
        try:
            assignments = participant._current_trial.node.vars["assignments"]
        except:
            assignments = dict()
            participant._current_trial.node.vars["assignments"] = assignments

        logger.info(f"Assignments old: {assignments}")

        trial_id = str(participant.id)

        if trial_id in assignments.keys():
            idx = assignments[trial_id]
            idx = int(idx)
        else:
            taken_ids = [int(idx) for idx in assignments.values()]
            available_ids = [idx for idx in range(NUM_FORAGERS) if idx not in taken_ids]
            assert (
                        len(available_ids) > 0), f"Error: Attempt to assign forager (participant:{participant.id}) in finished node (node:{participant._current_trial.node.id})."
            idx = available_ids[0]
            assignments[trial_id] = idx
            participant._current_trial.node.vars["assignments"] = assignments

        logger.info(f"Assigning trial {trial_id} to forager id {idx}")
        logger.info(f"Assignments new: {assignments}")

        return idx

    def format_answer(self, raw_answer, **kwargs) -> Union[float, str]:
        try:
            answer = raw_answer["rate_trial"]
            return answer
        except (ValueError, AssertionError) as e:
            logger.info(f"Error: {e}")
            return f"INVALID_RESPONSE"

###########################################