# Module with the custom node
##########################################################################################
# Imports
##########################################################################################
from typing import Dict, Any

from psynet.trial import ChainNode
from psynet.utils import get_logger
from psynet.trial.create_and_rate import CreateAndRateNodeMixin

logger = get_logger()

###########################################
# Custom node
###########################################

class CustomNode(CreateAndRateNodeMixin, ChainNode):

    def create_definition_from_seed(self, seed, experiment, participant):
        return seed

    def summarize_trials(self, trials: list, experiment, participant) -> Dict[str, Any]:
        """
        Reads the new sliders settings from the trials and modifies the seed accordingly
        """
        # Get current seed
        seed = self.seed.copy()

        # Get new sliders settings
        coordinator = self.get_coordinator(trials)
        overhead = coordinator.answer["overhead"]

        # Beget new setting
        seed["overhead"] = overhead,
        return seed

    def get_coordinator(self, trials):
        coordinator = [trial for trial in trials if 'coordinator' in str(trial).lower()]
        assert len(coordinator) == 1
        return coordinator[0]
