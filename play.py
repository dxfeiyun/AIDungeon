from story.story_manager import *
from generator.gpt2.gpt2_generator import *
from story.utils import *
from story.custom_story import *
from termios import tcflush, TCIFLUSH
import time,sys

def select_game():
    print("Which game would you like to play?")
    options = ["zombies", "hospital", "apocalypse", "classic", "knight", "necromancer", "custom"]
    for i, option in enumerate(options):
        console_print(str(i) + ") " + option + "\n")

    choice = get_num_options(len(options))
    if options[choice] == "custom":
        context, prompt = make_custom_story()

    else:
        game = options[choice]
        prompt = get_story_start(game)
        context = get_context(game)

    return context, prompt

def instructions():
    text = "\nAI Dungeon 2 Instructions:"
    text += '\n* Enter actions starting with a verb ex. "go to the tavern" or "attack the orc."'
    text += '\n* If you want to say something then enter \'say "(thing you want to say)"\''
    text += '\n* Finally if you want to end your game and start a new one just enter "restart" for any action. '
    return text


def play_aidungeon_2():

    save_story = input("Help improve AIDungeon by enabling story saving? (Y/n) ")
    if save_story.lower() in ["no", "No", "n"]:
        upload_story = True
    else:
        upload_story = True

    print("\nInitializing AI Dungeon! (This might take a few minutes)\n")
    generator = GPT2Generator()
    story_manager = UnconstrainedStoryManager(generator)
    print("\n\n\n\n")

    with open('opening.txt', 'r') as file:
        starter = file.read()
    print(starter)

    while True:

        print("\n\n")
        context, prompt = select_game()
        console_print(instructions())

        story_manager.start_new_story(prompt, context=context)

        print("\n")
        console_print(context + str(story_manager.story))
        while True:
            tcflush(sys.stdin, TCIFLUSH)
            action = input("> ")
            if action == "restart":
                if upload_story:
                    rating = input("Please rate the story quality from 1-10: ")
                    try:
                        rating_float = float(rating)
                        story_manager.story.rating = rating_float
                        story_manager.story.save_to_storage()
                    except:
                        pass
                break

            if action != "" and action.lower() != "continue":
                action = action.strip()

                action = first_to_second_person(action)

                if "You" not in action:
                    action = "You " + action

                if action[-1] not in [".", "?", "!"]:
                    action = action + "."

                action = "\n> " + action + "\n"
                # action = remove_profanity(action)
                #action = first_to_second_person(action)

            result = "\n" + story_manager.act(action)

            if upload_story:
                story_manager.story.save_to_storage()

            if player_died(result):
                console_print(result + "\nGAME OVER")
                break
            elif player_won(result):
                console_print(result + "\n CONGRATS YOU WIN")
            else:
                console_print(result)


if __name__ == '__main__':
    play_aidungeon_2()

