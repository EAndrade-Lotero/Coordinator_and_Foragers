# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
from markupsafe import Markup
from typing import Union, List, Dict, Any

import psynet.experiment
from psynet.modular_page import ImagePrompt, ModularPage, PushButtonControl, NullControl
from psynet.timeline import Timeline, CodeBlock
from psynet.trial.create_and_rate import (
    CreateAndRateNode,
    CreateAndRateTrialMakerMixin,
    CreateTrialMixin,
    RateTrialMixin,
)
from psynet.trial.imitation_chain import ImitationChainTrial, ImitationChainTrialMaker
from psynet.utils import get_logger
from psynet.trial import ChainNode
from psynet.trial.create_and_rate import CreateAndRateNodeMixin


from .custom_pages import SliderSettingPage
from .game_parameters import NUM_FORAGERS

logger = get_logger()


def animal_prompt(text, img_url):
    return ImagePrompt(
        url=img_url,
        text=Markup(text),
        width="300px",
        height="300px",
    )

class DummyControl(NullControl):

    def __init__(self):
        super().__init__()

    def format_answer(self, raw_answer, **kwargs) -> Union[List[str], str]:
        try:
            answer = ["A", "B"]
            return answer
        except (ValueError, AssertionError) as e:
            logger.info(f"Error: {e}")
            return f"INVALID_RESPONSE"


class CoordinatorTrial(CreateTrialMixin, ImitationChainTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):

        list_of_pages = [
            ModularPage(
                "positions",
                animal_prompt(text="Describe the animal", img_url=self.context["img_url"]),
                DummyControl(),
                time_estimate=self.time_estimate,
            ),
            SliderSettingPage(
                dimension="overhead",
                start_value=self.get_slider_value(participant),
                time_estimate=self.time_estimate,
            )
        ]

        return list_of_pages

    def get_slider_value(self, participant) -> float:
        overhead = participant._current_trial.definition["overhead"]
        return overhead


class SingleRateTrial(RateTrialMixin, ImitationChainTrial):
    time_estimate = 5

    def show_trial(self, experiment, participant):
        assert self.trial_maker.target_selection_method == "one"

        list_of_pages = [
            ModularPage(
                "rate_trial",
                animal_prompt(
                    text=f"You have been assigned to position:<br><strong>{self.get_trial_position(participant)}</strong>",
                    img_url=self.context["img_url"],
                ),
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
    pass

class CustomNode(CreateAndRateNodeMixin, ChainNode):

    def create_definition_from_seed(self, seed, experiment, participant):
        return seed

    def summarize_trials(self, trials: list, experiment, participant) -> Dict[str, Any]:
        """
        Reads the new sliders settings from the trials and modifies the seed accordingly
        """
        # Get current seed
        seed = self.seed.copy()
        logger.info(f"Current overhead: {seed["overhead"]}")

        coordinator = self.get_coordinator(trials)
        overhead = coordinator.answer["overhead"]
        logger.info(f"Overhead found from coordinator: {overhead}")

        seed["overhead"] = overhead
        logger.info(f"New seed: {seed}")

        return seed

    def get_coordinator(self, trials):
        coordinator = [trial for trial in trials if 'coordinator' in str(trial).lower()]
        assert len(coordinator) == 1
        return coordinator[0]

##########################################################################################
# Experiment
##########################################################################################


def get_trial_maker():
    rater_class = SingleRateTrial
    n_creators = 1
    n_raters = 2

    seed_definition = {
        "overhead": 1,
        "positions": ["A", "B"],
        "assignments": dict(),
    }
    start_nodes = [
        CustomNode(context={"img_url": "static/dog.jpg"}, seed=seed_definition)
    ]

    return CreateAndRateTrialMaker(
        n_creators=n_creators,
        n_raters=n_raters,
        node_class=CustomNode,
        creator_class=CoordinatorTrial,
        rater_class=rater_class,
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
