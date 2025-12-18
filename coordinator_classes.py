# Module with the coordinator classes

##########################################################################################
# Imports
##########################################################################################
from markupsafe import Markup
from typing import Union

from psynet.page import InfoPage
from psynet.utils import get_logger
from psynet.modular_page import (
    ModularPage,
    Prompt,
    SliderControl,
)
from psynet.trial.create_and_rate import CreateTrialMixin
from psynet.trial.imitation_chain import ImitationChainTrial
from psynet.timeline import CodeBlock

from .custom_pages import (
    SliderSettingPage,
)
from .custom_front_end import PositioningControl
from .text_variables import (
    COORDINATOR_INSTRUCTIONS,
    INVESTMENT_INSTRUCTIONS,
    POSITIONING_INSTRUCTIONS,
    SCORE_TEXT,
    WELL_BEING_TEXT,
)
from .helper_classes import RewardProcessing

logger = get_logger()

###########################################
# Coordinator classes
###########################################


########################
# Pages

########################
# Trial

class CoordinatorTrial(CreateTrialMixin, ImitationChainTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):

        list_of_pages = [
            # Greetings
            InfoPage(
                Markup(COORDINATOR_INSTRUCTIONS),
                time_estimate=5
            ),
            # Asks coordinator to invest
            ModularPage(
                "investment",
                Prompt(Markup(INVESTMENT_INSTRUCTIONS)),
                SliderControl(
                    start_value=self.set_start_value_investment(participant),
                    min_value=0.0,
                    max_value=0.85,
                    n_steps=86,
                ),
                time_estimate=self.time_estimate,
            ),
            # Propagate investment value
            CodeBlock(
                lambda participant: self.set_investment(participant),
            ),
            # Asks the coordinator to assign foragers to positions
            ModularPage(
                "positions_and_coins",
                Prompt(Markup(POSITIONING_INSTRUCTIONS)),
                PositioningControl(
                    world_path=participant.current_trial.definition["world_path"],
                    context=self.context,
                    investment=participant.current_trial.vars["investment"] # self.get_investment(participant),
                ),
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
                    start_value=0.0,
                    min_value=0.0,
                    max_value=1,
                    n_steps=100,
                ),
                time_estimate=self.time_estimate,
            ),
            # Tweak sliders
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
                n_steps=3,
            ),
        ]

        return list_of_pages

    def set_start_value_investment(self, participant) -> float:
        default_value = 0.0
        try:
            investment = participant.current_trial.vars["investment"]
        except:
            investment = default_value
            participant.current_trial.vars["investment"] = default_value
        return investment

    def set_investment(self, participant):
        last_answer = participant.answer_accumulators[-1]
        assert isinstance(last_answer, dict)
        assert "investment" in last_answer.keys()
        investment = last_answer["investment"]
        assert (isinstance(investment, Union[int, float])), f"Error: answer investment should be float but got {type(investment)}"
        investment = float(investment)
        logger.info(f"Setting investment to {investment}")
        participant.current_trial.vars["investment"] = float(investment)

    def get_investment(self, participant) -> float:
        try:
            investment = participant.current_trial.vars["investment"]
            investment = float(investment)
            logger.info(f"Ok, I see investment is {investment}")
            return investment
        except:
            logger.exception("Something went wrong. Current trial doesn't have an investment.")
            raise KeyError

    def get_slider_value(self, participant, parameter) -> float:
        value = participant.current_trial.definition["sliders"][parameter]
        if isinstance(value, tuple):
            value = value[0]
        assert isinstance(value, float), f"Error: expected float, got {type(value)} --- ({value=})."
        return value

    def get_reward_text(self, participant) -> Markup:
        n_coins = participant.current_trial.definition["n_coins"]
        sliders = participant.current_trial.definition["sliders"]
        text = RewardProcessing.get_reward(
            n_coins=n_coins,
            sliders=sliders,
            trial_type="coordinator",
        )
        text = SCORE_TEXT(text)
        return Markup(text)