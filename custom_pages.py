# Module with the custom pages
##########################################################################################
# Imports
##########################################################################################
from typing import Union, Optional

from markupsafe import Markup
from psynet.utils import get_logger
from psynet.timeline import FailedValidation
from psynet.modular_page import (
    ModularPage,
    Prompt,
    SliderControl,
)

from .text_variables import SLIDER_SETTING_TEXT

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
            n_steps: Optional[int] = 100,
    ) -> None:
        assert(dimension in ["overhead", "wages", "prerogative"]), f"Invalid dimension: {dimension}. Expected 'overhead', 'wages' or 'prerogative'"

        super().__init__(
            dimension,
            Prompt(
                text=Markup(SLIDER_SETTING_TEXT(dimension)),
            ),
            SliderControl(
                start_value=start_value,
                min_value=0,
                max_value=1,
                n_steps=n_steps,
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