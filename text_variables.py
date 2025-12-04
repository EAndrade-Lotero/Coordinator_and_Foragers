# module with the texts as variables to be used in the respective pages

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
        The purpose of this game is to collectively forage as many coins from the ground as possible.
    </p>

    <h2>Roles</h2>
    <p>
        In this game, you will be playing as one of two roles. A forager, who collects coins from the ground;
        or a coordinator, who coordinates the foragers’ efforts by assigning them to a favorable foraging ground.
        There will be four foragers and only one coordinator.
    </p>
    <br>
    <p>
        The coordinator will be given an endowment to invest for information about the terrain. The bigger the
        proportion of endowment invested, the higher the probability of discovering the location of each coin.
        Secondly, the coordinator will use this information to locate foragers at the most convenient points on
        the terrain.
    </p>
    <br>
    <p>
        Note that foragers will not be given any initial endowment.
    </p>
    <br>
    <p>
        Roles will be assigned in order of arrival to an iteration of the game. Each player is required to play
        three iterations in the same or different role.
    </p>

    <h2>The social contract</h2>
    <p>
        The social contract consists of three dimensions that determine how the collected coins are to be split
        among participants. To give this game a sense of long-term commitment, rewards for one iteration will
        depend on the number of coins collected by the foragers in the previous iteration.
    </p>
    <p>
        The three dimensions of the social contract are as follows:
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

    <h2>Rewards</h2>
    <p>
        The coordinator’s reward is calculated with the following formula:
    </p>
    <div class="formula-block">
        coordinator_reward = endowment_kept + total_coins * overhead
    </div>

    <p>
        Each forager’s reward is calculated using the three following formulas:
    </p>
    <div class="formula-block">
        wage_forager_i = total_coins * (1 - overhead) * (wages / 4)
    </div>
    <div class="formula-block">
        commission_forager_i = coins_collected_by_i * (1 - overhead) * (1 - wages)
    </div>
    <div class="formula-block">
        forager_i_reward = wage_forager_i + commission_forager_i
    </div>

    <p class="final-note">
        Please press the button &ldquo;Next&rdquo; to proceed to be placed in one of the roles.
    </p>

</body>
</html>
"""

############################################################
# Coordinator instructions

COORDINATOR_INSTRUCTIONS = f"""
    {STYLE}

    <h1>Instructions for the Coordinator</h1>

    <p>
    Welcome! You have been selected to play as the coordinator. Your role is to make sure that foragers are in a position to forage the maximum number of coins. To this effect, you must locate them at the best places in the terrain. 
    You will need information to do this task. So, the order of things is to first use your initial endowment to invest for information. What you want to know is where coins are located on the terrain. You will never be able to see all coins; only a percentage of them. What percentage will be visible depends on the percentage of your endowment that you invest. Please follow the instructions in the “Investment for information” page.
    Next, in the “Assign foragers” page, you will see a map with the discovered coins and icons of four foragers. Drag these icons onto the locations that, to the best of your knowledge, are the best position for foragers to collect more coins. These will be the locations that foragers will start from. They will move around the terrain foraging coins for as long as their trucks have fuel, and as fast as allowed by the social contract.
    Once you are done with this critical task, in the “Reward” page you will see the total number of coins collected by foragers on the previous iteration. You will also see your reward based on this number of coins. This reward is determined by the characteristics of the social contract. 
    Note that the monetary reward that you will receive at the end of the experiment is the sum of rewards from the three iterations you play. 
    </p>
    <br>
    <p>
    As a refresher, here is the formula used to calculate your reward:
    </p>
    <div class="formula-block">
        coordinator_reward = endowment_kept + total_coins * overhead
    </div>
    <p>
    For instance, suppose the foragers collected 100 coins in the previous iteration. If the overhead was 50%, you will keep 50 of these coins. Moreover, if your initial endowment was 10 coins and you only invested 20% in information, keeping 8 coins from your endowment, your reward will be 58 coins.
    Sure, the most crucial dimension of the social contract for you as a coordinator is the overhead. But don’t lose sight that the total number of coins depends on the foragers’ sweat, blood and tears they put into foraging coins. Their motivations are driven by the other dimensions of the social contract.
    </p>
    <br>
    <p>
    In the page “Well-being report” you will be asked to rate how well you feel about the reward obtained. Follow the instructions in this page to provide your report.
    [DEPENDING ON CONDITION] Finally, you will be given the power to tweak the three dimensions of the social contract. Follow the instructions in the page “Tweaking the social contract” to move the parameters in the direction that you consider will provide you with a better well-being (or keep them, if you are happy as it is).
    </p>
    <br>
    <p>
    That’s it for instructions. Enjoy playing “The coordinator and foragers” game!
    </p>

</body>
</html>
"""

############################################################
# Coordinator instructions

FORAGER_INSTRUCTIONS = f"""
    {STYLE}

    <h1>Instructions for a Forager</h1>

    <p>
    Welcome! You have been selected to play as a forager. Your task is simple: collect as many coins as you can while there is still fuel in your truck.
    You will be driving a small truck around a terrain, starting from an initial position selected by the coordinator. You will use this truck to collect coins by driving over them. You can accelerate, steer, break, and change gears. Don’t worry, it’s very easy to do it and you will be an expert driver in no time. 
    The only thing you should remember about gears is that they control two things. They control speed: the higher the gear number, the faster you go. The second, and most important thing, is that you will only be able to collect a coin if you pass over it and the truck is in first gear. No rushing like crazy collecting coins right and left; drive and collect safely.
    How many gears your truck has depends on the dimension “Foragers’ maximum speed” from the social contract.
    </p>
    <br>
    <p>
    Once your truck runs out of fuel, your task is over. You will be directed to the “Reward” page, in which you will see the total number of coins collected by foragers on the previous iteration. You will also see your reward based on this number of coins. This reward is determined by the characteristics of the social contract. 
    Note that the monetary reward that you will receive at the end of the experiment is the sum of rewards from the three iterations you play. 
    </p>
    <br>
    <p>
    As a refresher, here are the three formulas used to calculate your reward:
    </p>
    <div class="formula-block">
        wage_forager_i = total_coins * (1 - overhead) * (wages / 4)
    </div>
    <div class="formula-block">
        commission_forager_i = coins_collected_by_i * (1 - overhead) * (1 - wages)
    </div>
    <div class="formula-block">
        forager_i_reward = wage_forager_i + commission_forager_i
    </div>
    <br>
    <p>
    For instance, suppose the foragers collected 100 coins in the previous iteration. If the overhead was 20%, you and your fellow foragers will be left with 80 of these coins. If the wages parameter is 75%, then 60 of these coins will be equally split among foragers. This will give you 15 coins from wages. Moreover, if you collected 50 coins, this means that your commission is 10 coins (that is, 50% of the remaining 20 coins). In the end, your reward will be 15 + 10 = 25 coins.
    </p>
    <br>
    <p>
    In the page “Well-being report” you will be asked to rate how well you feel about the reward obtained. Follow the instructions in this page to provide your report.
    [DEPENDING ON CONDITION] Finally, you will be given the power to tweak the three dimensions of the social contract. Follow the instructions in the page “Tweaking the social contract” to move the parameters in the direction that you consider will provide you with a better well-being (or keep them, if you are happy as it is).
    </p>
    <br>
    <p>
    That’s it for instructions. Enjoy playing “The coordinator and foragers” game!
    </p>

</body>
</html>
"""