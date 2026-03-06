# Module with the custom node
##########################################################################################
# Imports
##########################################################################################
from typing import Dict, Any

from psynet.trial import ChainNode
from psynet.utils import get_logger
from psynet.trial.create_and_rate import CreateAndRateNodeMixin

from .game_parameters import (
    POWER_ROLES,
    RNG,
)

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

        power_role = self.participant_group
        assert power_role in POWER_ROLES

        if power_role == "coordinator":
            # Get new sliders settings
            coordinator = self.get_coordinator(trials)
            overhead = coordinator.vars["overhead"]
        elif power_role == "forager":
            forager_trials = self.get_foragers(trials)
            overheads = [trial.vars["overhead"] for trial in forager_trials]
            forager_id = RNG.choice(len(forager_trials))
            overhead = overheads[forager_id]
            self.vars["power_forager_id"] = forager_id
            logger.info(f"Power was given to forager {forager_id}")
        else:
            raise NotImplementedError

        # Transmit overhead
        seed["sliders"]["overhead"] = overhead

        return seed

    def get_coordinator(self, trials):
        coordinator = [
            trial for trial in trials
            if (
                    'coordinator' in str(trial).lower()
                    and "node" not in str(trial).lower()
            )
        ]
        assert len(coordinator) == 1
        return coordinator[0]

    def get_foragers(self, trials):
        forager_trials = [
            trial for trial in trials
            if (
                    trial.finalized == True
                    and trial.failed == False
                    and "forager" in str(trial).lower()
                    and "node" not in str(trial).lower()
            )
        ]
        return forager_trials
