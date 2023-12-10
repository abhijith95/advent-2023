import re
from utils import return_lines


def map_paths(lines) -> dict:
    map_dict: dict = {}
    for line in lines:
        regx_res = re.findall(r"(\w+)", line)
        map_dict.update({regx_res[0]: {"L": regx_res[1], "R": regx_res[2]}})
    return map_dict


def map_paths2(lines) -> [dict, list]:
    map_dict: dict = {}
    start_nodes: list = []
    for line in lines:
        regx_res = re.findall(r"(\w+)", line)
        map_dict.update({regx_res[0]: {"L": regx_res[1], "R": regx_res[2]}})
        if regx_res[0][-1] == "A":
            start_nodes.append(regx_res[0])
    return [map_dict, start_nodes]


def part1() -> None:
    """One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

    It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

    After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

    This format defines each node of the network individually. For example:

    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)
    Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

    Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

    LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)
    Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
    """
    lines: list[str] = return_lines("day8.txt")
    seq_instr = lines[0]
    map_dict = map_paths(lines[2:])
    zzz_found = False
    prev_step = "AAA"
    num_steps = 0
    while not zzz_found:
        for instruct in seq_instr:
            nxt_stp = map_dict[prev_step].get(instruct)
            num_steps += 1
            if nxt_stp == "ZZZ":
                zzz_found = True
                break
            else:
                prev_step = nxt_stp
    print(num_steps)


def part2() -> None:
    """What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

    After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

    For example:

    LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)
    Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
    So, in this example, you end up entirely on nodes that end in Z after 6 steps.

    Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?
    """
    lines: list[str] = return_lines("day8.txt")
    seq_instr = lines[0]
    map_dict, prev_nodes = map_paths2(lines[2:])
    total_steps = []
    for pr_node in prev_nodes:
        num_steps = 0
        zzz_found = False
        while not zzz_found:
            for instruct in seq_instr:
                next_node = map_dict[pr_node].get(instruct)
                # next_nodes = [map_dict[node].get(instruct) for node in prev_nodes]
                # end_char = [n[-1] for n in next_nodes]
                num_steps += 1
                if next_node[-1] == "Z":  # len(next_nodes) * ["Z"]
                    zzz_found = True
                    break
                else:
                    pr_node = next_node
        total_steps.append(num_steps)
    # find lcm of the total steps that will be the answer, although i am unsure how this can be unless we believe that the instruction will lead from specific node ending with A to anothe specific node ending with Z. But this is not very clear from the question.


if __name__ == "__main__":
    part2()
