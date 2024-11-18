def calc_hex_code():
    global k, h
    interval = min(k, h) * 255 / pow(k, h)
    global col_b, col_g, col_r
    if col_r == 255 and 0 <= col_g < 255 and col_b == 0:
        col_g += interval
        if col_g > 255:
            col_g = 255
    elif 0 < col_r <= 255 and col_g == 255 and col_b == 0:
        col_r -= interval
        if col_r < 0:
            col_r = 0
    elif 0 == col_r and col_g == 255 and 0 <= col_b < 255:
        col_b += interval
        if col_b > 255:
            col_b = 255
    elif 0 == col_r and 0 < col_g <= 255 and col_b == 255:
        col_g -= interval
        if col_g < 0:
            col_g = 0
    elif 0 <= col_r < 255 and 0 == col_g and col_b == 255:
        col_r += interval
        if col_r > 255:
            col_r = 255
    elif col_r == 255 and col_g == 0 and 0 < col_b <= 255:
        col_b -= interval
        if col_b < 0:
            col_b = 0
    return "#" + ('%02x%02x%02x' % (round(col_r), round(col_g), round(col_b)))


def print_statistics(_minutes, _seconds, l_min, l_max):
    print("########################################")
    print("l_min: " + str(l_min))
    print("l_max: " + str(l_max))
    print("Ratio of resulting drawing: " + str(l_max / l_min))
    print(f"The process took {_minutes:.0f} minutes and {_seconds:.3f} seconds!")

