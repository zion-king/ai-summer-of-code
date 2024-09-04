def printer(message, color="white"):
    color_codes = {
        "orange": "\033[0;31m",
        "sky_blue": "\033[0;36m",
        "red": "\033[0;31m",
        "cyan": "\033[0;32m",
        "teal": "\033[0;36m",
        "yellow": "\033[0;33m",
        "blue": "\033[0;34m",
        "purple": "\033[0;35m",
        "cyan": "\033[0;36m",
        "white": "\033[0;37m",
        "gold": "\033[1;33m",  # Adding gold color
        "bold_black": "\033[1;30m",
        "bold_red": "\033[1;31m",
        "bold_green": "\033[1;32m",
        "bold_yellow": "\033[1;33m",
        "bold_blue": "\033[1;34m",
        "bold_purple": "\033[1;35m",
        "bold_cyan": "\033[1;36m",
        "bold_white": "\033[1;37m",
        "reset": "\033[0m",
    }

    color_code = color_codes.get(color.lower(), color_codes["white"])

    # Apply color using ANSI escape codes
    colored_message = f"{color_code}{message}{color_codes['reset']}"

    # Print the colored message
    print(colored_message)