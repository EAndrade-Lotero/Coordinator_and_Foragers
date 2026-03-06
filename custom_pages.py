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
)

from .text_variables import (
    SLIDER_SETTING_TEXT,
    SATISFACTION_TEXT,
)
from .custom_front_end import CustomSliderControl

logger = get_logger()

###########################################
# Custom pages
###########################################

class SliderSettingPage(ModularPage):
    def __init__(
            self,
            label: str,
            dimension: str,
            time_estimate: float,
            start_value: Optional[float] = 0.0,
            min_value: Optional[float] = 0.0,
            max_value: Optional[float] = 1.0,
            n_steps: Optional[int] = 100,
            use_percentage: Optional[bool] = False,
            left_label: Optional[str] = "",
            right_label: Optional[str] = "",
            integer_rule: Optional[bool] = False,
    ) -> None:
        assert(dimension in ["overhead", "wages", "prerogative"]), f"Invalid dimension: {dimension}. Expected 'overhead', 'wages' or 'prerogative'"

        if use_percentage:
            min_value = 0.0
            max_value = 1.0

        super().__init__(
            label=label,
            prompt=Prompt(
                text=Markup(SLIDER_SETTING_TEXT(dimension)),
            ),
            control=CustomSliderControl(
                start_value=start_value,
                min_value=min_value,
                max_value=max_value,
                n_steps=n_steps,
                use_percentage=use_percentage,
                left_label=left_label,
                right_label=right_label,
                integer_rule=integer_rule,
            ),
            time_estimate=time_estimate,
            save_answer=dimension
        )
        self.dimension = dimension

    def format_answer(self, raw_answer, **kwargs) -> Union[float, str]:
        try:
            new_value = float(raw_answer)
            return new_value
        except (ValueError, AssertionError) as e:
            text = f"Error in slider with dimension {self.dimension}"
            text += f"\nIncorrect answer {raw_answer}: {raw_answer}"
            text += f"\n{e}"
            logger.info(text)
            return f"INVALID_RESPONSE"

    def validate(self, response, **kwargs) -> Union[FailedValidation, None]:
        logger.info(f"Validating...")
        if response.answer == "INVALID_RESPONSE":
            logger.info(f"Invalid response!")
            return FailedValidation(f"This failed for some reason.")
        logger.info(f"Validated!")
        return None


class SatisfactionPage(ModularPage):

    def __init__(self) -> None:
        super().__init__(
            "well-being",
            Prompt(Markup(SATISFACTION_TEXT)),
            CustomSliderControl(
                start_value=0.5,
                min_value=0.0,
                max_value=1,
                n_steps=100,
                use_percentage=True,
                right_label="%",
            ),
            time_estimate=15,
        )