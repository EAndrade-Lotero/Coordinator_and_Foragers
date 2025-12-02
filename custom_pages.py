# Module with the custom pages
##########################################################################################
# Imports
##########################################################################################
from typing import Union

from psynet.utils import get_logger
from psynet.timeline import FailedValidation

from psynet.modular_page import (
    ModularPage,
    Prompt,
    SliderControl,
)

logger = get_logger()

###########################################
# Custom pages
###########################################

class SliderSettingPage(ModularPage):
    def __init__(
            self,
            dimension: str,
            start_value: float,
            time_estimate: float,
    ) -> None:
        assert(dimension in ["overhead", "wages", "prerogative"]), f"Invalid dimension: {dimension}. Expected 'overhead', 'wages' or 'prerogative'"

        information_text = f'''
        You can modify the parameters of the social contract established so far.
        This is the place to modify the {dimension} parameter.
        HERE THE EXPLANATION.
        The slider below displays the current level of {dimension}. Please move it to match your desired level of {dimension}.
        '''
        assert(dimension in ["overhead", "wages", "prerogative"]), f"Invalid dimension: {dimension}. Expected 'overhead', 'wages-commission', 'prerogative'."

        super().__init__(
            dimension,
            Prompt(
                text=information_text,
            ),
            SliderControl(
                start_value=start_value,
                min_value=0,
                max_value=1,
                n_steps=100,
            ),
            time_estimate=time_estimate,
            save_answer=dimension
        )

    def format_answer(self, raw_answer, **kwargs) -> Union[float, str]:
        try:
            new_value = float(raw_answer)
            return new_value
        except (ValueError, AssertionError) as e:
            logger.info(f"Error: {e}")
            return f"INVALID_RESPONSE"

    def validate(self, response, **kwargs) -> Union[FailedValidation, None]:
        logger.info(f"Validating...")
        if response.answer == "INVALID_RESPONSE":
            logger.info(f"Invalid response!")
            return FailedValidation(f"This failed for some reason.")
        logger.info(f"Validated!")
        return None