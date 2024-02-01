from datetime import datetime, timedelta
from collections import Counter
import re
import random

class Diary:
    FILE_NAME = "diary.entries.txt"

    def __init__(self):
        self.entries = []
        self.mood_data = []
        self.points = 0
        self.last_check_in_time = None
        self.load_from_file()

    def add_entry(self, entry, mood=None):
        # Add the entry to the list along with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mood_str = f"Mood: {mood}" if mood is not None else ""
        entry_with_mood = f"{timestamp} - {entry} - {mood_str}"

        # Append the entry with mood to the list
        self.entries.append(entry_with_mood)

        # Only track mood if mood is provided
        if mood is not None:
            self.track_mood(mood)

        # Save mood data to file after adding as entry
        self.save_mood_to_file()

    def view_entries(self):
        # Display all entries with timestamps
        for entry in self.entries:
            print(entry)

    def save_to_file(self, filename=None):
        # Save entries to a text file
        filename = filename or self.FILE_NAME
        try:
            with open(filename, 'w') as file:
                for entry in self.entries:
                    file.write(entry + '\n')
        except Exception as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self, filename=None):
        # Loads entries from a text file
        filename = filename or self.FILE_NAME
        try:
            with open(filename, 'r') as file:
                self.entries = [line.strip() for line in file]
        except FileNotFoundError:
            print(f"File not found: {filename}")
        except Exception as e:
            print(f"Error loading from file: {e}")

        # Load mood data from file
        self.load_mood_data()

    def search_entries(self, keyword):
        # Search for entries containing specific keywords
        matching_entries = [entry for entry in self.entries if keyword.lower() in entry.lower()]
        return matching_entries

    def get_analytics(self, num_entries=100, stop_words=None):
        total_entries = len(self.entries)
        word_count = sum(len(entry.split()) for entry in self.entries)
        recent_entries = ' '.join(self.entries[-num_entries:])
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', recent_entries).lower()
        words = cleaned_text.split()

        # Exclude stop words
        if stop_words:
            words = [word for word in words if word.lower() not in stop_words]

        word_counts = Counter(words)
        top_word, top_word_count = word_counts.most_common(1)[0] if word_count else ('N/A', 0)

        # Mood analysis
        average_mood = sum(self.mood_data) / len(self.mood_data) if self.mood_data else 0

        return total_entries, word_count, top_word, top_word_count, average_mood

    def track_mood(self, mood):
        try:
            mood_int = int(mood)
            if 1 <= mood_int <= 10:
                self.mood_data.append(mood_int)
            else:
                print("Mood should be between 1 and 10.")
        except ValueError:
            print("Invalid mood input. Please enter a number between 1 and 10.")

    def analyze_mood(self):
        if not self.mood_data:
            print("No mood data available.")
            return

        average_mood = sum(self.mood_data) / len(self.mood_data)

        print(f"Average Mood: {average_mood}")

    def save_mood_to_file(self, filename=None):
        filename = filename or "mood_data.txt"
        try:
            with open(filename, 'w') as file:
                for mood in self.mood_data:
                    file.write(str(mood) + '\n')
        except Exception as e:
            print(f"Error saving mood data to file: {e}")

    def load_mood_data(self, filename=None):
        filename = filename or "mood_data.txt"
        try:
            with open(filename, 'r') as file:
                self.mood_data = [int(line.strip()) for line in file]
        except FileNotFoundError:
            print(f"Mood data file not found: {filename}")
        except Exception as e:
            print(f"Error loading mood data from file: {e}")

    # Define a list of journal prompts
    JOURNAL_PROMPTS = [
        "Write about a goal you achieved recently and how it made you feel.",
        "Describe a memorable moment from today",
        "What are you grateful for right now?",
        "How did I feel today?",
        "What went well today?",
        "What was something I learned today?",
        "What was the most prominent emotion I felt today?",
        "What did you do today?",
        "What stands out most about your day?",
        "what's something you're proud of yourself for?",
        "List your wins from today",
        "What are my top three values and how do they guide my decisions?",
        "Describe a recent challenge I faced and what I learned from it",
        "What accomplishments am I most proud of in the last year?",
        "How do I handle stress, and what strategies can I use to improve?",
        "List three things I'm grateful for today.",
        "Reflect on a mistake I made and what lessons I gained from it.",
        "How do I define success for myself, and am I currently working towards it?",
        "What activities bring me the most joy and fulfillment?",
        "Describe a time when I stepped out of my comfort zone and grew from the experience.",
        "Reflect on a relationship in my life and how it impacts my well-being",
        "Identify one area of my life where I can practice more self-compassion",
        "How do I prioritize self-care, and what activities rejuvenate me?",
        "Explore a goal that aligns with my passions and interests"
    ]

    def get_random_prompt(self):
        # Gets a random journal prompt from the list
        return random.choice(self.JOURNAL_PROMPTS)

    def daily_check_in(self):
        # Checks if 24 hours have passed since last check-in
        current_time = datetime.now()
        if self.last_check_in_time is None or (current_time - self.last_check_in_time) >= timedelta(days=1):
            # Performs a daily check-in and updates points
            self.points += 10
            self.last_check_in_time = current_time
            print("Daily check-in complete. You earned 10 points!")
        else:
            print("You have already performed a daily check-in in the last 24 hours.")

    def add_entry_with_points(self, entry, mood=None):
        # Adds an entry and updates points
        self.add_entry(entry, mood)
        self.points += 2
        print("Entry added. You earned 2 points!")

    def get_points(self):
        return self.points

def main():
    diary = Diary()

    stop_words = ["the", "and", "i", "a", "is", "of", "in", "to", "that", "it", "for", "with", "on", "at", "by", "this", "today", "was", "lot"]

    while True:
        print("\n1. Add entry\n2. View Entries\n3. Search Entries\n4. Random Prompt\n5. View Analytics\n6. Daily Check-in\n7. Save and Exit")
        choice = input("Enter your choice (1/2/3/4/5/6/7): ")

        try:
            if choice == '1':
                entry = input("Enter your diary entry: ")
                mood = input("Enter your mood (1-10): ")
                diary.add_entry_with_points(entry, mood)  # Fix: Pass mood parameter
            elif choice == '2':
                print("\n---- Entries ----")
                diary.view_entries()
            elif choice == '3':
                keyword = input("Enter keyword to search: ")
                matching_entries = diary.search_entries(keyword)
                if matching_entries:
                    print("\n---- Matching Entries ----")
                    for entry in matching_entries:
                        print(entry)
                else:
                    print(f"No entries found containing '{keyword}'.")
            elif choice == "4":
                # Option to get a random journal prompt
                random_prompt = diary.get_random_prompt()
                print(f"\nRandom Journal Prompt: {random_prompt}")
                add_prompt = input("Would you like to add this prompt as an entry? (y/n): ")
                if add_prompt == 'y':
                    entry = input("Enter your diary entry: " )
                    diary.add_entry_with_points(f"{random_prompt}\n{entry}")  # Combines prompt and entry
            elif choice == "5":
                total_entries, word_count, top_word, top_word_count, average_mood = diary.get_analytics(num_entries=100, stop_words=stop_words)
                print(f"\nTotal Entries: {total_entries}\nTotal words: {word_count}")
                print(f"Top Used Word: '{top_word}' (Used {str(top_word_count)} times)")
                print(f"Average Mood: {average_mood}")
            elif choice == '6':
                diary.daily_check_in()
            elif choice == "7":
                diary.save_to_file()
                print("Diary saved. Exiting... ")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")
        except Exception as e:
            print(f"An error occurred: {e}")

    print(f"Total Points: {diary.get_points()}")

if __name__ == "__main__":
    main()
