from __future__ import annotations

import sys

from tag.core.game import Game


def main() -> None:
    game = Game()
    if "--smoke-test" in sys.argv:
        game.smoke_test()
    else:
        game.run()


if __name__ == "__main__":
    main()
