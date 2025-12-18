# Helper classes to be used in the experiment
import PIL
import json
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from numpy.typing import NDArray
from matplotlib.offsetbox import (
    AnnotationBbox,
    OffsetImage
)
from typing import (
    List, Tuple, Dict, Iterable,
    Optional, Union, Any
)

from psynet.utils import get_logger

logger = get_logger()

try:
    # Assume running from psynet
    from .game_parameters import (
        WORLD_WIDTH,
        WORLD_HEIGHT,
        NUM_COINS,
        NUM_CENTROIDS,
        DISPERSION,
        NUM_FORAGERS,
        INITIAL_WEALTH,
        RNG,
    )
except:
    # If not, try normal import
    from game_parameters import (
        WORLD_WIDTH,
        WORLD_HEIGHT,
        NUM_COINS,
        NUM_CENTROIDS,
        DISPERSION,
        NUM_FORAGERS,
        INITIAL_WEALTH,
        RNG,
    )


class World:
    """2D grid world with coins placed according to a distribution.

    Grid cells contain 1 if a coin is present, otherwise 0.
    """
    width: Optional[int] = WORLD_WIDTH
    height: Optional[int] = WORLD_HEIGHT
    coin_path: Path = None
    map_path: Path = None
    forager_path = None
    num_foragers: int = NUM_FORAGERS
    _rng = RNG
    max_percentage_of_coins = 1

    def __init__(
        self,
        num_coins: int,
        num_centroids: int,
        distribution: str,
        dispersion: float,
    ) -> None:
        logger.info(f"Initializing world...")
        # Check width and height
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive.")
        self.grid = np.zeros((self.height, self.width))
        logger.info(f"Grid of dimensions: {self.grid.shape} created...")
        # Check number of coins
        coin_percentage = num_coins / (self.width * self.height)
        assert coin_percentage > 0, f"Error, number of coins should be greater than 0, bu got {num_coins}"
        assert coin_percentage < self.max_percentage_of_coins, f"Error: percentage of coins in world should not be greater than {self.max_percentage_of_coins}, bu got {coin_percentage}"
        logger.info(f"Percentage of map with coins: {coin_percentage}")
        self.num_coins = num_coins
        # Check centroids
        self.num_centroids = num_centroids
        # Check distribution
        assert(distribution in ["linear_up", "linear_down", "circular", "oval"]), f"Dispersion {distribution} not supported. Choose from ['linear', 'circular', 'oval']."
        self.distribution = distribution
        # Check dispersion
        assert(dispersion > 0), f"Dispersion must be greater than 0 (but got {dispersion})."
        self.dispersion = dispersion
        logger.info("Placing coins...")
        self._place_coins()

    @staticmethod
    def generate_from_json(path: Path) -> "World":
        with open(path, "r") as f:
            coins = json.load(f)
        world = World.generate_from_coins(coins)
        world.map_path = path
        return world

    @staticmethod
    def generate_from_coins(
        coins: List[Tuple[int, int]],
    ) -> "World":
        world_parameters = {
            "num_coins": NUM_COINS,
            "num_centroids": NUM_CENTROIDS,
            "dispersion": DISPERSION,
            "distribution": "linear"
        }
        world = World(**world_parameters)
        world.clear()
        xs, ys = zip(*coins)
        rows = np.array(ys)
        cols = np.array(xs)
        world.grid[rows, cols] = 1
        return world

    def place_given_coins(self, coins: List[Tuple[int, int]]) -> None:
        xs, ys = zip(*coins)
        rows = np.array(ys)
        assert(np.all(rows < self.height))
        cols = np.array(xs)
        assert(np.all(cols < self.width))
        self.grid[rows, cols] = 1

    def coin_positions(self) -> List[Tuple[int, int]]:
        """List of (row, col) positions where coins are present."""
        rc = np.argwhere(self.grid == 1)  # (row, col)
        coin_positions = [(int(c), int(r)) for r, c in rc]  # (x, y)
        return coin_positions

    def save_world(self) -> None:
        json.dump(self.coin_positions(), open(self.map_path, "w"))

    def count_coins(self) -> int:
        """Return the number of coins currently placed."""
        return self.grid.sum()

    def clear(self) -> None:
        """Remove all coins (set all cells to 0)."""
        self.grid = np.zeros((self.height, self.width))

    def _place_coins(self) -> None:
        """Create and place coins."""
        self.clear()
        if self.num_coins == 0:
            return

        coins_per_centroid = self.num_coins // self.num_centroids
        offset = self.count_coins() - coins_per_centroid * self.num_centroids
        coins_per_centroid = [coins_per_centroid for _ in range(self.num_centroids)]
        if offset > 0:
            coins_per_centroid[-1] += offset

        centroids = self.get_centroids()
        for i, (x, y) in enumerate(centroids):
            n_coins = coins_per_centroid[i]
            sample_coins = self.sample_bivariate_normal(
                mean=(x, y),
                cov=((self.dispersion, 0), (0, self.dispersion)),
                n=n_coins,
            )
            coords_x = [int(x) for x, y in sample_coins]
            coords_y = [int(y) for x, y in sample_coins]
            self.grid[coords_y, coords_x] = 1

        # Add random coins
        coins = self.create_random_coins(0.01)
        self.place_given_coins(coins)

    def get_centroids(self) -> List[Tuple[int, int]]:
        """Return the centroids of coins placed."""
        if self.num_centroids == 1:
            return [(int(self.width / 2), int(self.height / 2))]

        if self.distribution == "linear_down":
            sample = np.linspace(0, 1, self.num_centroids + 2)[1:-1]
            sample = [(int(x * self.width), int(x * self.height)) for x in sample]
            return sample

        if self.distribution == "linear_up":
            sample = np.linspace(0, 1, self.num_centroids + 2)[1:-1]
            sample = [(int(x * self.width), self.height - int(x * self.height)) for x in sample]
            return sample

        elif self.distribution == "circular":
            sample = np.linspace(0, 1, self.num_centroids + 1)[:-1]
            theta = (2.0 * np.pi) * sample
            x = np.cos(theta).tolist()
            y = np.sin(theta).tolist()
            sample = list(zip(x, y))

            x_scale = 0.25 * self.width
            y_scale = 0.25 * self.height
            sample = [(x * x_scale, y * y_scale) for x, y in sample]
            sample = [(x + 0.5 * self.width, y + 0.5 * self.height) for x, y in sample]
            sample = [(int(x), int(y)) for x, y in sample]
            return sample

        elif self.distribution == "oval":
            raise NotImplementedError("oval dispersion is not yet implemented.")

        else:
            raise NotImplementedError(f"Dispersion {self.distribution} not supported. Choose from ['linear', 'circular', 'oval'].")

    def create_random_coins(self, p:float) -> List[Tuple[int, int]]:
        """Create random coins."""
        assert(0 <= p <= 1)
        coins = []
        for x in range(self.width):
            for y in range(self.height):
                if self._rng.random() < p:
                    coins.append((x, y))
        return coins

    def __str__(self) -> str:
        """ASCII representation: '1' for coin, '.' for empty."""
        lines = []
        for r in range(self.height):
            line = "".join("1" if self.grid[r][c] else "." for c in range(self.width))
            lines.append(line)
        return "\n".join(lines)

    def render(
        self,
        bg=(0, 0, 0, 0),
        fg = (255, 255, 255, 255)
    ):
        # ) -> List[List[List[int, int, int]]]:
        """
        Convert a 2D binary-like array into an RGBA image array.

        Accepts mask shaped as (height, width) or (width, height).
        Returns shape (height, width, 4) with dtype uint8.
        """
        mask = np.asarray(self.grid)

        # Accept either (height, width) or (width, height)
        if mask.shape == (self.height, self.width):
            m = mask
        elif mask.shape == (self.width, self.height):
            m = mask.T
        else:
            raise ValueError(
                f"mask shape {mask.shape} doesn't match "
                f"(height,width)=({self.height},{self.width}) or (width,height)=({self.width},{self.height})"
            )

        m = m.astype(bool)

        rgba = np.empty((self.height, self.width, 4), dtype=np.uint8)
        rgba[:] = np.array(fg, dtype=np.uint8)
        rgba[m] = np.array(bg, dtype=np.uint8)

        return rgba

    def render_(
        self,
        show: bool = False,
        coin_zoom: float = 0.1,
        coin_percentage: Optional[float] = 1,
    ) -> NDArray[np.uint8]:
        """Render the world by drawing coin images at coin positions.

        Args:
            :param coin_zoom: Relative size of the coin inside a cell (0<zoom<=1).
            :param show: If True, also display the figure.
            :param coin_percentage: Probability of drawing a coin.
        """
        if not (0 < coin_zoom <= 1.0):
            raise ValueError("coin_zoom must be in (0, 1].")

        # Canvas sized roughly to grid, independent of DPI
        fig, ax = plt.subplots(
            # figsize=(int(self.width / 10), int(self.height / 10)),
            figsize=(1,1),
            dpi=100
        )

        # Light cell grid
        ax.set_xticks(np.arange(-.5, self.width, 1), minor=True)
        ax.set_yticks(np.arange(-.5, self.height, 1), minor=True)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        # ax.set_title("World", pad=8)
        ax.set_axis_off()

        # Load coin image (RGBA supported)
        raw_coin_img = plt.imread(self.coin_path)
        coin_img = OffsetImage(raw_coin_img, zoom=coin_zoom)

        # Place the coin image centered in each occupied cell
        half = 0.5 * coin_zoom
        coins = self.coin_positions()
        for (r, c) in coins:
            if self._rng.random() < coin_percentage:
                coin_img.image.axes = ax
                ab = AnnotationBbox(
                    coin_img,
                    (c + half, r + half),
                    frameon=False
                )
                ax.add_artist(ab)

        # Render the figure to a buffer
        fig.canvas.draw()
        # Convert to a NumPy array (RGBA)
        rgba_bytes = fig.canvas.buffer_rgba().tobytes()
        width, height = fig.canvas.get_width_height()
        pil_image = PIL.Image.frombytes(mode="RGBA", size=[width, height], data=rgba_bytes)
        img = np.array(pil_image)

        if show:
            plt.show()
        plt.close(fig)

        return img

    def sample_bivariate_normal(
        self,
        mean: Iterable[float],
        cov: Iterable[Iterable[float]],
        n: int,
    ) -> List[Tuple[float, float]] | NDArray[np.float64]:
        """
        Sample n points from a 2D (bivariate) normal distribution.

        Parameters
        ----------
        n : int
            Number of samples.
        mean : Iterable[float]
            Length-2 mean vector [mu_x, mu_y].
        cov : Iterable[Iterable[float]]
            2x2 covariance matrix [[var_x, cov_xy], [cov_yx, var_y]].

        Returns
        -------
        List[Tuple[float, float]] | NDArray[np.float_]
            The sampled coordinates.
        """
        mean_arr = np.asarray(mean, dtype=float)
        cov_arr = np.asarray(cov, dtype=float)

        samples: NDArray[np.float64] = self._rng.multivariate_normal(
            mean=mean_arr,
            cov=cov_arr,
            size=n
        )

        return [tuple(row) for row in samples]

    def get_probability_of_view(
        self,
        x:float,
        threshold:Optional[float]=0.8,
        steepness:Optional[float]=12.0,
    ) -> float:
        return 1.0 / (1.0 + np.exp(-steepness * (x - threshold)))

    def coordinator_view(self, information_investment:float) -> List[float]:
        # Initiate view
        terrain = np.ones((self.height, self.width)) * 140
        # Draw coins that are randomly selected to be seen according to investment
        for (x, y) in self.coin_positions():
            # Determine probability of view given investment
            p = self.get_probability_of_view(information_investment)
            if self._rng.random() < p:
                terrain[y, x] = 255
        return terrain.tolist()

    def generate_rgba_array(self, b=180, a_even=255, a_odd=140) -> List[float]:
        coords = self.coin_positions()
        xs, ys = zip(*coords)
        rows = np.array(ys)
        cols = np.array(xs)
        terrain = np.ones((self.height, self.width)) * a_odd
        terrain[rows, cols] = a_even
        return terrain.tolist()

    def generate_terrain(self) -> NDArray[np.int32]:
        coords = self.coin_positions()
        xs, ys = zip(*coords)
        rows = np.array(ys)
        cols = np.array(xs)
        terrain = self._rng.integers(220, 255, size=(self.height, self.width))
        terrain[rows, cols] = 0

        # Check coin positions are 0
        coin_checks = [terrain[y, x] == 0 for x, y in coords]
        assert(np.all(coin_checks))

        return terrain.tolist()


class WealthTracker:
    """Keeps track of the coins throughout iterations"""

    def __init__(self, n_coins:Optional[int]=INITIAL_WEALTH) -> None:
        self.n_coins = n_coins
        self.num_foragers: int = NUM_FORAGERS
        self.coordinator_wealth: Union[float, None] = None
        self.foragers_wealth: Union[List[float], None] = None

    def update_from_trials(self, trials: List[Any], sliders: Dict[str, float]) -> None:
        forager_trials = [t for t in trials if 'forager' in str(t).lower()]
        assert len(forager_trials) == self.num_foragers

        # Get forager production in previous episode
        foragers_payoffs = self.get_coins_from_foragers(forager_trials)
        self.n_coins = sum(foragers_payoffs)
        foragers_proportions = np.array(foragers_payoffs) / self.n_coins

        logger.info(f"Foragers collected {self.n_coins} coins in total last round.")
        logger.info(f"Foragers proportions: {foragers_proportions}")

        # Get slider parameters
        assert("overhead" in sliders.keys()), f"Error: sliders has to have an 'overhead' key (observed keys are{sliders.keys()}) )."
        assert("wages" in sliders.keys()), f"Error: sliders has to have an 'wages' key (observed keys are{sliders.keys()}) )."
        overhead = sliders["overhead"]
        wages_proportion = sliders["wages"]

        # Calculate coordinator's wealth
        self.coordinator_wealth = overhead * self.n_coins
        remaining = self.n_coins - self.coordinator_wealth

        # Calculate foragers' wealth
        wages = remaining * wages_proportion
        remaining = remaining - wages
        foragers_split = foragers_proportions * remaining
        self.foragers_wealth = wages + foragers_split

    def get_coins_from_foragers(self, trials: List[Any]) -> NDArray[np.float64]:
        foragers_payoffs = []
        for trial in trials:
            answers = self.get_coins(trial)
            logger.info(f"{str(trial)} => {answers}")
            foragers_payoffs.append(answers)
        return np.array(foragers_payoffs)

    def get_coins(self, trial: Any) -> int:
        logger.info(f"{hasattr(trial, "vars['coins_foraged']")}")
        return 10

    def initialize(self, sliders: Dict[str, float]) -> None:
        # Get slider parameters
        wages_proportion = sliders["wages"]

        # Calculate coordinator's wealth
        coordinator_wealth = self.calculate_coordinator_reward(sliders)

        remaining = self.n_coins - self.coordinator_wealth

        # Calculate foragers' wealth
        wages = remaining * wages_proportion
        remaining = remaining - wages
        foragers_split = np.array([remaining / self.num_foragers]) * self.num_foragers
        self.foragers_wealth = wages + foragers_split

    def calculate_coordinator_reward(self, sliders: Dict[str, float]) -> float:
        # Get slider parameters
        overhead = sliders["overhead"]
        self.coordinator_wealth = overhead * self.n_coins
        return self.coordinator_wealth

    # def calculate_foragers_reward(self, slider: SliderValues) -> float:


    def get_coordinator_wealth(self) -> float:
        assert(self.coordinator_wealth is not None), "Coordinator wealth is not set yet. Run update() first."
        return self.coordinator_wealth

    def get_forager_wealth(self, forager_id: int) -> float:
        assert(self.foragers_wealth is not None), "Forager wealth is not set yet. Run update() first."
        return self.foragers_wealth[forager_id]


class RewardProcessing:
    """Processes rewards and gives feedback"""

    @staticmethod
    def get_reward_text(
        n_coins: int,
        slider: Any,
        trial_type: str
    ) -> str:
        trial_types = ["coordinator"] + [f"forager-{i}" for i in range(NUM_FORAGERS)]
        assert(trial_type in trial_types), f"Invalid trial type. Expected one of {trial_types} but got {trial_type}."

        # Get
        accumulated_wealth = WealthTracker(n_coins)
        accumulated_wealth.initialize(slider)

        if trial_type == "coordinator":
            wealth = accumulated_wealth.get_coordinator_wealth()
        elif trial_type.startswith("forager"):
            forager_id = trial_type.split("-")[1]
            forager_id = int(forager_id)
            wealth = accumulated_wealth.get_forager_wealth(forager_id)
        else:
            raise ValueError(f"Invalid trial type: {trial_type}. Expected one of {trial_types}.")

        reward_text = f"The total number of coins collected on the previous iteration is {n_coins}.\n\n"
        reward_text += f"Based on the existing contract, you received {wealth} coins.\n\n"
        return reward_text
