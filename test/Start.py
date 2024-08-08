import argparse
from Game import HeroAndDemonKingGame

game = HeroAndDemonKingGame()


if __name__ == '__main__':
    game.game_init()

    parser = argparse.ArgumentParser(description="System run arguments")
    parser.add_argument('--debug', action='store_true', help="Debug mod flag")

    args = parser.parse_args()

    if not args.debug:
        while True:
            game.start_turn()
    else:
        game.test_entity_conversation()
