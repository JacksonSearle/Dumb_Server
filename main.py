import json
import random
import time
from pathlib import Path

# List of 10 sentences describing daily tasks someone might do
daily_tasks = [
    "Going to the market.",
    "Cooking a meal.",
    "Reading a book.",
    "Cleaning the house.",
    "Taking a nap.",
    "Going for a walk.",
    "Meeting a friend.",
    "Practicing a hobby.",
    "Working out.",
    "Tending to the garden.",
]

# Read in all data from on_startup.json
with open(Path("game_info/on_startup.json"), "r") as f:
    on_startup = json.load(f)

# Read in all data from to_client.json
with open(Path("game_info/to_client.json"), "r") as f:
    to_client = json.load(f)

# Map the agents by their name for easier access
to_client_agents = {agent["name"]: agent for agent in to_client["agents"]}

# Load the data from to_server.json
with open(Path("game_info/to_server.json"), "r") as f:
    to_server = json.load(f)

while True:
    # Go through the 3 characters provided in to_server
    for agent in to_server["agents"]:
        # 1 in 10 chance (for each character) to change their destination
        if random.randint(1, 10) == 1:
            # Change their destination to a destination from on_startup.json
            new_destination = random.choice(on_startup["allDestinations"])
            agent["destination"] = new_destination
            to_client_agents[agent["name"]]["destination"] = new_destination

            # Change their status to a new sentence out of the 10 sentences
            new_status = random.choice(daily_tasks)
            to_client_agents[agent["name"]]["status"] = new_status

    # At the end of each update loop (which this is), write the changes to on_startup
    with open(Path("game_info/on_startup.json"), "w") as f:
        json.dump(on_startup, f, indent=2)

    # Write the changes to to_client.json
    with open(Path("game_info/to_client.json"), "w") as f:
        json.dump(to_client, f, indent=2)

    # Pause for 1 seconds
    time.sleep(1)
