# pylint: disable=unused-import,abstract-method,unused-argument
##########################################################################################
# Imports
##########################################################################################
from markupsafe import Markup
from typing import Union, Dict

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

    def format_answer(self, raw_answer, **kwargs) -> Union[Dict[str, int], str]:
        try:
            answer ={"A": 1, "B":2}
            return answer
        except (ValueError, AssertionError) as e:
            logger.info(f"Error: {e}")
            return f"INVALID_RESPONSE"


class CreateTrial(CreateTrialMixin, ImitationChainTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):

        list_of_pages = [
            ModularPage(
                "assignments",
                animal_prompt(text="Describe the animal", img_url=self.context["img_url"]),
                DummyControl(),
                time_estimate=self.time_estimate,
            ),
            SliderSettingPage(
                dimension="overhead",
                start_value=0.5,
                time_estimate=self.time_estimate,
            ),
            CodeBlock(
                lambda participant: self.initialize_assigments(participant),
            )
        ]

        return list_of_pages

    def initialize_assigments(self, participant) -> None:
        assignments = {trial.id:None for trial in participant._current_trial.node.all_trials}
        participant._current_trial.node.vars["assignments"] = assignments


class SingleRateTrial(RateTrialMixin, ImitationChainTrial):
    time_estimate = 5

    def show_trial(self, experiment, participant):
        assert self.trial_maker.target_selection_method == "one"

        assert len(self.targets) == 1
        target = self.targets[0]
        answers = self.get_target_answer(target)

        logger.info(f"Answers (type={type(answers)}: {answers}")
        creation = answers["assignments"]

        logger.info(f"OKOKO{participant._current_trial.node.vars["assignments"]}")

        list_of_pages = [
            ModularPage(
                "rate_trial",
                animal_prompt(
                    text=f"How well does this description match the animal?<br><strong>{creation}</strong>",
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

    variables ={
        "assignments":dict()
    }

    pass
    # def summarize_trials(self, trials: list, experiment, participant) -> None:
    #     pass

##########################################################################################
# Experiment
##########################################################################################


def get_trial_maker():
    rater_class = SingleRateTrial
    n_creators = 1
    n_raters = 2
    rate_mode = "rate"
    include_previous_iteration = True
    target_selection_method = "one"

    seed_definition = {
        "overhead": 1,
        "assignments": dict(),
    }
    start_nodes = [
        CreateAndRateNode(context={"img_url": "static/dog.jpg"}, seed=seed_definition)
    ]

    return CreateAndRateTrialMaker(
        n_creators=n_creators,
        n_raters=n_raters,
        node_class=CustomNode,
        creator_class=CreateTrial,
        rater_class=rater_class,
        # mixin params
        include_previous_iteration=include_previous_iteration,
        rate_mode=rate_mode,
        target_selection_method=target_selection_method,
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
