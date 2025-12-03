# Module with the custom trialmaker

##########################################################################################
# Imports
##########################################################################################

from typing import List, Any

from psynet.trial.create_and_rate import CreateAndRateTrialMakerMixin
from psynet.trial.imitation_chain import ImitationChainTrialMaker
from psynet.utils import get_logger

logger = get_logger()

###########################################
# TrialMaker class
###########################################

class CreateAndRateTrialMaker(CreateAndRateTrialMakerMixin, ImitationChainTrialMaker):
    response_timeout_sec = 300 # (200% of the estimated time)
    allow_revisiting_networks_in_across_chains = False

    def custom_network_filter(self, candidates, participant) -> List[Any]:
        """
        # Filter out networks with active trials
        """
        logger.info("Applying custom network filter...")
        # Exclude networks with active trials
        filtered_networks = [
            network for network in candidates
            if (
                not self.has_active_trials(network)
            )
        ]
        return filtered_networks

    def has_active_trials(self, network: Any) -> bool:
        active_trials = [
            trial.id for trial in network.all_trials
            if (
                trial.finalized == False
                and trial.failed == False
            )
        ]
        return len(active_trials) > 0