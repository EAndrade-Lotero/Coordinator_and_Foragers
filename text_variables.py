# module with the texts as variables to be used in the respective pages
from .game_parameters import NUM_FORAGERS, WORLD_PATHS

############################################################
# Format

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
            max-width: 750px;
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

############################################################
# Welcome text

WELCOME_TEXT = f"""
    {STYLE}

    <h1>Welcome to the coordinator and foragers game!</h1>

    <h2>Overview</h2>
    <p>
        The purpose of this game is to collectively forage as many coins as possible from the ground.
    </p>

    <h2>Roles</h2>
    <p>
        In this game, you will be playing as one of two roles. A forager, who collects coins from the ground;
        or a coordinator, who coordinates the foragers’ efforts by assigning them to a favorable foraging ground.
        There will be {NUM_FORAGERS} foragers and only one coordinator.
    </p>
    <p>
        The coordinator will be given an endowment to invest for information about the terrain. The bigger the
        proportion of endowment invested, the higher the probability of discovering the location of each coin.
        He or she will use this information to initially locate foragers at the most convenient points on
        the terrain.
    </p>
    <p>
        Foragers will not be given any initial endowment. They will be given a 3-gear UTV with a limited amount
        of fuel to move around the terrain and forage coins.
    </p>
    <p>
        Roles will be assigned in order of arrival to an iteration of the game. Each player will be asked to play
        {len(WORLD_PATHS)} iterations.
    </p>

    <h2>Score</h2>
    <p>
        Scores will be calculated by dividing the total number of coins foraged in the previous iteration.
    </p>
    
    <p>
        The coordinator’s score will depend on two factors:
        <li>
            The coins remaining from the initial endowment after investing for information.
        </li>
        <li>
            A predetermined percentage of the total number of coins.
        </li>
    </p>
    <p>
        The score for each forager will depend on three factors:
        <li>
            How many coins are going to the coordinator.
        </li>
        <li>
            How many remaining coins are evenly split among all foragers.
        </li>
        <li>
            How many coins the forager collected.
        </li>
    </p>

    <h2>The social contract</h2>
    <p>
        The social contract consists of three dimensions that determine how the collected coins are to be split
        among participants. The three dimensions are as follows:
    </p>
    <p>
    </p>
    <ul>
        <li>
            <strong>Overhead (a number between 0 and 1):</strong>
            This is the percentage of the total amount of collected coins that is kept by the coordinator.
        </li>
        <li>
            <strong>Wages:</strong>
            This is the percentage of coins (remaining after subtracting overhead) that is evenly split among
            foragers. The remaining coins are distributed between the foragers in proportion to the number of
            coins collected by each one of them.
        </li>
        <li>
            <strong>Foragers’ maximum speed:</strong>
            This is the allowed maximum speed for foragers’ trucks.
        </li>
    </ul>

    <p class="final-note">
        If you understood these instructions, press the button &ldquo;Next&rdquo; to proceed.
        You will be placed in one of the two roles.
    </p>

</body>
</html>
"""

############################################################
# Coordinator texts

COORDINATOR_INSTRUCTIONS = f"""
    {STYLE}

    <h1>Instructions for the Coordinator</h1>
    <br>
    <p>
    Welcome! You have been selected to play as the coordinator. 
    </p>
    <h2>
    Goal
    </h2>
    <p>    
    Your role is to make sure that foragers are in a position to forage the maximum number of coins. 
    So you must locate them at the best places in the terrain. You will need information for this. 
    </p>
    <h2>
    Information
    </h2>
    <p>        
    Congratulations! You have been given an endowment of 10 coins!
    </p>
    <p>        
    In the next page, you will be asked to use this endowment to obtain information. 
    What you want to know is the locations of pockets of coins. That is, places with
    high concentrations of coins. You will never be able to see all coins; only a percentage of them. 
    How many coins will be visible depends on how much of your endowment you invest. 
    Please follow the instructions in the “Gathering information” page to make your investment.
    </p>
    <h2>
    Assign foragers
    </h2>
    <p>
    Once you have made your investment in information, you will be redirected to the “Assign foragers” page.
    There you will see a map with the discovered coins and icons of {NUM_FORAGERS} foragers. Drag these icons 
    onto the locations that will allow foragers to collect more coins. Please follow the instructions in
    the “Positioning foragers” page. 
    </p>
    <h2>
    Score
    </h2>
    <p>
    Once you are done with this critical task, in the “Score” page you will see the total number of 
    coins collected by foragers on the previous iteration. You will also see your score based on this number. 
    </p>
    <h2>
    Well-being report
    </h2>
    <p>
    The score is determined by the characteristics of the social contract, which you can evaluate in the 
    “Well-being report” page. Follow the instructions in this page to provide your report.
    </p>
    <h2>
    Tweak the social contract
    </h2>
    <p>
    Finally, you will be given the power to tweak the three dimensions of the social contract. 
    Follow the instructions in the “Tweaking the social contract” pages to move the parameters 
    in the direction that  you consider will provide you with a better well-being.
    </p>
    <br>
    <br>
    <p>
    That’s it for instructions. Enjoy playing “The coordinator and foragers” game!
    </p>
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

INVESTMENT_INSTRUCTIONS = f"""
    {STYLE}

    <h1>Gathering information</h1>
    <br>
    <p>
    You have to invest a percentage of your endowment to obtain information about the location
    of coins in the terrain. The higher the percentage you invest, the higher the probability 
    for each coin to be visible in your map. You will only be able to see this map in the next page.
    </p>
    <p>
    Remember, you will not be able to see all coins but only a fraction of them. You must
    use your judgement to infer the location of pockets of coins, that is, places with high
    concentrations of coins.
    </p>
    <p>
    Move the slider to determine the percentage of your endowment that you want to invest. 
    </p>
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>
    <br>

</body>
</html>
"""

############################################################
# Positioning page

POSITIONING_INSTRUCTIONS = f"""
    {STYLE}

    <h1>Assign foragers</h1>
    <br>
    <p>
    Assign each forager to a location to maximize the coins they can forage. 
    Simply drag each icon and drop it to the selected position on the map. 
    </p>
    <p class="final-note">
    When you are ready to continue, press the 'Next' button.
    </p>
    <br>

</body>
</html>
"""

############################################################
# Slider tweaking

SLIDER_SETTING_TEXT = lambda dimension: f"""
    {STYLE}

    <h1>Tweaking the social contract</h1>
    
    <h2>{dimension.upper()}</h2>
    <br>
    <p>
    This is the place to modify the parameters of the social contract established so far.
    </p>
    <p>
    You can now modify the {dimension} parameter. 
    </p>
    <p>
    The slider below displays its current level.
    </p>
    <p>
     Please move it to match your desired level of {dimension}.
    </p>
    <br>
    </p>
    <p class="final-note">
    When you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

############################################################
# Forager instructions

FORAGER_INSTRUCTIONS = f"""
    {STYLE}

    <h1>Instructions for a Forager</h1>
    <br>
    <p>
    Welcome! You have been selected to play as a forager! 
    </p>
    <h2>
    Goal
    </h2>
    <p>
    Your task is simple: collect as many coins as you can while there is still fuel in your UTV.
    You will be driving around a terrain, starting from an initial position selected by the coordinator. 
    You will use this vehicle to collect coins by driving over them. 
    </p>
    <h2>
    Your vehicle
    </h2>
    <p>
    You can accelerate, steer, break, and change gears. Don’t worry, it’s very easy to do it and you will be 
    an expert driver in no time. The only thing you should remember about gears is that they control two things. 
    They control speed: the higher the gear number, the faster you go. 
    </p>
    <p>
    The second, and most important thing, is that <strong>you will only be able to collect a coin if the truck 
    is in first gear</strong> when you pass over it. 
    </p>
    <p>    
    Do not randomly move collecting coins right and left; drive and collect safely and thoughtfully.
    </p>
    <p>    
    How many gears your UTV has depends on the dimension “Foragers’ maximum speed” from the social contract.
    </p>
    <h2>
    Score
    </h2>
    <p>
    Once your UTV runs out of fuel, your task is over. You will be directed to the “Score” page, 
    in which you will see the total number of coins collected by foragers on the previous iteration. 
    You will also see your reward based on this number of coins. This reward is determined by 
    the characteristics of the social contract. 
    </p>
    <h2>
    Well-being report
    </h2>
    <p>
    In the page “Well-being report” you will be asked to rate how well you feel about the score obtained. 
    Follow the instructions in this page to provide your report.
    </p>
    <br>
    <br>
    <p>
    That’s it for instructions. Enjoy playing “The coordinator and foragers” game!
    </p>
    <p class="final-note">
    If you are ready to continue, press the 'Next' button.
    </p>

</body>
</html>
"""

############################################################
# Time to forage

FORAGING_PAGE = f"""
It's time to forage! Remember, you will only be able to forage a coin if your
UTV is in first gear. Enjoy the ride!
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

############################################################
# Well-being page

WELL_BEING_TEXT = f"""
    {STYLE}

    <h1>Well-being report</h1>
    <br>
    <p>
    It is time to take a step back and calmly ask yourself whether the result obtained
    agrees with the work that you have put in so far. 
    </p>
    <p>
    A 0% agreement, at the far left
    of the slider, would mean that you definitely want a change in the social contract.
    </p>
    <p>
    A 100% agreement, at the far right of the slider, would mean that things are just fine
    and we can leave them be.
    </p>
    <p>
    Use the slider below to report your well-being with the obtained result.
    </p>
    <br>
    <p class="final-note">
    When you are ready to continue, press the 'Next' button.
    </p>
    <br>

</body>
</html>
"""