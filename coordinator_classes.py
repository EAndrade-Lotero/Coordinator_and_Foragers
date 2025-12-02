# Module with the coordinator classes

##########################################################################################
# Imports
##########################################################################################
from markupsafe import Markup
# from typing import (
#     Any, Union, List, Dict
# )

from psynet.utils import get_logger
from psynet.timeline import (
    # CodeBlock,
    for_loop,
)
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
            ModularPage(
                "positions",
                Prompt(text="This is a dummy positioning page"),
                PushButtonControl(
                    choices=INITIAL_POSITIONS,
                    labels=["Next"],
                    arrange_vertically=False,
                ),
                time_estimate=self.time_estimate,
            ),
            for_loop(
                label="slider_setting",
                iterate_over=lambda: ["overhead", "wages", "prerogative"],
                logic=lambda parameter: SliderSettingPage(
                    dimension=parameter,
                    start_value=participant._current_trial.definition["sliders"][parameter],
                    time_estimate=self.time_estimate,
                ),
                time_estimate_per_iteration=5,
            ),
        ]

        return list_of_pages


# class CoordinatorTrial(CreateTrialMixin, ImitationChainTrial):
#     time_estimate = 5
#     accumulate_answers = True
#
#     def show_trial(self, experiment, participant) -> List[Any]:
#
#         logger.info(f"Participant {participant.id} has the role COORDINATOR")
#
#         list_of_pages = [
#             # Greetings
#             InfoPage("""HERE THE INSTRUCTIONS"""),
#             # Asks coordinator to invest
#             InvestingPage(time_estimate=self.time_estimate),
#             # Asks the coordinator to assign foragers to positions
#             ModularPage(
#                 "forager_positions",
#                 HelloPrompt(
#                     username="Coordinator",
#                     text=Markup(
#                         """
#                         <h3>Position foragers</h3>
#                         <p>Please position all the foragers on the map below.</p>
#                         """
#                     )
#                 ),
#                 PositioningControl(
#                     world=participant._current_trial.definition["world"],
#                     context=self.context,
#                     investment=participant.answer.get("investment"),
#                 ),
#                 time_estimate=self.time_estimate,
#             ),
#             # Informs the reward
#             InfoPage(
#                 RewardProcessing.get_reward_text(
#                     n_coins=participant._current_trial.definition["wealth"],
#                     slider=participant._current_trial.definition["sliders"],
#                     trial_type="coordinator"
#                 ),
#                 time_estimate=5
#             ),
#             # WellBeingReportPage(
#             #     time_estimate=self.time_estimate,
#             # ),
#             #
#             for_loop(
#                 label="slider_setting",
#                 iterate_over=lambda: ["overhead", "wages"],
#                 logic=lambda parameter: SliderSettingPage(
#                     dimension=parameter,
#                     start_value=participant._current_trial.definition["sliders"][parameter],
#                     time_estimate=self.time_estimate,
#                 ),
#                 time_estimate_per_iteration=5,
#             ),
#             CodeBlock(
#                 lambda participant: self.set_node_state(participant),
#             )
#         ]
#         return list_of_pages
#
#     def set_node_state(self, participant) -> None:
#         """
#         Initializes the foragers ids to be taken by subsequent forager trials
#         """
#         forager_positions = participant.answers["forager_positions"]
#         assignments = {
#             forager_id: None for forager_id in forager_positions.keys()
#         }
#         participant._current_trial.vars.assignments = assignments
#
#     def set_node_investment(self, participant) -> None:
#         investment = participant.answers["investment"]
#         assert(investment is not None)
#         participant._current_trial.vars.investment = investment
#
#     def format_answer(self, raw_answer, **kwargs) -> Union[Dict[str, Any], str]:
#         logger.info(f"Formatting the coordinator trial answer: {raw_answer}")
#         try:
#             assert(isinstance(raw_answer, dict))
#             assert('assign_foragers' in raw_answer.keys())
#             assert('overhead' in raw_answer.keys())
#             return raw_answer
#         except (ValueError, AssertionError):
#             return f"INVALID_RESPONSE"

###########################################