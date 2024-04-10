# space_pirates_event.py
import random

class SpacePiratesEvent:
    def __init__(self, player):
        self.player = player

    def post_combat_victory(self):
        # Assuming the player gains resources and needs to make strategic decisions next
        self.player.add_score(10)  # Adjust score gain as needed
        self.player.update_state("strategic_planning")
        return ("Your crew's valiant efforts have fended off the pirate assault! With this victory, you can now focus on your mission's broader objectives.")

    def post_combat_defeat(self):
        self.player.add_score(-5)  # Adjust score penalty as needed.
        self.player.change_hp(-20)  # Apply damage to reflect the defeat.
        self.player.has_encountered_space_pirates = False  # Allow re-encountering pirates.

        self.player.update_state("recovery_phase")
        return ("Despite your best efforts, the pirates overwhelm your defenses. It's time to lick your wounds, repair the ship, and plan your next move.")

    def handle_event(self, user_input):
        lowered = user_input.lower()

        # Main encounter handler
        if self.player.state == "space_pirates":
            return self.space_pirates_encounter(lowered)
        # Other specific event states
        elif self.player.state == "pirates_combat":
            return self.pirates_combat(lowered)
        elif self.player.state == "pirates_hiding_success":
            return self.pirates_hiding_success()
        elif self.player.state == "pirates_hiding_failure":
            return self.pirates_hiding_failure()
        elif self.player.state == "high_success_help":
            return self.high_success_help()
        elif self.player.state == "partial_success_help":
            return self.partial_success_help()
        elif self.player.state == "failed_help":
            return self.failed_help()
        else:
            # Default message for any unhandled state
            return "The situation with the space pirates evolves in unexpected ways. How will you adapt? 'Stay on guard' or 'reassess your strategy'?"

    def space_pirates_encounter(self, user_input=None):
        # Depending on user_input, proceed to combat, hiding, or signaling for help
        if user_input:
            if "prepare" in user_input or "fight" in user_input:
                self.player.update_state("pirates_combat")
                return self.pirates_combat()
            elif "hide" in user_input or "attempt" in user_input:
                return self.attempt_hiding()
            elif "signal" in user_input or "help" in user_input:
                return self.signal_for_help()
            return "The space pirates are approaching. What's your plan?"
        # If no user_input (automatic progression), decide a random approach (combat/hide/help)
        # For demonstration, let's assume it chooses to hide
        return self.attempt_hiding()

    def signal_for_help(self):
        outcome = random.choices(
            ["high_success", "partial_success", "failure"],
            weights=[50, 30, 20],
            k=1
        )[0]

        if outcome == "high_success":
            self.player.update_state("high_success_help")
            return "Assistance arrives, driving the pirates away."
        elif outcome == "partial_success":
            self.player.has_encountered_space_pirates = False
            self.player.update_state("partial_success_help")
            return "A friendly ship provides some assistance, but the pirates are still a threat."
        elif outcome == "failure":
            self.player.has_encountered_space_pirates = False
            self.player.change_hp(-20)
            self.player.update_state("failed_help")
            return "No help arrives; the pirate ship is bearing down on you."

    def attempt_hiding(self):
        # Determine success or failure of hiding
        success = random.choice([True, False])
        if success:
            self.player.update_state("pirates_hiding_success")
            return self.pirates_hiding_success()
        self.player.update_state("pirates_hiding_failure")
        return self.pirates_hiding_failure()

    def pirates_combat(self, user_input=None):
        # Determine the outcome of combat
        combat_success = random.choice([True, False])
        if combat_success:
            self.player.update_state("post_combat_victory")
            return self.post_combat_victory()
        self.player.update_state("post_combat_defeat")
        return self.post_combat_defeat()

    def default_handler(self):
        # Handle any undefined states or unexpected paths
        return "An unexpected situation has arisen. How will you navigate this new challenge?"

    def pirates_hiding_success(self):
        self.player.add_score(5)  # Reward for successful evasion.
        self.player.update_state("strategic_planning")  # Transition to strategic planning.
        return (
            "Having successfully hidden from the pirates, you now have the opportunity to make strategic decisions. "
            "How will you proceed with your journey?")

    def pirates_hiding_failure(self):
        self.player.change_hp(-15)  # Penalty for failed hiding attempt.
        self.player.update_state("pirates_combat")  # Transition to combat state.
        return ("Your attempt to hide has failed; the pirates have detected your ship. Prepare for combat!")

    def high_success_help(self):
        self.player.add_score(10)
        self.player.update_state("beginning")
        return "With the help of arriving allies, you fend off the pirates."

    def partial_success_help(self):
        self.player.add_score(5)
        self.player.update_state("beginning")
        return "Assistance arrives, but the pirates are still a threat. You manage to escape with minor damage."

    def failed_help(self):
        self.player.change_hp(-20)
        self.player.update_state("beginning")
        return "Your calls for help go unanswered, and the pirate attack leaves your ship damaged."
