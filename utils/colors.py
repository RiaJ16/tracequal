import colorsys


def calculate_gradient_color(value):
    min_color = (220, 108, 96)   # #dc6c60
    middle_color = (236, 203, 69)  # #eccb45
    max_color = (13, 253, 163)  # #0dfda3

    if value <= 20:
        r = interpolate_color_value(min_color[0], middle_color[0], value * 2)
        g = interpolate_color_value(min_color[1], middle_color[1], value * 2)
        b = interpolate_color_value(min_color[2], middle_color[2], value * 2)
    else:
        r = interpolate_color_value(middle_color[0], max_color[0], (value - 50) * 2)
        g = interpolate_color_value(middle_color[1], max_color[1], (value - 50) * 2)
        b = interpolate_color_value(middle_color[2], max_color[2], (value - 50) * 2)

    return f'rgb({r}, {g}, {b})'


def lighten_rgb_color(rgb_s, factor=0.3):
    rgb_s = rgb_s.lstrip("rgb(").rstrip(")")
    r, g, b = rgb_s.split(", ")
    r = float(r)
    g = float(g)
    b = float(b)
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    new_s = max(min(s * factor, 1.0), 0.0)
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, l, new_s)

    return f'rgb({new_r * 255}, {new_g * 255}, {new_b * 255})'


def interpolate_color_value(min_value, max_value, value):
    return min_value + (max_value - min_value) * (value / 100)
