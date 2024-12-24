from enum import StrEnum


class Styles(StrEnum):
    """Basic formatting styles."""
    OFF = '\033[0m'

    # Text styles.
    BOLD = '\033[1m'
    ITALIC = '\x1b[3m'
    UNDERSCORE = '\033[4m'

    # Text colors.
    TEXT_BLACK = '\033[30m'
    TEXT_RED = '\033[31m'
    TEXT_GREEN = '\033[32m'
    TEXT_YELLOW = '\033[33m'
    TEXT_BLUE = '\033[34m'
    TEXT_MAGENTA = '\033[35m'
    TEXT_CYAN = '\033[36m'
    TEXT_WHITE = '\033[37m'

    # Background colors.
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class Logger:
    """A class for pretty terminal print."""

    @staticmethod
    def print(msg: str, styles: list[Styles], end: str = '\n'):
        """Prints text with applied styles.

        Args:
            msg: Message to print.
            styles: List of styles to apply.
            end: String appended after the last value, default a newline.
        """
        style = ''.join(styles)
        print(style + msg + Styles.OFF, end=end)

    @staticmethod
    def info(msg, end: str = '\n'):
        """Prints informational message.

        Args:
            msg: Message to print.
            end: String appended after the last value, default a newline.
        """
        print(str(msg), end=end)

    @staticmethod
    def success(msg, end: str = '\n'):
        """Prints success message.

        Args:
            msg: Message to print.
            end: String appended after the last value, default a newline.
        """
        Logger.print(str(msg), [Styles.TEXT_GREEN], end=end)

    @staticmethod
    def warning(msg, end: str = '\n'):
        """Prints warning message.

        Args:
            msg: Message to print.
            end: String appended after the last value, default a newline.
        """
        Logger.print(str(msg), [Styles.TEXT_YELLOW, Styles.BOLD], end)

    @staticmethod
    def error(msg, end: str = '\n'):
        """Prints warning message.

        Args:
            msg: Message to print.
            end: String appended after the last value, default a newline.
        """
        Logger.print(str(msg), [Styles.TEXT_RED, Styles.BOLD], end=end)
