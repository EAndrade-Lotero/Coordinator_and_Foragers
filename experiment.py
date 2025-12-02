# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
from markupsafe import Markup
from typing import Union, List, Dict, Any

import psynet.experiment
from psynet.modular_page import Prompt, ModularPage, PushButtonControl
from psynet.timeline import Timeline
from psynet.trial.create_and_rate import (
    CreateAndRateTrialMakerMixin,
    RateTrialMixin,
)
from psynet.trial.imitation_chain import ImitationChainTrial, ImitationChainTrialMaker
from psynet.utils import get_logger

from .coordinator_classes import CoordinatorTrial
from .custom_node import CustomNode
from .game_parameters import (
    NUM_FORAGERS,
    INITIAL_POSITIONS,
    STARTING_SLIDERS,
    NUM_CENTROIDS,
    NUM_COINS,
    DISPERSION,
    LIST_OF_DISTRIBUTIONS,
    IMAGE_PATHS,
)

logger = get_logger()


class SingleRateTrial(RateTrialMixin, ImitationChainTrial):
    time_estimate = 5

    def show_trial(self, experiment, participant):
        assert self.trial_maker.target_selection_method == "one"

        list_of_pages = [
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
        positions = self.get_positions()
        forager_id = self.get_forager_id(participant)
        return positions[forager_id]

    def get_positions(self) -> List[int]:
        """
        Gets the positions of the foragers provided by the coordinator
        """
        assert len(self.targets) == 1
        target = self.targets[0]
        answers = self.get_target_answer(target)
        return answers["positions"]

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
            assert(len(available_ids) > 0), f"Error: Attempt to assign forager (participant:{participant.id}) in finished node (node:{participant._current_trial.node.id})."
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


class CreateAndRateTrialMaker(CreateAndRateTrialMakerMixin, ImitationChainTrialMaker):
    response_timeout_sec = 300 # (200% of the estimated time)
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

    start_nodes = [
        CustomNode(
            context=IMAGE_PATHS,
            seed={
                # Parameters of the world to be created
                "world_parameters": {
                    "num_coins": NUM_COINS,
                    "num_centroids": NUM_CENTROIDS,
                    "dispersion": DISPERSION,
                    "distribution": distribution
                },
                # Settings of the social contract
                "sliders": STARTING_SLIDERS,
                # Default initial positions of foragers in the world
                "positions": INITIAL_POSITIONS,
                # Default empty assignment of foragers to positions
                "assignments": dict(),
            }
        ) for distribution in LIST_OF_DISTRIBUTIONS
    ]

    return CreateAndRateTrialMaker(
        n_creators=1,
        n_raters=NUM_FORAGERS,
        node_class=CustomNode,
        creator_class=CoordinatorTrial,
        rater_class=SingleRateTrial,
        # mixin params
        include_previous_iteration=True,
        rate_mode="rate",
        target_selection_method="one",
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
        get_trial_maker()
    )
