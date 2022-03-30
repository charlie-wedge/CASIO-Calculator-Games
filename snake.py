# code written by Charlie Wedge

import random
import math

empty = "-"
snake = "X"
apple = "@"
direction_characters = ["^", "v", "<", ">"]
horizontal = 10  # 10 for the calculator
vertical = 6  # 6 for the calculator

positions_x = [0]
positions_y = [0]
apple_position = [0, 0]
direction = 1


increase_in_next_frame = False
game_is_running = True


def play_game():
    # these controls can be changed if playing on computer rather than calculator:
    up = "8"  # w / 8
    down = "2"  # s / 2
    left = "4"  # a / 4
    right = "6"  # d / 6
    terminate = "."

    check_apple()

    while game_is_running:
        global direction
        global increase_in_next_frame

        temp_positions = [positions_x[0], positions_y[0]]
        user_input = input()  # they gotta spam enter for this to work

        if user_input == up:
            temp_positions[1] -= 1
            direction = 0
        elif user_input == down:
            temp_positions[1] += 1
            direction = 1
        elif user_input == left:
            temp_positions[0] -= 1
            direction = 2
        elif user_input == right:
            temp_positions[0] += 1
            direction = 3
        elif user_input == terminate:
            display_end_screen("Game finished", "Your score is {}".format(len(positions_x)))
            return
        else:
            print_frame()
            continue

        # see if we've hit the edge wall, and if so, move these head to the opposite wall:
        if temp_positions[0] > horizontal-1:  # hit the right wall
            temp_positions[0] = 0
        elif temp_positions[0] < 0:  # hit the left wall
            temp_positions[0] = horizontal-1
        elif temp_positions[1] > vertical-1:  # hit the bottom wall
            temp_positions[1] = 0
        elif temp_positions[1] < 0:  # hit the top wall:
            temp_positions[1] = vertical-1

        if increase_in_next_frame:
            increase_in_next_frame = False
            #  increases the len of positions by inserting new indexes at the beginning
            positions_x.insert(0, temp_positions[0])
            positions_y.insert(0, temp_positions[1])
        else:
            #  push everything back by one:
            for p in range(len(positions_x)-1):
                positions_x[len(positions_x) - (1+p)] = positions_x[len(positions_x) - (2+p)]
                positions_y[len(positions_y) - (1+p)] = positions_y[len(positions_y) - (2+p)]
            # write the new positions:
            positions_x[0] = temp_positions[0]
            positions_y[0] = temp_positions[1]

        if has_crashed(positions_x, positions_y):
            display_end_screen("GAME OVER", "Your score is {}".format(len(positions_x)))
            return

        check_apple()
        if not game_is_running:
            return

        print_frame()


def has_crashed(pos_x, pos_y):
    head_x = pos_x[0]
    head_y = pos_y[0]

    for a in range(1, len(pos_x)):  # could also be len(pos_y)
        if head_x == pos_x[a] and head_y == pos_y[a]:
            return True
    return False


def print_frame():
    for v in range(vertical):  # for every vertical
        str_out = ""
        for h in range(horizontal):  # for every horizontal
            # print either empty or snake dependent on positions[]
            is_match = False
            is_head = False
            is_apple = False
            for n in range(len(positions_x)):  # search if there's a snake in this position
                if h == positions_x[n] and v == positions_y[n]:  # if it's a match
                    is_match = True
                    if n == 0:  # need to know for if we should draw an arrow at this one
                        is_head = True
                if check_if_apple(h, v):
                    is_apple = True

            if is_apple:
                str_out += apple
            else:
                if is_match:
                    if is_head:
                        str_out += direction_characters[direction]
                    else:
                        str_out += snake
                else:
                    str_out += empty

            str_out += " "
        print(str_out)  # print to screen


def check_apple():
    if check_if_apple(positions_x[0], positions_y[0]):
        global increase_in_next_frame
        global game_is_running

        # is the game complete?:
        if len(positions_x) >= (horizontal * vertical):
            game_is_running = False
            display_end_screen("YOU WIN!", "You scored {}!".format(len(positions_x)))
            return
        # come up with a new apple position:
        else:
            found_position = False  # declaration
            while not found_position:  # the above if statement should prevent this from halting
                rand_x = random.randint(0, horizontal-1)
                rand_y = random.randint(0, vertical-1)
                if not check_if_snake(rand_x, rand_y):  # we're good tso spawn an apple here
                    apple_position[0] = rand_x
                    apple_position[1] = rand_y
                    found_position = True

            increase_in_next_frame = True


# check if the apple is in position x, y
def check_if_apple(x, y):
    if apple_position[0] == x and apple_position[1] == y:
        return True
    return False


def check_if_snake(x, y):
    for a in range(len(positions_x)):  # could also be len(positions_y)
        if positions_x[a] == x and positions_y[a] == y:
            return True
    return False


def display_end_screen(message_one, message_two):
    # check if we can actually format it nicely with the given variables
    if vertical < 4 or (horizontal*2)-2 <= len(message_one) or (horizontal*2)-2 <= len(message_two):
        print(message_one)
        print(message_two)
        return

    print(return_end_screen_across())  # +-----+
    print(return_end_screen_text(message_one))  # |  Game over!  |
    print(return_end_screen_text(message_two))  # | Score is: 21 |

    for y in range(vertical-4):
        end_str = "|"
        for x in range((horizontal-2)*2):
            end_str += " "
        end_str += "|"
        print(end_str)  # |     |

    print(return_end_screen_across())  # +-----+


def return_end_screen_text(text):
    end_str = "|"
    centre_position = (horizontal-2) - (len(text)/2)
    for x in range(math.floor(centre_position)):
        end_str += " "
    end_str += text
    for x in range(math.ceil(centre_position)):
        end_str += " "
    end_str += "|"
    return end_str;


def return_end_screen_across():
    end_str = "+"
    for x in range((horizontal-2)*2):
        end_str += "-"
    end_str += "+"
    return end_str  # +-----+


print_frame()
play_game()

