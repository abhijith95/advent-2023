import re
from utils import return_lines
from enum import Enum


class Hands(Enum):
    FIVEOFKIND = [5]
    FOUROFKIND = [4, 1]
    FULLHOUSE = [3, 2]
    THREEOFKIND = [3, 1, 1]
    TWOPAIR = [2, 2, 1]
    ONEPAIR = [2, 1, 1, 1]
    HIGHCARD = [1, 1, 1, 1, 1]


HAND_VALUE: dict[Hands, str] = {
    Hands.FIVEOFKIND: "7",
    Hands.FOUROFKIND: "6",
    Hands.FULLHOUSE: "5",
    Hands.THREEOFKIND: "4",
    Hands.TWOPAIR: "3",
    Hands.ONEPAIR: "2",
    Hands.HIGHCARD: "1",
}

CARD_VALUE: dict[str, int] = {
    "A": "14",
    "K": "13",
    "Q": "12",
    "J": "1",  # use 11 for part 1
    "T": "10",
    "9": "9",
    "8": "8",
    "7": "7",
    "6": "6",
    "5": "5",
    "4": "4",
    "3": "3",
    "2": "2",
}


def identify_hand(line: str) -> dict:
    cards: list[str] = re.findall(pattern=r"[AKQJT98765432]", string=line.split(" ")[0])
    bid: int = int(line.split(" ")[1])
    # number of repeating cards appearing in the hand
    card_countInfo: dict = {i: cards.count(i) for i in cards}
    # card_countInfo: list = [cards.count(i) for i in cards]
    # PART2 #####################################
    if "J" in list(card_countInfo.keys()):
        # we take away all the joker and then add it to that hand with the maximum count.
        joker_count = card_countInfo.get("J")
        if joker_count < 5:
            # if all of them are joker then we leave it as five of a kind
            card_countInfo.pop("J", None)
            # get the key with maximum count value
            tmp_key: str = max(card_countInfo, key=card_countInfo.get)
            card_countInfo[tmp_key] += joker_count
    # PART2 #####################################
    hand_value = 0
    for i, c in enumerate(cards):
        hand_value += (10 ** (-1.5 * i)) * int(CARD_VALUE.get(c))
    # hand_value: list = [CARD_VALUE.get(c) for c in cards]
    hand_info: dict = {"count_info": card_countInfo}
    for hand in Hands:
        if sorted(hand.value) == sorted(card_countInfo.values()):
            hand_info.update({"Hand info": hand})
            # tmp: float = (int("".join(hand_value)) - 23456) / 1414141414
            # hand_value: float = int(HAND_VALUE.get(hand)) + float(
            #     int("".join(hand_value)) / 1414141414
            # )
            hand_value += 100 * int(HAND_VALUE.get(hand))
            hand_info.update({"hand_value": hand_value})
            break
    hand_info.update({"bid": bid})
    return hand_info


def part1():
    """In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

    Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456
    Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

    If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

    So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

    To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483
    This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

    So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
    Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

    Find the rank of every hand in your set. What are the total winnings?


    """
    lines: list[str] = return_lines("day7.txt")
    handInfo_list: dict[dict] = {}
    for line in lines:
        tmp: dict = identify_hand(line)
        handInfo_list.update({tmp.get("hand_value"): identify_hand(line)})
    sortd_dict = dict(sorted(handInfo_list.items()))
    ans_sum = 0
    for i, d in enumerate(sortd_dict.values()):
        ans_sum += (i + 1) * d.get("bid")
    print(ans_sum)


def part2():
    pass


if __name__ == "__main__":
    part1()
