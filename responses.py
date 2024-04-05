# responses.py
import random
from random import choice

# Import the SpacePiratesEvent class from the separate file
from space_pirates_event import SpacePiratesEvent

class Player:
    def __init__(self):
        self.state = "beginning"
        self.score = 0  # Initialize score
        self.hp = 100  # Initialize HP
        self.has_encountered_space_pirates = False  # To ensure the event triggers only once

    def update_state(self, new_state):
        print(f"Updating state from {self.state} to {new_state}")  # Debugging
        self.state = new_state

    def add_score(self, points):
        self.score += points

    def change_hp(self, hp_change):
        self.hp += hp_change
        if self.hp > 100:
            self.hp = 100
        elif self.hp <= 0:
            self.reset_player()

    def reset_player(self):
        self.hp = 100
        self.score = 0  # Reset score
        self.state = "beginning"  # Reset state
        self.has_encountered_space_pirates = False  # Reset this flag upon player reset
        print("Mission failed. Your score has been reset.")

    def get_status(self):
        return f"HP: {self.hp}, Score: {self.score}"

class DialogueManager:
    def __init__(self):
        self.dialogues = {
            "beginning": {
                "message": "You stand at the helm of your spaceship, the vast universe sprawling out before you. How will you begin your journey?",
                "choices": ["Set a course toward the distant star system", "Navigate through the nebulous region",
                            "Chart a path along the trade routes"]
            },
            "exploring": {
                "message": "You're now navigating through uncharted space, where every asteroid and nebula could hold untold secrets or unforeseen dangers.",
                "choices": ["Continue exploring", "Return to base", "Analyze your findings"]
            },
            "analyzing": {
                "message": "You've collected valuable data from your recent explorations. How will you analyze these findings to benefit your mission?",
                "choices": ["Analyze the asteroid's core samples", "Examine the alien artifact",
                            "Investigate the strange signals"]
            },
            "scanning": {
                "message": "The ship's scanners are active, peeling back the layers of space to reveal the resources and mysteries hidden within.",
                "choices": ["Scan the nearby sector.", "Perform a deep space survey.", "Initiate a detailed threat scan."]
            },
            "interacting": {
                "message": "Contact has been made. Whether it's a distress signal or an unknown entity, your decisions here could have significant repercussions.",
                "choices": ["Respond to the signal", "Proceed with caution", "Avoid the encounter"]
            },
            "repairing": {
                "message": "The constant wear and tear on the ship necessitate regular maintenance. Your choices could determine the efficiency and safety of your vessel.",
                "choices": ["Complete the repairs", "Upgrade the ship", "Conduct a thorough maintenance check"]
            },
            "trading": {
                "message": "Trade negotiations are underway. Your diplomatic skills could yield valuable resources or forge crucial alliances.",
                "choices": ["Negotiate a better deal", "Accept the current offer", "Decline and explore other options"]
            },
            "diplomacy": {
                "message": "Your diplomatic acumen is put to the test as you engage with other factions or civilizations. The outcomes could shape your journey.",
                "choices": ["Forge an alliance", "Negotiate peace", "Seek trade opportunities"]
            },
            "researching": {
                "message": "The data you've gathered is ripe for analysis, promising to unlock new technologies or reveal secrets of the cosmos.",
                "choices": ["Analyze the data", "Share the findings", "Conduct further research"]
            },
            "mining": {
                "message": "Resource extraction is crucial for your survival and the mission's success. How you manage this task could have lasting effects.",
                "choices": ["Harvest the resources", "Search for more valuable materials",
                            "Evaluate the potential risks"]
            },
            "checking": {
                "message": "The wellbeing of your crew is paramount. Regular check-ins are vital for morale and the mission's success.",
                "choices": ["Conduct a health and morale check", "Initiate a team-building exercise",
                            "Address any crew concerns"]
            },
            "negotiating": {
                "message": "In the vast expanse of space, negotiation is a valuable tool. Engaging with other entities could lead to alliances or conflicts.",
                "choices": ["Discuss a potential alliance", "Negotiate a cease-fire", "Engage in trade negotiations"]
            },
            "strategic_planning": {
                "message": "With the pirate threat neutralized, you gather resources from the debris. It's time to make strategic decisions for your next move. ",
                "choices": [
                    "Enhance your ship",
                    "Explore new territories",
                    "Consolidate your resources"
                ],
            },
            "deep_space_exploration": {
                "message": "The cosmos beckons with mysteries and wonders. As you delve into the depths of space, what marvels will you uncover?",
                "choices": [
                    "Investigate the drifting space station",
                    "Navigate the temporal rift",
                    "Explore the mysterious nebula"
                ],
            },
            "cosmic_anomaly_encounter": {
                "message": "A baffling cosmic anomaly has been detected. How will you interact with this mysterious phenomenon?",
                "choices": [
                    "Enter the dimensional gateway",
                    "Observe the collapsing star from a safe distance",
                    "Attempt to harness energy from the cosmic artifact"
                ],
            },
            "anomaly_aftermath": {
                "message": "The encounter with the cosmic anomaly has left its mark. How will you proceed in the wake of these events?",
                "choices": [
                    "Analyze the knowledge and artifacts obtained from the gateway",
                    "Study the data collected from the collapsing star",
                    "Stabilize your ship's systems affected by the quantum fluctuations"
                ],
            },
            "strategic_decision_point": {
                "message": "You've reached a pivotal moment in your journey. As the cosmos stands still, reflecting on your achievements, you realize the vastness of your accomplishments. This marks a pause in your exploration, a chance to bask in the glory of your successes and to dream of future endeavors. Your journey is far from over, but at this juncture, let's take a moment to reflect and prepare for the next chapter.",
                "choices": [
                    "Review your achievements and status",
                    "Prepare for future adventures (Reset the game)",
                    "Celebrate and rest (End the session)"
                ],
            },
            "recovery_phase": {
                "message": "Your ship has suffered damage, and the crew's morale is low. It's crucial to address these issues before continuing your journey.",
                "choices": [
                    "Conduct repairs on the ship",
                    "Focus on boosting crew morale",
                    "Send a distress signal for assistance"
                ],
            },
        }

    def get_dialogue(self, player_state):
        dialogue = self.dialogues.get(player_state)
        if dialogue:
            return {"message": dialogue["message"], "choices": dialogue["choices"]}
        else:
            return {"message": "You find yourself at a crossroads. Choose your path.", "choices": []}

player = Player()
dialogue_manager = DialogueManager()
space_pirates_event = SpacePiratesEvent(player)

def simple_hash(synonym, outcomes_count):
    # A simple hash function: sum ASCII values and mod by number of outcomes
    return sum(ord(char) for char in synonym) % outcomes_count

def get_response(user_input: str) -> str:
    lowered = user_input.lower().split()

    # Trigger the space pirates event if the score threshold is reached, the event hasn't occurred yet, and the player has at least 20 health
    if player.score >= 20 and not player.has_encountered_space_pirates and player.hp >= 20:
        player.update_state("space_pirates")
        player.has_encountered_space_pirates = True  # Ensure the event only triggers once

    # If the current state involves the space pirates event, delegate handling to the SpacePiratesEvent class
    if player.state in ["space_pirates", "pirates_combat", "pirates_hiding_success", "pirates_hiding_failure"]:
        return space_pirates_event.handle_event(user_input)

    # Handling responses based on the player's current state
    if player.state == "strategic_decision_point":
        user_choice = user_input.lower()
        if "review" in user_choice:
            return f"Your current status: HP: {player.hp}, Score: {player.score}."
        elif "prepare" in user_choice or "reset" in user_choice:
            player.reset_player()
            return "You decide to prepare for new adventures. The cosmos resets, but your experience remains. When you're ready, new challenges await."
        elif "celebrate" in user_choice or "rest" in user_choice:
            return "You take a moment to rest and celebrate your achievements. The universe will hold more adventures when you return."

    # Define actions with potential outcomes
    actions = {
        "set_course": {
            "synonyms": ["set", "course", "navigate", "chart", "plot", "path"],
            "valid_states": ["beginning"],
            "points": [1, 2, 3],  # Assigning minimal points as it's the beginning of the game.
            "hp_change": [0, 0, 0],  # No HP change for setting a course.
            "consequences": [
                "You set a course toward a distant star system, rumored to hold untold riches and dangers.",
                "Navigating through a nebulous space region, you chart a path filled with potential scientific discoveries.",
                "Plotting a course along the trade routes, you prepare for encounters with other spacefarers and potential trading opportunities."
            ],
            "next_state": "exploring"  # Leads to the exploration phase.
        },
        "explore": {
            "synonyms": ["explore", "exploring", "investigate", "analyze", "findings", "probe"],
            "valid_states": ["exploring"],
            "points": [6, 4, 2],
            "hp_change": [0, 5, 5],
            "consequences": [
                "You venture deeper into uncharted territories, discovering new celestial phenomena.",
                "You return to your base to regroup and plan your next move, ensuring your ship is prepared for further adventures.",
                "You take time to analyze the data collected during your explorations, uncovering valuable insights."
            ],
            "next_state": "analyzing"
        },
        "scan": {
            "synonyms": ["scan", "survey", "examine", "inspect"],
            "valid_states": ["scanning"],
            "points": [10, 5, 0],
            "hp_change": [10, 5, -10],
            "consequences": [
                "A benign anomaly is detected during the scan, enhancing your ship's capabilities."
                "Your survey located a derelict spacecraft. It's a goldmine of technology waiting to be explored.",
                "The scanning process attracts attention from nearby pirates. You fend them off but not without some trouble.",

            ],
            "next_state": "mining"
        },
        "check": {
            "synonyms": ["check", "monitor", "assess", "evaluate"],
            "valid_states": ["checking"],
            "points": [2, 1, 3],
            "hp_change": [-5, 0, 5],
            "consequences": [
                "Upon checking, you find the crew's spirits are low, necessitating some morale-boosting activities.",
                "The crew is doing well, everything is running smoothly on board.",
                "A crew member presents an innovative idea to improve ship efficiency, boosting everyone's spirits."
            ],
            "next_state": "repairing"
        },
        "repair": {
            "synonyms": ["repair", "repairs", "upgrade", "enhance", "fix", "mend", "restore"],
            "valid_states": ["repairing"],
            "points": [2, 3, 4],
            "hp_change": [5, 10, 15],
            "consequences": [
                "Quick fixes are made to the ship, ensuring it remains spaceworthy for the next part of your journey.",
                "You conduct a thorough overhaul of the ship, enhancing its performance for upcoming challenges.",
                "The repair session reveals an opportunity for a significant upgrade, fortifying your ship beyond its original state."
            ],
            "next_state": "exploring"
        },
        "trade": {
            "synonyms": ["negotiate", "barter", "decline", "no", "accept"],
            "valid_states": ["trading"],
            "points": [4, 3, 5],
            "hp_change": [0, -5, 5],
            "consequences": [
                "Your trading skills net you some valuable assets for your journey into the unknown.",
                "A misunderstanding during the trade talks leads to a tense moment, but you manage to salvage the deal.",
                "An exceptionally favorable trade gives you access to resources that significantly enhance your mission."
            ],
            "next_state": "checking"
        },
        "negotiate": {
            "synonyms": ["negotiate", "confer", "discuss", "ally"],
            "valid_states": ["negotiating"],
            "points": [5, 3, 2],
            "hp_change": [0, 0, -10],
            "consequences": [
                "Your diplomatic efforts forge a new alliance, opening up promising avenues for exploration and trade.",
                "The negotiations are tough, but you manage to secure a deal that keeps your mission on track.",
                "Diplomatic tensions rise, leading to a challenging situation that tests your resolve and strategic acumen."
            ],
            "next_state": "trading"
        },
        "analyze": {
            "synonyms": ["analyze", "asteroid", "examine", "investigate", "research"],
            "valid_states": ["analyzing"],
            "points": [6, 4, 2],
            "hp_change": [0, -5, -10],
            "consequences": [
                "Your analysis of the asteroid's core samples reveals a new form of energy-efficient fuel, sparking excitement among the crew.",
                "While examining the alien artifact, a hidden compartment opens, unveiling ancient technology that could advance your ship's capabilities.",
                "Investigating the strange signals from a nearby planet leads to a minor system glitch, causing some temporary setbacks."
            ],
            "next_state": "scanning"
        },
        "mine": {
            "synonyms": ["mine", "extract", "harvest", "excavate"],
            "valid_states": ["mining"],
            "points": [3, 2, 5],
            "hp_change": [-5, 0, 10],
            "consequences": [
                "Mining operations are tough, with some unexpected challenges, but the rewards are tangible.",
                "Your harvesting efforts proceed without a hitch, securing the resources needed for your journey.",
                "An abundance of resources is found, significantly bolstering your mission's prospects."
            ],
            "next_state": "interacting"
        },
        "interact": {
            "synonyms": ["interact", "communicate", "engage", "respond"],
            "valid_states": ["interacting"],
            "points": [3, 2, 1],
            "hp_change": [0, -5, 5],
            "consequences": [
                "You open a channel of communication with an unknown entity, which turns out to be friendly, sharing valuable information.",
                "You attempt to interact with a foreign object, but it triggers a defense mechanism, slightly damaging the ship.",
                "Your interaction yields a new alliance, offering resources and support for your mission."
            ],
            "next_state": "negotiating"
        },
        "strategic_planning": {
            "synonyms": ["enhance", "plan", "strategize", "organize", "prepare"],
            "valid_states": ["strategic_planning"],
            "points": [7, 5, 4],  # Enhanced point rewards
            "hp_change": [5, 10, 0],  # Minimized HP loss and enhanced HP gains
            "consequences": [
                "Your strategic planning uncovers a hidden cache of alien technology, offering advanced upgrades for your ship. The potential for new capabilities is immense.",
                "Intensive preparations lead to a significant breakthrough in your ship's defense systems, providing a substantial increase in durability and combat readiness.",
                "While reviewing your resources, you discover a forgotten artifact on board, promising unknown benefits or insights."
            ],
            "next_state": "deep_space_exploration"
        },
        "deep_space_exploration": {
            "synonyms": ["explore", "venture", "investigate", "discover"],
            "valid_states": ["deep_space_exploration"],
            "points": [6, 4, 3],  # Slightly less than strategic_planning but still rewarding
            "hp_change": [0, 5, -5],  # Mixed outcomes with potential for both gain and minor loss
            "consequences": [
                "You encounter a drifting space station of unknown origin. Inside, you find advanced technology and a map to a distant, uncharted galaxy.",
                "An anomaly in space leads you to a temporal rift. Navigating through, your ship gains unique insights into the cosmos, enhancing your knowledge and equipment.",
                "While exploring a nebula, you inadvertently awaken an ancient cosmic entity. Its intentions are unclear, but its power is undeniable."
            ],
            "next_state": "cosmic_anomaly_encounter"  # Leads to various potential scenarios
        },
        "cosmic_anomaly_encounter": {
            "synonyms": ["investigate", "enter", "observe", "harness", "energy", "approach", "analyze", "examine"],
            "valid_states": ["cosmic_anomaly_encounter"],
            "points": [4, 6, 2],  # Varied points reflecting the risks and rewards
            "hp_change": [0, -10, 5],  # Potential risk or minor health gain
            "consequences": [
                "The anomaly turns out to be a gateway to a parallel dimension. Exploring it offers unique resources but with unknown risks.",
                "Upon closer examination, the anomaly is a collapsing star about to go supernova. Evacuating in time avoids disaster but forfeits valuable data.",
                "The anomaly is an ancient cosmic artifact emitting mysterious energy. Harnessing this energy could enhance your ship's capabilities."
            ],
            "next_state": "anomaly_aftermath"  # Transition to dealing with the aftermath of the choice
        },
        "anomaly_aftermath": {
            "synonyms": ["reflect", "analyze", "knowledge", "study", "data", "stabilize", "consequence", "outcome"],
            "valid_states": ["anomaly_aftermath"],
            "points": [3, 2, 5],  # Reflecting a range of outcomes based on the choice made
            "hp_change": [5, 0, -5],  # Health adjustments based on the nature of the aftermath
            "consequences": [
                "Having navigated the dimensional gateway, you emerge with advanced knowledge and artifacts, but the journey has taken a toll on your crew's health.",
                "The observation of the collapsing star provides valuable data for your mission, though you regret missing out on closer exploration.",
                "The energy harnessed from the cosmic artifact boosts your ship's systems, but the process unleashes a series of unpredictable quantum fluctuations."
            ],
            "next_state": "strategic_decision_point"  # Leading back to a decision-making juncture
        },
        "strategic_decision_point": {
            "synonyms": ["decide", "plan", "strategize", "choose"],
            "valid_states": ["strategic_decision_point"],
            "points": [2, 3, 4],  # Points reflecting strategic thinking and planning
            "hp_change": [0, 0, 0],  # No health change, focusing on strategy
            "consequences": [
                "After thorough analysis, you decide to delve deeper into uncharted territories, seeking out the mysteries of the universe.",
                "Choosing to consolidate your resources, you focus on strengthening your ship and crew, preparing for future challenges.",
                "You opt to make contact with a nearby civilization, hoping to forge alliances or gather information beneficial to your mission."
            ],
            "next_state": "new_exploration_phase"  # Transition to a new phase of exploration or interaction
        },
        "recovery_phase": {
            "synonyms": ["repair", "boost", "assess"],
            "valid_states": ["recovery_phase"],
            "points": [2, 2, 2],
            "hp_change": [10, 0, 0],
            "consequences": [
                "Your ship is repaired and systems are upgraded, making you ready for whatever lies ahead.",
                "The crew's morale is boosted, strengthening their resolve for future encounters.",
                "Resources are optimized, enhancing your preparedness for upcoming challenges."
            ],
            "next_state": "exploring"  # Return to a state where encountering pirates again is possible if defeated.
        },
    }

    lowered_words = user_input.lower().split()
    action_taken = False
    consequence = ""
    hp_change = 0
    points = 0
    new_dialogue = None

    for action, details in actions.items():
        if player.state in details["valid_states"]:  # Check if the action is valid in the current state
            matched_synonym = next((keyword for keyword in details["synonyms"] if keyword in lowered_words), None)
            if matched_synonym:
                action_taken = True

                index = simple_hash(matched_synonym, len(details['consequences']))
                consequence = details['consequences'][index]
                hp_change = details['hp_change'][index]
                points = details['points'][index]

                player.update_state(details["next_state"])
                player.add_score(points)
                player.change_hp(hp_change)

                new_dialogue = dialogue_manager.get_dialogue(player.state)
                print(f"New state: {player.state}, Dialogue: {new_dialogue}")
                break

    if action_taken:
        if player.hp <= 0:
            player.reset_player()
            return "Your actions have led to critical system failures, and the mission comes to a sudden end."
        else:
            # Format the response to include the consequence, player stats, and new dialogue message.
            # Then, present the choices on a new line for clear visibility.
            response = f"{consequence} You earned {points} points. HP: {player.hp}, Score: {player.score}.\n\n"
            response += f"{new_dialogue['message']}\nChoices: {' | '.join(new_dialogue['choices'])}"
            return response

        # Default response if no action is taken
    if not action_taken:
        # Check if the user is asking for their status
        if "status" in lowered_words:
            return player.get_status()

        # Greeting responses - now checking for exact matches
        greetings = ["hello", "hi", "hey", "greetings"]
        greeting_responses = ["Hello there!", "Hi! How can I assist you today?", "Hey! What's up?",
                              "Greetings, traveler!"]
        if any(greeting in lowered_words for greeting in greetings):
            return random.choice(greeting_responses)

        # Farewell responses - also checking for exact matches
        farewells = ["bye", "goodbye", "farewell", "see you", "later"]
        farewell_responses = ["Goodbye! Stay safe on your journey.", "Farewell! Come back soon.", "See you later!"]
        if any(farewell in lowered_words for farewell in farewells):
            return random.choice(farewell_responses)

        # Help responses
        help_keywords = ["help", "assist", "support"]
        help_response = "Need some help? Check out #welcome-and-rules for guidance or post your query in #feedback for more assistance!"
        if any(help_word in lowered_words for help_word in help_keywords):
            return help_response

    # Default response if no specific action, greeting, farewell, or help keyword is recognized
    default_dialogue = dialogue_manager.get_dialogue(player.state)
    return f"{default_dialogue['message']}\nChoices: {' | '.join(default_dialogue['choices'])}"

