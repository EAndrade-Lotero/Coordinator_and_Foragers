# Module with the coordinator classes

##########################################################################################
# Imports
##########################################################################################
from markupsafe import Markup
# from typing import (
#     Any, Union, List, Dict
# )

from psynet.page import InfoPage
from psynet.utils import get_logger
# from psynet.timeline import (
#     for_loop,
# )
from psynet.modular_page import (
    ModularPage,
    Prompt,
    PushButtonControl,
    SliderControl,
)
from psynet.trial.create_and_rate import CreateTrialMixin
from psynet.trial.imitation_chain import ImitationChainTrial

from .custom_pages import (
    SliderSettingPage,
)
from .game_parameters import INITIAL_POSITIONS
from .text_variables import COORDINATOR_INSTRUCTIONS

logger = get_logger()

###########################################
# Coordinator classes
###########################################


########################
# Pages

class InvestingPage(ModularPage):
    def __init__(
            self,
            time_estimate: float,
    ) -> None:

        information_text = Markup("""
        <h3>Investing for information</h3>
        <p>You have to invest a percentage of your endowment to obtain information about the location of the resources.
        The percentage you invest corresponds to the probability that each coin is shown in your map.
        Move the slider to determine the percentage of your endowment that you want to invest.</p>
        """)
        super().__init__(
            "investment",
            Prompt(
                text=information_text,
            ),
            SliderControl(
                start_value=0.5,
                min_value=0,
                max_value=1,
                n_steps=100,
            ),
            time_estimate=time_estimate,
        )

    def format_answer(self, raw_answer, **kwargs) -> str:
        try:
            investment = float(raw_answer)
            logger.info(f"------> The coordinator invests: {investment*100}%")
            return raw_answer
        except (ValueError, AssertionError) as e:
            logger.info(f"Error: {e}")
            return f"INVALID_RESPONSE"


########################
# Trial

class CoordinatorTrial(CreateTrialMixin, ImitationChainTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):

        list_of_pages = [
            InfoPage(
                Markup(COORDINATOR_INSTRUCTIONS),
                time_estimate=5
            ),
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
            ),
            SliderSettingPage(
                dimension="wages",
                start_value=self.get_slider_value(participant, "wages"),
                time_estimate=self.time_estimate,
            ),
            SliderSettingPage(
                dimension="prerogative",
                start_value=self.get_slider_value(participant, "prerogative"),
                time_estimate=self.time_estimate,
            ),
            # for_loop(
            #     label="slider_setting",
            #     iterate_over=lambda: ["overhead", "wages", "prerogative"],
            #     logic=lambda parameter: SliderSettingPage(
            #         dimension=parameter,
            #         start_value=self.get_slider_value(participant, parameter),
            #         time_estimate=self.time_estimate,
            #     ),
            #     time_estimate_per_iteration=5,
            # ),
        ]

        return list_of_pages

    def get_slider_value(self, participant, parameter) -> float:
        value = participant._current_trial.definition["sliders"][parameter]
        if isinstance(value, tuple):
            value = value[0]
        assert isinstance(value, float), f"Error: expected float, got {type(value)} --- ({value=})."
        return value


