import sys

from .cli import main
from .gui import run_gui


if __name__ == "__main__":
    if "--gui" in sys.argv:
        sys.argv.remove("--gui")
        run_gui()
        raise SystemExit(0)

    raise SystemExit(main())
