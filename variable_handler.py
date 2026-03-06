from psynet.utils import get_logger

logger = get_logger()


class VariableHandler:

    possible_levels = ["top", "trial"]
    debug = False

    def __init__(self, level: str = "top", use_vars: bool = False) -> None:
        assert level in self.possible_levels, f"Error: level should be one of {self.possible_levels} but got {level}."
        self.level = level
        self.use_vars = use_vars

    def get_value(self, participant, variable: str):
        if self.use_vars:
            return self.get_from_vars(participant, variable)
        else:
            return self.get_from_var(participant, variable)

    def get_from_var(self, participant, variable: str):
        data = self.get_data_at_level(participant)
        if data.has(variable):
            return getattr(participant.var, variable)
        else:
            return None

    def get_from_vars(self, participant, variable):
        data = self.get_data_at_level(participant)
        try:
            value = data[variable]
            return value
        except Exception as e:
            data[variable] = None
            if self.debug:
                logger.info(f"VariableHandler error ==> Variable {variable} doesn't exist in vars at level {self.level}")
            return None

    def get_data_at_level(self, participant):
        if self.use_vars:
            if self.level == "top":
                data = participant.vars
            elif self.level == "trial":
                data = participant.current_trial.vars
            else:
                raise NotImplementedError(f"Error: Level {self.level} not implemented!")
        else:
            if self.level == "top":
                data = participant.var
            elif self.level == "trial":
                data = participant.current_trial.var
            else:
                raise NotImplementedError(f"Error: Level {self.level} not implemented!")
        return data

    @staticmethod
    def get_value_from_last_answer(participant, page_label: str):
        last_answer = participant.answer_accumulators[-1]
        assert isinstance(last_answer, dict)
        assert page_label in last_answer.keys(), f"Error: page with label {page_label} is not in answers. Found only: {last_answer.keys()}"
        value = last_answer[page_label]
        return value

    @staticmethod
    def set_value_from_last_answer(participant, page_label: str, variable: str):
        value = VariableHandler.get_value_from_last_answer(participant, page_label)
        participant.current_trial.vars[variable] = value
