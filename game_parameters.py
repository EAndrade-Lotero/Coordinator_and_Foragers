# Module with the game parameters
import numpy as np

NUM_FORAGERS = 2
POWER_ROLE = "coordinator"

WORLD_WIDTH = 250
WORLD_HEIGHT = 200
NUM_CENTROIDS = 13
NUM_COINS = 100
DISPERSION = 10

INITIAL_WEALTH = 700
LIST_OF_DISTRIBUTIONS = ["circular", "linear_up", "linear_down"]
INITIAL_POSITIONS = [(0,0), (WORLD_WIDTH, WORLD_HEIGHT)]

STARTING_SLIDERS = {
    "overhead":0.5,
    "wages":0.5,
    "prerogative":0.5
}

NUM_TRIALS_PER_PARTICIPANT = 2
MAX_NODES_PER_CHAIN = 10

WORLD_PATHS = [
    "static/assets/images/map1.json",
    "static/assets/images/map2.json",
    "static/assets/images/map3.json",
]

IMAGE_PATHS = {
    "coin_url": "static/assets/images/coin.png",
    "forager_url": "static/assets/images/forager.png",
}

RNG = np.random.default_rng(42)