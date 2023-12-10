from utils import return_lines


def match_lists(list1: list, list2: list) -> int:
    """Function that will return the number of matches between two lists

    Parameters
    ----------
    list1 : list
    list2 : list

    Returns
    -------
    int
        number of matches
    """
    if len(list1) < len(list2):
        sml_list = list1
        big_list = list2
    else:
        sml_list = list2
        big_list = list1

    num_hits: int = 0
    for i in sml_list:
        for j in big_list:
            if (i == j) and (i.isdigit() and j.isdigit()):
                num_hits += 1
    return num_hits


def part1() -> None:
    """The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, all with their opaque covering already scratched off. Picking one up, it looks like each card has two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have. You organize the information into a table (your puzzle input).

    As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the list of winning numbers. The first match makes the card worth one point and each match after the first doubles the point value of that card.

    For example:

    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86) are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three times for each of the three matches after the first).

    Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
    Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
    Card 4 has one winning number (84), so it is worth 1 point.
    Card 5 has no winning numbers, so it is worth no points.
    Card 6 has no winning numbers, so it is worth no points.
    So, in this example, the Elf's pile of scratchcards is worth 13 points.
    """
    lines: list[str] = return_lines(txtFile="day4_egInput.txt")
    winNums_list: list[list[int]] = []
    myNums_list: list[list[int]] = []
    total_pnts: int = 0

    for i, line in enumerate(lines):
        num_list: str = line.split(": ")[1]
        # (.*)(?=\|) (?<=\|).*
        winNums_list.append(num_list.split(" | ")[0].split(" "))
        myNums_list.append(num_list.split(" | ")[1].split(" "))

    for list1, list2 in zip(myNums_list, winNums_list):
        num_hits = match_lists(list1, list2)
        num_pnts = 0
        if num_hits > 0:
            total_pnts += 2 ** (num_hits - 1)
    print(total_pnts)


def part2() -> None:
    """There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.

    Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

    Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win any more cards. (Cards will never make you copy a card past the end of the table.)

    This time, the above example goes differently:

    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
    Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
    Your copy of card 2 also wins one copy each of cards 3 and 4.
    Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
    Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
    Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
    Your one instance of card 6 (one original) has no matching numbers and wins no more cards.
    Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!

    Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of scratchcards, how many total scratchcards do you end up with?
    """
    lines: list[str] = return_lines(txtFile="day4_input.txt")
    score: dict = {}
    orig_cards: list[int] = []
    copy_cards: list[int] = []
    for i, line in enumerate(lines):
        num_list: str = line.split(": ")[1]
        # (.*)(?=\|) (?<=\|).*
        num_hits = match_lists(
            num_list.split(" | ")[0].split(" "), num_list.split(" | ")[1].split(" ")
        )
        score.update({i + 1: num_hits})
        orig_cards.append(i + 1)

        if num_hits > 0:
            nrOf_rep = copy_cards.count(i + 1)
            copy_cards = copy_cards + (nrOf_rep + 1) * [
                j for j in range(i + 2, i + 2 + num_hits)
            ]
        # else:
        #     copy_cards = copy_cards + [j for j in range(i + 2, i + 2 + num_hits)]

    print(len(copy_cards) + len(orig_cards))


if __name__ == "__main__":
    part2()
