# Module with the coordinator classes

##########################################################################################
# Imports
##########################################################################################
import ast
from markupsafe import Markup
from typing import (
    List, Union, Dict,
    Any, Tuple
)

from psynet.page import InfoPage
from psynet.utils import get_logger
from psynet.modular_page import (
    ModularPage,
    Prompt,
    SliderControl,
    PushButtonControl,
)
from psynet.trial.create_and_rate import RateTrialMixin
from psynet.trial.imitation_chain import ImitationChainTrial

from .custom_node import CustomNode
from .custom_front_end import ForagingControl
from .helper_classes import RewardProcessing
from .game_parameters import NUM_FORAGERS
from .text_variables import (
    FORAGER_INSTRUCTIONS,
    FORAGING_PAGE,
    SCORE_TEXT,
    WELL_BEING_TEXT,
)

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
    accumulate_answers = True

    def show_trial(self, experiment, participant):
        assert self.trial_maker.target_selection_method == "all"

        list_of_pages = [
            ModularPage(
                "forager_id",
                Prompt(Markup(FORAGER_INSTRUCTIONS)),
                PushButtonControl(
                    choices=[self.get_forager_id(participant)],
                    labels=["Next"],
                    arrange_vertically=False,
                ),
                time_estimate=self.time_estimate,
            ),
            ModularPage(
                "coins_foraged",
                Prompt(FORAGING_PAGE),
                ForagingControl(
                    position=self.get_my_trial_position(participant),
                    coins=self.get_world_coins(participant),
                    max_gear=self.get_max_gear(participant),
                    context=self.context,
                ),
                time_estimate=self.time_estimate,
            ),
            InfoPage(
                # f"You have collected {self.get_num_coins(participant)} coins!"
                f"You have collected 0 coins!",
                time_estimate=self.time_estimate,
            ),
            InfoPage(
                Markup(self.get_reward_text(participant)),
                time_estimate=self.time_estimate,
            ),
            # Asks coordinator well-being
            ModularPage(
                "well-being",
                Prompt(Markup(WELL_BEING_TEXT)),
                SliderControl(
                    start_value=0.5,
                    min_value=0.0,
                    max_value=1,
                    n_steps=100,
                ),
                time_estimate=self.time_estimate,
            ),
        ]

        return list_of_pages

    def get_my_trial_position(self, participant):
        """
        Gets the position of the trial
        """
        positions = self.get_positions(participant)
        forager_id = self.get_forager_id(participant)
        position = positions[forager_id]
        logger.info(f"Forager {forager_id} has position {position}")
        return position

    def get_positions(self, participant) -> List[Tuple[int, int]]:
        """
        Gets the positions of the foragers provided by the coordinator
        """
        # Get positions and coins from coordinator
        positions_and_coins = self.get_positions_and_coins(participant)
        # Keep positions
        positions = positions_and_coins["positions"]
        # Verify type of positions
        if isinstance(positions, str):
            try:
                positions = ast.literal_eval(positions)
            except Exception as e:
                logger.error(f"Error parsing {positions}")
                raise e
        assert isinstance(positions, list), f"Error: expected list, got {type(positions)}"
        logger.info(f"Positions obtained {positions}")
        return positions

    def get_positions_and_coins(self, participant) -> Dict[str, List[Tuple[int, int]]]:
        # Get answers
        coordinator_answers = self.get_answer_from_coordinator(participant)
        # Extract positions from answers
        assert "positions_and_coins" in coordinator_answers.keys(), f"Error: Found no positions_and_coins in coordinator's answers: {coordinator_answers.keys()}"
        return coordinator_answers["positions_and_coins"]

    def get_answer_from_coordinator(self, participant) -> Dict[str, Any]:
        # Get current node
        current_node = participant.current_trial.node
        # Get answers
        coordinator_answers = self.get_answers_from_role('coordinator', current_node)
        assert len(coordinator_answers) == 1, f"Error: Found more than one coordinator in node {current_node.id}"
        coordinator_answers = coordinator_answers[0]
        return coordinator_answers

    def get_forager_id(self, participant) -> int:
        """
        Checks if trial is assigned a forager id and, if not, give it one.
        """
        # Useful records
        trial_id = str(participant.current_trial.id)
        current_node = participant.current_trial.node
        # Check if I have a forager id.
        try:
            forager_id = participant.current_trial.vars["forager_id"]
            forager_id = int(forager_id)
        except:
            # No forager id yet
            # Determining forager ids from other foragers
            # First, get the answers from other forager trials
            other_foragers_answers = self.get_answers_from_role('forager', current_node)
            # Determine the taken ids
            taken_ids = [answer["forager_id"] for answer in other_foragers_answers]
            taken_ids = [int(idx) for idx in taken_ids]
            # Get a list of available ids
            available_ids = [idx for idx in range(NUM_FORAGERS) if idx not in taken_ids]
            assert (len(available_ids) > 0), f"Error: Attempt to assign forager (trial:{trial_id}) in node (node:{participant.current_trial.node.id})."
            # Get the first available id as a forager_id
            forager_id = available_ids[0]
            # Register forager id in working memory for the trial
            participant.current_trial.vars["forager_id"] = forager_id

        logger.info(f"Trial {trial_id} was assigned to forager {forager_id}")
        return forager_id

    def get_answers_from_role(self, role: str, node: CustomNode) -> List[Dict[str, Any]]:
        """Gets the answers from the trial or trials of the given rol"""
        """
        Gets the positions of the foragers provided by the coordinator
        """
        assert role in ['coordinator', 'forager'], f"Error: expected 'coordinator' or 'forager', got {role}"
        # Get the trials that are finalized and not failed that have the required role
        trials_with_role_in_node = [
            trial for trial in node.all_trials
            if (
                    trial.finalized == True
                    and trial.failed == False
                    and role in str(trial).lower()
            )
        ]
        logger.info(f"Found {len(trials_with_role_in_node)} trials with {role} role in node {node.id}")
        if len(trials_with_role_in_node) == 0:
            return []
        # Get answers from trials
        list_of_answers = [self.get_answers_from_trial(trial) for trial in trials_with_role_in_node]
        return list_of_answers

    def get_answers_from_trial(self, trial: ImitationChainTrial) -> Dict[str, Any]:
        """Extract the answers from the given trial"""
        assert isinstance(trial, ImitationChainTrial), f"Error: expected ImitationChainTrial, got {type(trial)}"
        # Extract the answer
        answer = self.get_target_answer(trial)
        assert isinstance(answer, dict), f"Error: expected dict, got {type(answer)} --- {answer=}"
        return answer

    def get_world_coins(self, participant) -> List[Tuple[int, int]]:
        coins = self.get_initial_coins(participant)
        # Get the answers from other forager trials
        other_foragers_answers = self.get_answers_from_role('forager', participant.current_trial.node)
        # Subtract the coins gathered by each forager
        for answer in other_foragers_answers:
            other_forager_coins = [tuple(coin) for coin in answer["coins_foraged"]]
            # logger.info(f"Other forager collected coins: {other_forager_coins}")
            if isinstance(other_forager_coins, str):
                other_forager_coins = ast.literal_eval(other_forager_coins)
            if len(other_forager_coins) > 0:
                coins = [(coin) for coin in coins if coin not in other_forager_coins]
        # logger.info(f"Remaining coins: {coins}")
        return coins

    def get_initial_coins(self, participant) -> List[Tuple[int, int]]:
        # Get positions and coins from coordinator
        positions_and_coins = self.get_positions_and_coins(participant)
        # Keep only coins
        coins = positions_and_coins["coins"]
        # Verify type of coins
        if isinstance(coins, str):
            try:
                coins = ast.literal_eval(coins)
            except Exception as e:
                logger.error(f"Error parsing {coins}")
                raise e
        assert isinstance(coins, list), f"Error: expected list, got {type(coins)}"
        # logger.info(f"All coins in the world at the beginning: {coins}")
        return coins

    def get_max_gear(self, participant) -> int:
        coordinator_answers = self.get_answer_from_coordinator(participant)
        prerogative = coordinator_answers["prerogative"]
        if isinstance(prerogative, str):
            prerogative = ast.literal_eval(prerogative)
        assert isinstance(prerogative, float), f"Error: expected float, got {type(prerogative)}"
        max_gear = int(prerogative * 2)
        return max_gear

    def get_num_coins(self, participant) -> int:
        if participant.answer_accumulators[-1] is not None:
            last_answer = participant.answer_accumulators[-1]
            # assert isinstance(last_answer, List(Tuple[int, int])), f"Error: expected list, got {type(last_answer)}"
            assert "coins_foraged" in last_answer.keys()
            coins = last_answer["coins_foraged"]
            if isinstance(coins, str):
                coins = ast.literal_eval(coins)
            return len(coins)
        else:
            return 0

    def get_reward_text(self, participant) -> Markup:
        try:
            n_coins = participant.current_trial.definition["n_coins"]
        except:
            logger.info(f"Could not get number of coins")
            n_coins = 10
        try:
            sliders = participant.current_trial.definition["sliders"]
        except:
            sliders = {
                "overhead":1,
                "wages":1,
                "prerogative":1,
            }
            logger.info(f"Could not get sliders")
        try:
            text = RewardProcessing.get_reward(
                n_coins=n_coins,
                sliders=sliders,
                trial_type=f"forager-{self.get_forager_id(participant)}",
            )
        except:
            text = f"Error: Could not get reward for forager-{self.get_forager_id(participant)}"
            logger.info(text)
        text = SCORE_TEXT(text)
        return Markup(text)

    def format_answer(self, raw_answer, **kwargs) -> Union[float, str]:
        try:
            # answer = raw_answer["well-being"]
            # return answer
            return raw_answer
        except (ValueError, AssertionError) as e:
            logger.info(f"Error: {e}")
            return f"INVALID_RESPONSE"

###########################################