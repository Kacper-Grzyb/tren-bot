import random


class Colors:
    color_values = list()
    @staticmethod
    def get_random_color() -> (int, int, int):
        if not Colors.color_values:
            Colors.color_values = list(Colors.COLORS.values())
            random.shuffle(Colors.color_values)

        r, g, b, _ = Colors.color_values.pop()
        return r, g, b

    COLORS = {
        "blue3": (0, 0, 205, 255),
        "chocolate4": (139, 35, 35, 255),
        "cornflowerblue": (100, 149, 237, 255),
        "darkolivegreen": (85, 107, 47, 255),
        "darkorange3": (205, 102, 0, 255),
        "darkred": (139, 0, 0, 255),
        "darkviolet": (148, 0, 211, 255),
        "deeppink2": (205, 16, 118, 255),
        "dodgerblue3": (24, 116, 205, 255),
        "gold2": (238, 201, 0, 255),
        "green3": (0, 205, 0, 255),
        "hotpink4": (139, 58, 98, 255),
        "indigo": (75, 0, 130, 255),
        "khaki4": (139, 134, 78, 255),
        "limegreen": (50, 205, 50, 255),
        "magenta4": (139, 0, 139, 255),
        "orange2": (238, 154, 0, 255),
        "orangered2": (238, 64, 0, 255),
        "red3": (205, 0, 0, 255),
        "seagreen": (46, 139, 87, 255),
        "turquoise4": (0, 128, 128, 255),
        "yellow3": (139, 139, 0, 255),
    }
