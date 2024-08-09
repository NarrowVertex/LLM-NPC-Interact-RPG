import argparse
from DataLoader import load_game_from_yaml


try:
    game
except NameError:
    game = load_game_from_yaml("test/game/HeroAndDemonKingGame")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="System run arguments")
    parser.add_argument('--debug', action='store_true', help="Debug mod flag")

    args = parser.parse_args()

    print("[===================================================]")
    print(f"               [{game.game_name}]")
    print(f"     {game.game_description}")
    print("[===================================================]")

    if not args.debug:
        while True:
            game.start_turn()
    else:
        game.test_entity_conversation()
