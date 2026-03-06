# Module with the custom trialmaker

##########################################################################################
# Imports
##########################################################################################

from typing import List, Any
from markupsafe import Markup

from psynet.page import InfoPage
from psynet.timeline import PageMaker
from psynet.trial.create_and_rate import CreateAndRateTrialMakerMixin
from psynet.trial.imitation_chain import ImitationChainTrialMaker
from psynet.utils import get_logger

from .game_parameters import WORLD_PATHS
from .text_variables import STYLE

logger = get_logger()

###########################################
# TrialMaker class
###########################################

class CreateAndRateTrialMaker(CreateAndRateTrialMakerMixin, ImitationChainTrialMaker):
    response_timeout_sec = 500 # (200% of the estimated time)
    check_timeout_interval_sec = 500
    allow_revisiting_networks_in_across_chains = False
    give_end_feedback_passed = True

    def custom_network_filter(self, candidates, participant) -> List[Any]:
        """
        # Filter out networks with active trials
        """
        # logger.info(f"Active networks: {[(network.id, not self.has_active_trials(network)) for network in candidates]}")
        logger.info("Applying custom network filter...")
        # Exclude networks with active trials
        filtered_networks = [
            network for network in candidates
            if (
                not self.has_active_trials(network)
            )
        ]
        if len(filtered_networks) == 0:
            logger.info("WARNING: No active networks found")
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

    def _get_end_feedback_passed_logic(self):
        if self.give_end_feedback_passed:

            def f(participant):
                score = participant.module_state.performance_check["score"]
                return self.get_end_feedback_passed_page(score, participant.id)

            return PageMaker(f, time_estimate=5)
        else:
            return []

    def get_end_feedback_passed_page(self, score, participant_id):
        # Overriding participant_trials
        all_trials_as_coordinator = self.creator_class.query.filter_by(
            participant_id=participant_id
        ).all()
        all_trials_as_forager = self.rater_class.query.filter_by(
            participant_id=participant_id
        ).all()
        all_participant_trials = all_trials_as_coordinator + all_trials_as_forager
        logger.info(f"all trials: {[trial.id for trial in all_participant_trials]}")

        # Get scores from trials
        scores = []
        logger.info(f"Checking score from {len(all_participant_trials)} rounds...")
        for trial in all_participant_trials:
            try:
                score = int(trial.score)
                scores.append(score)
            except Exception as e:
                text = f"Incorrect score for trial {trial.id}: {trial.score}"
                text += f"\n{e}"
                logger.error(text)
                scores.append("Round failed")
        logger.info(f"Participant scores: {scores}")
        if len(scores) != len(WORLD_PATHS):
            logger.info(f"Warning: Number of scores does not match number of rounds ({len(scores)} != {len(WORLD_PATHS)})")

        final_score = sum([score for score in scores if isinstance(score, int)])
        score_to_display = "NA" if final_score is None else f"{int(final_score)}"

        reward_text = f"""
            {STYLE}
            <h1>Final score</h1>
            <p>Your final score is: {score_to_display}</p>
            <br>
            <p>Here is the score you obtained each round:</p>
        """

        for i, round_score in enumerate(scores):
            reward_text += f"<p>Round: {round_score}</p>"
            reward_text += "<br>"

        reward_text += """
        <p class="final-note">
        Note: Scores may not be listed in the proper order.
        </p>
        <br>
        <p class="final-note">
        If you are ready to continue, press the 'Next' button.
        </p>        
        """

        return InfoPage(
            Markup(reward_text),
            time_estimate=5,
        )
