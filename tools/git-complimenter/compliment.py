import json
import random
import os

COMPLIMENTS_PATH = os.path.expanduser("~/Research/hub/iconocracy-corpus/tools/git-complimenter/compliments.json")

def get_compliment():
    with open(COMPLIMENTS_PATH, "r") as f:
        compliments = json.load(f)
    return random.choice(compliments)

if __name__ == "__main__":
    print(f"\n--- ICONOCRACY: {get_compliment()} ---\n")
