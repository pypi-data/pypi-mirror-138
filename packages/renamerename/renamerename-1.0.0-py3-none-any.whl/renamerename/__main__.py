"""RenameRename entrypoint script"""

import sys
from renamerename.executor import app


def main():
    sys.exit(app.run())


if __name__ == "__main__":
    main()
