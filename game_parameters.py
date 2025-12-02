# Module with the game parameters
import numpy as np

NUM_FORAGERS = 2
POWER_ROLE = "coordinator"

NUM_CENTROIDS = 2
NUM_COINS = 100
DISPERSION = 10

INITIAL_WEALTH = 100
LIST_OF_DISTRIBUTIONS = ["linear"]
INITIAL_POSITIONS = ["A", "B"]

STARTING_SLIDERS = {
    "overhead":0.5,
    "wages":0.5,
    "prerogative":0.5
}

NUM_TRIALS_PER_PARTICIPANT = 2
MAX_NODES_PER_CHAIN = 10

IMAGE_PATHS = {
    "img_url": "static/positioning.png",
    "map_url": "static/map.png",
    "coin_url": "static/coin.png",
    "forager_url": "static/forager.png",
}

RNG = np.random.default_rng(42)