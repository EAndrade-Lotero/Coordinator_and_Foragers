# module with the texts as variables to be used in the respective pages
try:
    from .game_parameters import (
        NUM_FORAGERS,
        WORLD_PATHS,
        ASSETS_PATHS,
        REWARD_SCALING_FACTOR,
        MAX_BONUS_REWARD,
    )
except:
    from game_parameters import (
        NUM_FORAGERS,
        WORLD_PATHS,
        ASSETS_PATHS,
        REWARD_SCALING_FACTOR,
        MAX_BONUS_REWARD,
    )

############################################################
# Format

DESCRIPTION = "Participants divide labor to maximize number of foraged coins and tweak the parameters of the social contract."

STYLE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome to the coordinator and foragers game!</title>
    <style>
        body {
            font-family: "Book Antiqua", "Palatino Linotype", Palatino, serif;
            font-size: 14pt;
            line-height: 1.5;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            background-color: #f5ecd9;
            background-image:
                radial-gradient(circle at top left, rgba(0,0,0,0.06), transparent 60%),
                radial-gradient(circle at bottom right, rgba(0,0,0,0.06), transparent 60%);
        }

        h1 {
            text-align: center;
            font-size: 2em;
            margin-bottom: 0.2em;
        }

        h2 {
            margin-top: 1.8em;
            margin-bottom: 0.4em;
            font-size: 1.3em;
        }

        p {
            margin: 0.4em 0;
            text-align: justify;
        }

        ul {
            margin: 0.4em 0 0.4em 1.5em;
        }

        li {
            margin: 0.2em 0;
        }

        .formula-block {
            margin: 0.6em 0 0.8em 1.5em;
            font-family: "Courier New", Courier, monospace;
        }

        .final-note {
            margin-top: 2em;
            font-weight: bold;
        }
    </style>
</head>
<body>

"""

TWO_COLUMN_STYLE = """
  <style>
    .two-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      align-items: start;
      max-width: 800px;
      margin: 0 auto;
      padding: 24px;
    }

    .col {
      border: 1px solid #ddd;
      border-radius: 12px;
      padding: 16px;
    }

    .col img {
      width: 100%;
      height: auto;
      display: block;
      border-radius: 10px;
      margin-bottom: 12px;
    }

    /* Stack on small screens */
    @media (max-width: 800px) {
      .two-col { grid-template-columns: 1fr; }
    }
  </style>
"""


THREE_COLUMN_STYLE = """
  <style>
    .three-cols {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;              /* space between columns */
    }

    .col3 {
      padding: 12px;
    }
  </style>
"""


############################################################
# Welcome text

WELCOME_TEXT_1 = f"""
    {STYLE}

    <h1>Welcome to the coordinator and foragers game!</h1>

    <h2>Overview</h2>
    <p>
        The purpose of this game is to collectively forage as many coins as possible from the ground.
    </p>
    <img src={ASSETS_PATHS["foraging_url"]} alt="Two foragers moving around the world" width=400px/>
    <p>
        In this game, you will be playing as one of two roles. A forager, who collects coins from the ground;
        or a coordinator, who coordinates the foragers’ efforts by assigning them to a favorable foraging ground.
    </p>    
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>
</body>
</html>
"""

WELCOME_TEXT_2 = f"""
    {STYLE}

    {TWO_COLUMN_STYLE}

    <h1>Welcome to the coordinator and foragers game!</h1>

    <h2>Roles</h2>
    
      <section class="two-col">
    <div class="col">
      <h2>The foragers</h2>
        </br>
        <p>
            Foragers will be given a vehicle with a limited amount of fuel to move around the terrain and forage coins.
        </p>
        </br>
        <img src={ASSETS_PATHS["foraging_url"]} alt="Two foragers moving around the world" width=400px/>
    </div>
    <div class="col">
      <h2>The coordinator</h2>
        <p>
             The coordinator helps foragers start in favorable locations. 
             The coordinator can buy resource location information before setting each forager's starting point.
        </p>
        <img src={ASSETS_PATHS["drag_drop_url"]} alt="Drag and drop foragers on the terrain" width=250px/>
    </div>
  </section>
    <p>            
        There will be {NUM_FORAGERS} foragers and only one coordinator.
    </p>    
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

WELCOME_TEXT_3 = f"""
    {STYLE}

    <h1>Welcome to the coordinator and foragers game!</h1>

    <h2>Rounds</h2>
    <p>
      You will play {len(WORLD_PATHS)} rounds. Each round is a self-contained world, so your actions in one round do not
      affect the worlds you will play later. However, your actions will shape the experience of players in subsequent
      iterations.
    </p>
    <p>
        Roles will be assigned in order of arrival to the round. 
    </p>
    <p>
        Players may get the same or a different role each round.
    </p>
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

WELCOME_TEXT_4 = f"""
    {STYLE}

    <h1>Welcome to the coordinator and foragers game!</h1>

    <h2>Score and monetary reward</h2>
    <p>
      In this experiment, your monetary reward has two parts:
    </p>
    <ul>
      <li>
        Payment based on the time you spend completing the experiment.
      </li>
      <li>
        A performance bonus. The bonus is calculated as your score (in coins) multiplied by {REWARD_SCALING_FACTOR}.
      </li>
    </ul>
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""


SOCIAL_CONTRACT = f"""
    {STYLE}

    <h2>The social contract</h2>
    <p>
        The social contract consists of three dimensions that determine how the collected coins are to be split
        among participants. The three dimensions are as follows:
    </p>
    <p>
    </p>
    <ul>
        <li>
            <strong>Overhead:</strong>
            This is the percentage of collected coins that is kept by the coordinator.
        </li>
        <li>
            <strong>Salary vs. Commission:</strong>
            This is the percentage of coins (remaining after subtracting overhead) that is evenly split among
            foragers (which produces the foragers' salary). The remaining coins are distributed between 
            the foragers in proportion to the number of coins collected by each one of them (the foragers' bonus).
        </li>
        <li>
            <strong>Foragers’ maximum speed:</strong>
            This is the allowed maximum speed for foragers’ trucks.
        </li>
    </ul>
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

PLAYING_WITH_SOCIAL_CONTRACT = f"""
    {STYLE}

    <h2>The social contract in action</h2>
    <p>
    Move the sliders below to explore how changing the social-contract dimensions would affect everyone’s score.
    </p>
    <p>
    One slider —Foragers’ maximum speed— does not change the score. Instead, it changes how much area foragers 
    can cover. Use the minimap in the right-hand panel below to see how the reachable area expands or shrinks as you adjust it.
    </p>
    <p class="final-note">
    Press the 'Next' button when you are ready to continue.
    </p>    
"""

CURRENT_OVERHEAD = lambda overhead: f"""
    {STYLE}
    
    <h1>Current value of the overhead</h1>
    <br>
    <p>
      The overhead is the percentage of coins the coordinator keeps from the total collected by the foragers.
      Right now, it is:
    </p>
    <p class="final-note">
    {overhead}%
    </p>
    
    <h2>Understanding the overhead</h2>
    <p>
      The example below shows how changing the current value of the overhead affects everyone’s rewards.
      The modifications you make here have no effect on the current value for this round; it is already set. 
      You will be asked latter to propose a new value.
    </p>
    <p>
      Assume you invested all 10 coins (leaving you with 0), and the three foragers collected 50, 30, and 20 coins.
    </p>

</body>
</html>
"""

############################################################
# Coordinator texts

COORDINATOR_INSTRUCTIONS_1 = lambda round_number: f"""
    {STYLE}

    <h1>Instructions for the Coordinator</h1>
    <br>
    <p>
    Welcome! You have been selected to play as the coordinator. 
    </p>
    <p>
    (Round {round_number} / {len(WORLD_PATHS)})
    </p>
    <h2>
    Goal
    </h2>
    <p>
      As the coordinator, you will invest in gathering information to decide where to assign foragers,
      with the goal of collecting as many coins as possible.
    </p>
    
    <p>
      You will also propose a change in the overhead, that is, the percentage of coins from the total
       set of coins collected by foragers that you will keep for yourself.
    </p>

    <h2>Overview</h2>
    
    <p>In this task, you will:</p>
    
    <ol>
      <li>Review the current overhead level.</li>
      <li>Complete a brief training on how to invest in information.</li>
      <li>Spend part of your endowment to learn where coins are located on the terrain.</li>
      <li>Assign foragers to the locations you identify.</li>
      <li>Propose a new overhead level.</li>
    </ol>
    
    <p>You will be guided through each step one at a time.</p>

    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""


INVESTMENT_INSTRUCTIONS = f"""
    {STYLE}

    <h1>Training for investing in information</h1>
    <br>
    <p>
      You have been given an endowment of 10 coins.
    </p>
    <p>
      You can invest some of these coins to learn where coins are located on the terrain.
      The more you invest:
    <ol>
      <li>The higher the chance that real coins are visible on the map.</li>
      <li>The lower the chance that false coins (noise) are visible on the map.</li>
    </ol>       
    <p>
      Note: Coins invested in information are spent—you will not keep them as part of your final reward.
    </p>
    <p>
      Move the slider below to see how your investment affects the information shown.
    </p>
    <p>
      Hover over the image to reveal the true coin locations.
    </p>
</body>
</html>
"""

MAKE_INVESTMENT = f"""
    {STYLE}

    <h1>Make your investment</h1>
    <br>
    <p>
    In this page you will use the slider to choose how many coins you want to invest.       
    </p>
    <p class="final-note">
      Note: You won't see the map with the coins until the next page, after you make your investment.
    </p>
    <br>
    <p>
    Make your investment:    
    </p>

</body>
</html>
"""


POSITIONING_INSTRUCTIONS = f"""
    {STYLE}

    <h1>Assign foragers</h1>
    <br>
    <p>
    Assign each forager to a location to maximize the coins they can forage. 
    Simply drag each icon and drop it to the selected position on the map. 
    </p>
    <br>

</body>
</html>
"""

############################################################
# Slider tweaking

OVERHEAD_TEXT = "This is the percentage of collected coins that is kept by the coordinator."
WAGES_TEXT = """This is the percentage of coins (remaining after subtracting overhead) that is evenly split 
among foragers. The remaining coins are distributed between the foragers in proportion to the number of coins
collected by each one of them."""
PREROGATIVE_TEXT = "This is the allowed maximum speed for foragers’ vehicles."

def explanation_text(dimension):
    if dimension == "overhead":
        return OVERHEAD_TEXT
    elif dimension == "wages":
        return WAGES_TEXT
    elif dimension == "prerogative":
        return PREROGATIVE_TEXT
    else:
        raise ValueError(f"Dimension must be 'overhead', 'wages', 'prerogative' (but got {dimension}.)")


def format_dimension(dimension:str) -> str:
    if dimension == "wages":
        return "Salary vs. Commission"
    if dimension == "prerogative":
            return "Foragers’ maximum speed"
    else:
        return dimension

SLIDER_SETTING_TEXT = lambda dimension: f"""
    {STYLE}

    <h1>Tweaking the social contract</h1>
    
    <h2>{format_dimension(dimension).upper()}</h2>
    <p>
    {explanation_text(dimension)}
    </p>
    <br>
        <p>
          Use this page to propose a new value for the
          <strong>{format_dimension(dimension)}</strong> parameter.
        </p>
        
        <p class="final-note">
          Note: Your proposal may or may not be adopted by the game.
        </p>
        <br>
        <p>
          The slider below shows the current value of
          <strong>{format_dimension(dimension)}</strong>.
          Drag it to set your preferred level.
        </p>

</body>
</html>
"""

############################################################
# Forager instructions

FORAGER_INSTRUCTIONS_1 = lambda episode_number: f"""
    {STYLE}

    <h1>Instructions for a Forager</h1>
    <br>
    <p>
    Welcome! You have been selected to play as a forager! 
    </p>
    <p>
    (Round {episode_number} / {len(WORLD_PATHS)})
    </p>
    <h2>
    Goal
    </h2>
    <p>
    Your task is simple: collect as many coins as you can while there is still fuel in your vehicle.
    </p>
    <img src={ASSETS_PATHS["forager_url"]} alt="The forager" width=300px/>    
    
    <h2>Overview</h2>
    <p>In this task, you will:</p>
    <ol>
      <li>Understand how your vehicle moves.</li>
      <li>Review the current overhead level.</li>
      <li>Drive around a terrain, starting from an initial position selected by the coordinator.</li>
      <li>Propose a new overhead level.</li>
    </ol>
    
    <p>You will be guided through each step one at a time.</p>
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

VEHICLE_TEXT_0 = f"""
    {STYLE}

    {THREE_COLUMN_STYLE}

    <h2>
    Your vehicle
    </h2>

    <p>
    To move, point your mouse at a nearby tile and click. Your vehicle will move toward the tile you clicked.
    </p>

    <img src={ASSETS_PATHS["click_move_url"]} alt="Click to move" width="400px"/>
    <p>
    If you click any tile inside the reachable area, you will move precisely to that tile.
    </p>
    <p>
    If you click any tile outside the reachable area, you will move toward the tile but will
    remain in the reachable area.
    </p>
    <p>
    When your vehicle runs out of fuel, your task is over.
    </p>

    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

VEHICLE_TEXT_1 = f"""
    {STYLE}

    {THREE_COLUMN_STYLE}
    
    <h2>
    Your vehicle
    </h2>
    
    <p>
    To move, point your mouse at a nearby tile and click. Your vehicle will move toward the tile you clicked.
    </p>
    
    <img src={ASSETS_PATHS["click_move_url"]} alt="Click to move" width="400px"/>
    
    <p>
    Which tiles count as “nearby” depends on your current gear.
    </p>
    
    <section class="three-cols">
      <div class="col3">
        Gear 1
      </div>
      <div class="col3">
        Gear 2
      </div>
      <div class="col3">
        Gear 3 
      </div>
    </section>
    <section class="three-cols">
      <div class="col3">
        <img src={ASSETS_PATHS["gear_1_url"]} alt="Proximal tiles with gear 1" width="150px"/>
      </div>
      <div class="col3">
        <img src={ASSETS_PATHS["gear_2_url"]} alt="Proximal tiles with gear 2" width="150px"/>
      </div>
      <div class="col3">
        <img src={ASSETS_PATHS["gear_3_url"]} alt="Proximal tiles with gear 3" width="150px"/>
      </div>
    </section>
    
    <p>
    If you click any tile inside the reachable area, you will move precisely to that tile.
    </p>
    <p>
    If you click any tile outside the reachable area, you will move toward the tile but will
    remain in the reachable area.
    </p>
    <p>
    When your vehicle runs out of fuel, your task is over.
    </p>

    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

VEHICLE_TEXT_2 = f"""
    {STYLE}

    {THREE_COLUMN_STYLE}

    <h2>
    Gears
    </h2>
    
    <p>
    You can change gears to adjust how far you can move in a single click.
    </p>
    
    <img src={ASSETS_PATHS["gears_url"]} alt="The gears" width="300px"/>
    
    <p>
    Higher gears give you a larger reach, while using the same amount of fuel per move.
    </p>
    
    <section class="three-cols">
      <div class="col3">
        <img src={ASSETS_PATHS["gear_1_url"]} alt="Reachable tiles with gear 1" width="150px"/>
      </div>
      <div class="col3">
        <img src={ASSETS_PATHS["gear_2_url"]} alt="Reachable tiles with gear 2" width="150px"/>
      </div>
      <div class="col3">
        <img src={ASSETS_PATHS["gear_3_url"]} alt="Reachable tiles with gear 3" width="150px"/>
      </div>
    </section>
    
    <section class="three-cols">
      <div class="col3">
        <b>Gear 1:</b> Move up to 1 tile toward the tile you clicked.
      </div>
      <div class="col3">
        <b>Gear 2:</b> Move up to 2 tiles toward the tile you clicked.
      </div>
      <div class="col3">
        <b>Gear 3:</b> Move up to 3 tiles toward the tile you clicked.
      </div>
    </section>
    
    <p>
    Click any tile within the reachable area to move directly to that tile.
    </p>
    
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

MINIMAP_TEXT = f"""
    {STYLE}

    <h2>
    The minimap
    </h2>
    
    <p>
    Navigation information is limited. To help you orient yourself, you will see a minimap showing your
    current location on the full ground.
    </p>

    <img src={ASSETS_PATHS["minimap_url"]} alt="The minimap" width="300px"/>

    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

############################################################
# Time to forage

FORAGING_PAGE = f"""
    
    <p>
    It’s time to forage! 
    Drive your vehicle onto the golden squares to collect coins.
    Enjoy the ride!
    </p>
    <p class="final-note">
    When you are ready to continue, press the 'Next' button.
    </p>
"""


COLLECTING_TEXT = f"""
    {STYLE}

    <h2>Collecting</h2>
    <p>
      Please wait while the foragers collect coins.
    </p>
    <p>
      They will continue collecting until they run out of fuel or choose to stop.
    </p>
    <p class="final-note">
    Do not refresh this page!
    </p>
"""

OTHER_FORAGERS_COLLECTING_TEXT = lambda collected_coins: f"""
    {STYLE}

    <h2>Score</h2>
    You have collected {collected_coins} coins!
    <p>
      Please wait while the other foragers collect coins.
    </p>
    <p class="final-note">
    Do not refresh this page!
    </p>
"""

############################################################
# Score page

SCORE_TEXT = lambda reward_text: f"""
    {STYLE}

    <h1>Score</h1>
    <br>
    {reward_text}
    <br>
    <p class="final-note">
    When you are ready to continue, press the 'Next' button.
    </p>
    <br>

</body>
</html>
"""


MY_COLLECTED_COINS_TEXT = lambda my_coins: f"""
    {STYLE}

    <h1>Coins collected</h1>
    <br>
    You collected {my_coins} coins!
    <br>
    <p class="final-note">
    When you are ready to continue, press the 'Next' button.
    </p>
    <br>

</body>
</html>
"""
############################################################
# Well-being page

SATISFACTION_TEXT = f"""
    {STYLE}
    <h1>Satisfaction report</h1>
    <br>
    <p>
      Now take a moment to step back and reflect: does the score you obtained feel adequate?
    </p>
    
    <p>
      A 0% agreement (far left) means you strongly disagree with the outcome and definitely
      want to change the social contract.
    </p>
    
    <p>
      A 100% agreement (far right) means you fully agree with the outcome —things are fine
      as they are— and you don't want to change the social contract.
    </p>
    
    <p>
      Use the slider below to report your satisfaction with this outcome.
    </p>
    <br>
    <p class="final-note">
    When you are ready to continue, press the 'Next' button.
    </p>
    <br>

</body>
</html>
"""

