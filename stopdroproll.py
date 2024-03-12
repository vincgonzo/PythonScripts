from pwn import *
import time

# challenge answer script to CybersecurityChallenge HTB 2024 Game 

def play_game():
    with remote("94.237.48.219", 57833) as r:
        # Start the game
        r.recvuntil("Are you ready? (y/n)")
        r.sendline("y")

        r.recvuntil("Ok then! Let's go!")
        log.info("Game started!")

        first_iteration = True
        while True:
            #if not first_iteration:
            #    r.recvuntil("What do you do? ")
            # Receive scenario(s) from the game
            scenarios = r.recvline().decode().strip()
            if not scenarios:
                log.info("Empty scenarios. Skipping...")
                continue
            log.info(f"\nReceived scenarios: {scenarios}")
            # Process the scenarios and send the appropriate responses
            responses = process_scenarios(scenarios)
            log.info(f"Sending responses: {responses}")
            r.sendline(responses)

            # Check if the flag is received
            if "HTB" in responses:
                log.success("Congratulations! Flag received.")
                break

            first_iteration = False

def process_scenarios(scenarios):
    # Truncate scenarios after encountering "What do you do? "
    scenarios = scenarios.replace("What do you do? ", "").strip()

    # Process scenarios and generate responses
    responses = []
    for scenario in scenarios.split(", "):
        # Handle multiple lines in scenarios
        scenario = scenario.splitlines()[0].strip()

        if scenario == "GORGE":
            responses.append("STOP")
        elif scenario == "PHREAK":
            responses.append("DROP")
        elif scenario == "FIRE":
            responses.append("ROLL")

    return "-".join(responses)

if __name__ == "__main__":
    play_game()

