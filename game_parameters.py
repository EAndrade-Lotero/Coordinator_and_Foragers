# Module with the game parameters
import numpy as np

NUM_FORAGERS = 2
POWER_ROLE = "coordinator"

WORLD_WIDTH = 15
WORLD_HEIGHT = 10
NUM_CENTROIDS = 1
NUM_COINS = 5
DISPERSION = 1

INITIAL_WEALTH = 3
LIST_OF_DISTRIBUTIONS = ["linear"]
INITIAL_POSITIONS = ["A", "B"]

STARTING_SLIDERS = {
    "overhead":0.5,
    "wages":0.5,
    "prerogative":0.5
}

NUM_TRIALS_PER_PARTICIPANT = 2
MAX_NODES_PER_CHAIN = 10

WORLD_PATHS = [
    "static/assets/images/map.json"
]

IMAGE_PATHS = {
    "coin_url": "static/assets/images/coin.png",
    "forager_url": "static/assets/images/forager.png",
}

RNG = np.random.default_rng(42)