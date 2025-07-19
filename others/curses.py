import threading
import time
import os

# Global variable to control the timer
timer_running = True

# Timer function
def countdown(seconds):
    global timer_running
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_format = f"{mins:02d}:{secs:02d}"
        print(f"\rTime left: {timer_format}", end="", flush=True)
        time.sleep(1)
    timer_running = False
    print("\nTime's up!")

# Main game function
def main_game():
    print("Game has started! Type 'exit' to end the game.")
    while timer_running:
        user_input = input("\nYour move: ")
        if user_input.lower() == 'exit':
            print("Exiting the game.")
            break
        # Process the user's input (game logic can be added here)
        print(f"You entered: {user_input}")

# Start the game with the countdown timer
def start_game_with_timer():
    timer_seconds = 10  # Set countdown time (in seconds)
    
    # Start the countdown timer in a separate thread
    timer_thread = threading.Thread(target=countdown, args=(timer_seconds,))
    timer_thread.start()
    
    # Start the main game loop
    main_game()

# Execute the game with the countdown timer
if __name__ == "__main__":
    start_game_with_timer()
