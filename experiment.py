# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
# from markupsafe import Markup
import ast
from typing import Union, List, Any, Dict

import psynet.experiment
from psynet.modular_page import Prompt, ModularPage, PushButtonControl
from psynet.timeline import Timeline
from psynet.utils import get_logger
from sqlalchemy.testing import assert_warns

from .custom_pages import SliderSettingPage
from .custom_node import CustomNode
from .game_parameters import (
    NUM_FORAGERS,
    INITIAL_POSITIONS,
    STARTING_SLIDERS,
    WORLD_PATHS,
    IMAGE_PATHS,
)

logger = get_logger()


class CoordinatorTrial(CreateTrialMixin, ImitationChainTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):

        list_of_pages = [
            ModularPage(
                "positions",
                Prompt(text="This is a dummy positioning page"),
                PushButtonControl(
                    choices=[INITIAL_POSITIONS],
                    labels=["Next"],
                    arrange_vertically=False,
                ),
                time_estimate=self.time_estimate,
            ),
            SliderSettingPage(
                dimension="overhead",
                start_value=self.get_slider_value(participant, "overhead"),
                time_estimate=self.time_estimate,
            )
        ]

        return list_of_pages

    def get_slider_value(self, participant, parameter) -> float:
        value = participant._current_trial.definition[parameter]
        if isinstance(value, tuple):
            value = value[0]
        assert isinstance(value, float), f"Error: expected float, got {type(value)} --- {value=}"
        return value


class ForagerTrial(RateTrialMixin, ImitationChainTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):
        assert self.trial_maker.target_selection_method == "all"

        list_of_pages = [
            ModularPage(
                "forager_id",
                Prompt(text=f"Congratulations! You are a forager!"),
                PushButtonControl(
                    choices=[self.get_forager_id(participant)],
                    labels=["Next"],
                    arrange_vertically=False,
                ),
            ),
            ModularPage(
                "rate_trial",
                Prompt(text=f"You have been assigned to position: {self.get_trial_position(participant)}"),
                PushButtonControl(
                    choices=[1],
                    labels=["Next"],
                    arrange_vertically=False,
                ),
            )
        ]

        return list_of_pages

    def get_trial_position(self, participant):
        """
        Gets the position of the trial
        """
        positions = self.get_positions(participant)
        forager_id = self.get_forager_id(participant)
        position = positions[forager_id]
        logger.info(f"Trial {forager_id} has position {position}")
        return position

    def get_positions(self, participant) -> List[int]:
        """
        Gets the positions of the foragers provided by the coordinator
        """
        # Get current node
        current_node = participant.current_trial.node
        # Get answers.
        coordinator_answers = self.get_answers_from_role('coordinator', current_node)
        assert len(coordinator_answers) == 1, f"Error: Found more than one coordinator in node {current_node.id}"
        coordinator_answers = coordinator_answers[0]
        # Extract positions from answers
        assert "positions" in coordinator_answers.keys(), f"Error: Found no positions in coordinator's answers: {coordinator_answers.keys()}"
        positions = coordinator_answers["positions"]
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
            assert(len(available_ids) > 0), f"Error: Attempt to assign forager (trial:{trial_id}) in node (node:{participant.current_trial.node.id})."
            # Get the first available id as a forager_id
            forager_id = available_ids[0]
            # Register forager id in working memory for the trial
            participant.current_trial.vars["forager_id"] = forager_id

        logger.info(f"Trial {trial_id} was assigned to forager id {forager_id}")
        return forager_id

    def get_answers_from_role(self, role:str, node:CustomNode) -> List[Dict[str, Any]]:
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

    def get_answers_from_trial(self, trial:ImitationChainTrial) -> Dict[str, Any]:
        """Extract the answers from the given trial"""
        assert isinstance(trial, ImitationChainTrial), f"Error: expected ImitationChainTrial, got {type(trial)}"
        # Extract the answer
        answer = self.get_target_answer(trial)
        assert isinstance(answer, dict), f"Error: expected dict, got {type(answer)} --- {answer=}"
        return answer

    def format_answer(self, raw_answer, **kwargs) -> Union[float, str]:
        try:
            # answer = raw_answer["rate_trial"]
            # return answer
            return raw_answer
        except (ValueError, AssertionError) as e:
            logger.info(f"Error: {e}")
            return f"INVALID_RESPONSE"


class CreateAndRateTrialMaker(CreateAndRateTrialMakerMixin, ImitationChainTrialMaker):
    response_timeout_sec = 300 # (200% of the estimated time)
    check_timeout_interval_sec = 30
    allow_revisiting_networks_in_across_chains = False

    def custom_network_filter(self, candidates, participant) -> List[Any]:
        """
        # Filter out networks with active trials
        """
        logger.info("Applying custom network filter...")
        # Exclude networks with active trials
        filtered_networks = [
            network for network in candidates
            if (
                not self.has_active_trials(network)
            )
        ]
        return filtered_networks

    def has_active_trials(self, network: Any) -> bool:
        active_trials = [
            trial.id for trial in network.all_trials
            if (
                trial.finalized == False
                and trial.failed == False
            )
        ]
        return len(active_trials) > 0


##########################################################################################
# Experiment
##########################################################################################


def get_trial_maker():

    seed_definition = {
        "overhead": 1.0,
        "positions": INITIAL_POSITIONS,
    }
    start_nodes = [
        CustomNode(context={}, seed=seed_definition)
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
