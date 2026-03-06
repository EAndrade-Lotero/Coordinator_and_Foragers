import json
import numpy as np
from typing import Dict

try:
    from .tiles3 import IHT, tiles
except:
    from tiles3 import IHT, tiles

class TilesQ:
    """
    Defines a tile coding linear approximation.
    Input:
        - numDims (int), number of dimensions of the continuous state space
        - numTilings (int), the number of tilings. Should be a power of 2, e.g., 16.
        - numTiles (list), a list with the number of tiles per dimension
        - scaleFactors (list), a list with the normalization factor per dimension
        - maxSize (int), the max number of tiles
        - weights (list), the list of weights
    """
    def __init__(self, parameters :Dict):
        self.numDims = parameters["numDims"]
        self.numTilings = parameters["numTilings"]
        self.numTiles = parameters["numTiles"]
        self.scaleFactors = parameters["scaleFactors"]
        self.alpha = parameters["alpha"]
        self.maxSize = parameters["maxSize"]
        self.iht = IHT(self.maxSize)
        self.weights = np.zeros(self.maxSize, dtype=np.float32)
        self.active_tiles = []
        self.dummy_action = 0

    def my_tiles(self, state):
        """
        Determines the tiles that get activated by the state
        """
        # Normalizes the state
        scaled_s = self.normalize(state)
        # Rescale for use with `tiles` using numTiles
        rescaled_s = [scaled_s[i ] *self.numTiles[i] for i in range(self.numDims)]
        self.active_tiles = tiles(self.iht, self.numTilings, rescaled_s, [self.dummy_action])
        return self.active_tiles

    def predict(self, state):
        """
        Returns the sum of the weights corresponding to the active tiles
        """
        return sum([self.weights[tile] for tile in self.my_tiles(state)])

    def learn(self, state, update):
        """
        Updates its weights.
        """
        estimate = self.predict(state)
        error = update - estimate
        # Gradient is 1 only for active tiles and 0 otherwise
        # Thus only updates weights of active tiles
        assert(isinstance(self.weights, np.ndarray))
        self.weights[self.active_tiles] += self.alpha * error

    def normalize(self, state):
        """
        Normalizes state. Should perform the following iteration
        scaled_s = []
        for i, scale in enumerate(self.scaleFactors):
            x = scale(state[i], scale["min"], scale["max"])
            scaled_s.append(x)
        I use list comprehension to optimize speed
        """
        def re_scale(x, min_, max_):
            return (x - min_) / (max_ - min_)

        return [re_scale(state[i], scale["min"], scale["max"]) for i, scale in enumerate(self.scaleFactors)]

    def save(self, file :str) -> None:
        json_dump = {
            'weights': self.weights.tolist(),
            'dictionary': {
                self.iht.dictionary[key] :key for key in self.iht.dictionary.keys()
            },
            'overfull_count' :self.iht.overfullCount
        }
        json_object = json.dumps(json_dump, indent=4)
        # Writing to file
        with open(file, "w") as outfile:
            outfile.write(json_object)
        outfile.close()

    def load(self, file :str) -> None:
        self.active_tiles = []
        with open(file, 'r') as openfile:
            # Reading from file
            json_dump = json.load(openfile)
        self.weights = np.array(json_dump['weights'], dtype=np.float32)
        self.iht = IHT(self.maxSize)
        self.iht.dictionary = json_dump['dictionary']
        self.iht.dictionary = {tuple(self.iht.dictionary[key]) :int(key) for key in self.iht.dictionary.keys()}
        self.iht.overfullCount = json_dump['overfull_count']
        openfile.close()

num_actions = 11 # Discretize commission rate in ten bins
state_scales = [
    {'min':0.0, 'max':1.0}, # For commission rate
]
tiles_parameters = {
    'numDims': 1, # commission rate
    'numTilings': 3,
    'numTiles': [3],
    'scaleFactors':state_scales,
    'maxSize':4096,
    'alpha':0.1,
}
common_pool = TilesQ(
    parameters=tiles_parameters,
)