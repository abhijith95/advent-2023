import re
import numpy as np


def return_lines(txtFile: str) -> list[str]:
    """Function that will go through a text file and return the lines as list of string

    Parameters
    ----------
    txtFile : str
        name of the text file

    Returns
    -------
    list[str]
        lines in the text file
    """
    with open(txtFile, "r") as f:
        lines: list[str] = f.readlines()
    return lines


def task1() -> None:
    """As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

    The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

    For example:

    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet
    In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

    Consider your entire calibration document. What is the sum of all of the calibration values?
    """
    txt_fileName = "task1.txt"
    with open(txt_fileName, "r") as f:
        lines: list[str] = f.readlines()

    sum_ans: int = 0
    for line in lines:
        regx_res = re.findall(pattern=r"(\d)", string=line)
        if regx_res:
            # do this step only if you find numbers in the line
            tmp_num: int = int("".join([regx_res[0], regx_res[-1]]))
            sum_ans += tmp_num

    print("The total sum is, ", sum_ans)


def task2() -> None:
    """Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

    Equipped with this new information, you now need to find the real first and last digit on each line. For example:

    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

    What is the sum of all of the calibration values?
    """
    words_to_numMap: dict[str, str] = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }
    txt_fileName = "task1.txt"
    with open(txt_fileName, "r") as f:
        lines: list[str] = f.readlines()

    # having the positive lookahead will help in selecting overlapping numbers like twone into 2 and a 1.
    search_pattern = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"
    sum_ans: int = 0
    for line in lines:
        regx_res = re.findall(pattern=search_pattern, string=line)
        tmp_num: int = 0
        if regx_res:
            tmp_num = int(
                "".join(
                    [
                        words_to_numMap.get(regx_res[0]),
                        words_to_numMap.get(regx_res[-1]),
                    ]
                )
            )
        sum_ans += tmp_num

    print("The total sum is, ", sum_ans)


def task3() -> None:
    """As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

    To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

    You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

    For example, the record of a few games might look like this:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

    The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

    In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

    Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
    """
    game_dict = {}
    lines = return_lines("task3.txt")
    sum_ans: int = 0
    possible_combo: dict[str, int] = {"red": 12, "blue": 14, "green": 13}
    for line in lines:
        regx_res = re.findall(pattern=r"(?<=Game )\d+", string=line)
        game_id = int(regx_res[0])
        game_dict.update({game_id: {"red": 0, "blue": 0, "green": 0}})
        its_possble = True
        for game_set in line.split(";"):
            for pattern, color in zip(
                (r"(\d+(?= red))", r"(\d+(?= blue))", r"(\d+(?= green))"),
                ("red", "blue", "green"),
            ):
                regx_res = re.findall(pattern, game_set)
                if regx_res and int(regx_res[0]) > possible_combo.get(color):
                    its_possble = False
        if its_possble:
            sum_ans += game_id
    print(sum_ans)


def task4() -> None:
    """As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

    Again consider the example games from earlier:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
    Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
    Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
    Game 4 required at least 14 red, 3 green, and 15 blue cubes.
    Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
    The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

    For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
    """
    game_dict = {}
    lines = return_lines("task3.txt")
    sum_ans: int = 0
    for line in lines:
        powr = 1
        regx_res = re.findall(pattern=r"(?<=Game )\d+", string=line)
        game_id = int(regx_res[0])
        max_cubes = [0, 0, 0]
        for game_set in line.split(";"):
            for i, pattern in enumerate(
                (r"(\d+(?= red))", r"(\d+(?= blue))", r"(\d+(?= green))")
            ):
                regx_res = re.findall(pattern, game_set)
                if regx_res and (int(regx_res[0]) > max_cubes[i]):
                    max_cubes[i] = int(regx_res[0])
        sum_ans += np.prod(max_cubes)
    print(sum_ans)


def search_grid(i: int, j: int, nr_row: int, nr_col: int) -> list[int]:
    if i == 0 and j == 0:
        return [[0, 1], [1, 0], [1, 1]]
    elif i == 0 and j == nr_col - 1:
        return [[0, j - 1], [1, j], [1, j - 1]]
    elif i == nr_row - 1 and j == 0:
        return [[i - 1, 0], [i, 1], [i - 1, 1]]
    elif i == nr_row - 1 and j == nr_col - 1:
        return [[i, j - 1], [i - 1, j], [i - 1, j - 1]]
    elif j == 0:
        return [[i - 1, j], [i + 1, j], [i, j + 1], [i - 1, j + 1], [i + 1, j + 1]]
    elif i == 0:
        return [[i, j - 1], [i, j + 1], [i + 1, j], [i + 1, j - 1], [i + 1, j + 1]]
    elif i == nr_row - 1:
        return [[i, j - 1], [i, j + 1], [i - 1, j], [i - 1, j - 1], [i - 1, j + 1]]
    elif j == nr_col - 1:
        return [[i - 1, j], [i + 1, j], [i, j - 1], [i - 1, j - 1], [i + 1, j - 1]]
    else:
        return [
            (i, j - 1),
            (i - 1, j - 1),
            (i + 1, j - 1),
            (i, j + 1),
            (i - 1, j + 1),
            (i + 1, j + 1),
            (i - 1, j),
            (i + 1, j),
        ]


def task5() -> None:
    """The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

    The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

    Here is an example engine schematic:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

    Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
    """
    lines: list[str] = return_lines("task5.txt")
    lines = [l.replace("\n", "") for l in lines]
    nr_rows: int = len(lines)
    nr_cols: int = len(lines[0])
    not_symbols: list[str] = ["."] + [str(i) for i in range(10)]
    ans_sum = []
    prt_num = ""
    for i, line in enumerate(lines):
        j = 0
        strt_indx = 0
        while j < nr_cols:
            if line[j].isdigit():
                # perform the search only if the character is a digit
                found_symbol = False
                search_list: list[int] = search_grid(i, j, nr_rows, nr_cols)
                for indx_pair in search_list:
                    if lines[indx_pair[0]][indx_pair[1]] not in not_symbols:
                        # we have found a symbol
                        found_symbol = True
                        break
                if found_symbol:
                    # collect all the digits amidst the line, that end with the current digit as the final character
                    prev_digits = re.findall(
                        pattern=r"(?<=\.)\d*" + line[j] + r"|(?<=)\d*" + line[j],
                        string=line[strt_indx : j + 1],
                    )
                    # starting from the current digit collect all the digits until you hit . or end of line
                    post_digits = re.findall(
                        pattern=r"\d*(?=\.)|" + r"\d*(?=)",
                        string=line[j:],
                    )
                    prt_num = ""
                    if prev_digits:
                        # the current digit is collected twice so we drop it in the previous part
                        prt_num = prt_num + "".join(prev_digits[0][0:-1])
                    if post_digits:
                        prt_num = prt_num + "".join(post_digits[0])
                        j += len(post_digits[0])
                    else:
                        j += 1
                    if prt_num:
                        ans_sum.append(int(prt_num))
                else:
                    j += 1
            else:
                # every time we encounter a period we will change our start index, this is so we don't search the
                # previous number set
                strt_indx = j
                j += 1
    print(sum(ans_sum))


def task6() -> None:
    """The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

    You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

    Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

    The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

    This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

    Consider the same engine schematic again:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
    """
    lines: list[str] = return_lines("task5.txt")
    lines = [l.replace("\n", "") for l in lines]
    nr_rows: int = len(lines)
    nr_cols: int = len(lines[0])
    ans_sum: int = 0
    prt_num = ""
    gearPos: list[list[int]] = []
    prtNums: list[int] = []

    for i, line in enumerate(lines):
        j = 0
        strt_indx = 0
        while j < nr_cols:
            if line[j].isdigit():
                # perform the search only if the character is a digit
                found_symbol = False
                search_list: list[int] = search_grid(i, j, nr_rows, nr_cols)
                for indx_pair in search_list:
                    if lines[indx_pair[0]][indx_pair[1]] == "*":
                        # we have found the gear symbol
                        found_symbol = True
                        gearPos_x: int = indx_pair[0]
                        gearPos_y: int = indx_pair[1]
                        break
                if found_symbol:
                    # collect all the digits amidst the line, that end with the current digit as the final character
                    prev_digits = re.findall(
                        pattern=r"(?<=\.)\d*" + line[j] + r"|(?<=)\d*" + line[j],
                        string=line[strt_indx : j + 1],
                    )
                    # starting from the current digit collect all the digits until you hit . or end of line
                    post_digits = re.findall(
                        pattern=r"\d*(?=\.)|" + r"\d*(?=)",
                        string=line[j:],
                    )
                    prt_num = ""
                    if prev_digits:
                        # the current digit is collected twice so we drop it in the previous part
                        prt_num = prt_num + "".join(prev_digits[0][0:-1])
                    if post_digits:
                        prt_num = prt_num + "".join(post_digits[0])
                        j += len(post_digits[0])
                    else:
                        j += 1
                    if prt_num:
                        prtNums.append(int(prt_num))
                        gearPos.append([gearPos_x, gearPos_y])
                else:
                    j += 1
            else:
                # every time we encounter a period we will change our start index, this is so we don't search the
                # previous number set
                strt_indx = j
                j += 1

    for i, (num, gPos) in enumerate(zip(prtNums, gearPos)):
        for num2, gPos2 in zip(prtNums[i + 1 :], gearPos[i + 1 :]):
            if gPos[0] == gPos2[0] and gPos[1] == gPos2[1]:
                ans_sum += num * num2
                break

    print(ans_sum)


if __name__ == "__main__":
    task6()
