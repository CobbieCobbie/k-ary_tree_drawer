def calc_hex_code(step: int, total_steps: int) -> str:
    """Return a hex colour string that cycles through the RGB colour wheel.

    The colour wheel is divided into *total_steps* equal intervals so that the
    full spectrum is traversed regardless of tree size.  *step* is the
    zero-based index of the node being coloured (0 → root).

    The wheel has six segments (R→Y, Y→G, G→C, C→B, B→M, M→R) each spanning
    255 units, giving 1530 total units.  We map *step/total_steps* onto that
    range and decompose back into (r, g, b).
    """
    if total_steps <= 1:
        return "#ff0000"

    # normalise step to [0, 1530)
    pos = (step / total_steps) * 1530
    segment, offset = divmod(pos, 255)
    segment = int(segment) % 6
    offset = int(round(offset))

    if segment == 0:   # red → yellow  (g rises)
        r, g, b = 255, offset, 0
    elif segment == 1: # yellow → green  (r falls)
        r, g, b = 255 - offset, 255, 0
    elif segment == 2: # green → cyan  (b rises)
        r, g, b = 0, 255, offset
    elif segment == 3: # cyan → blue  (g falls)
        r, g, b = 0, 255 - offset, 255
    elif segment == 4: # blue → magenta  (r rises)
        r, g, b = offset, 0, 255
    else:              # magenta → red  (b falls)
        r, g, b = 255, 0, 255 - offset

    return "#" + "%02x%02x%02x" % (
        max(0, min(255, r)),
        max(0, min(255, g)),
        max(0, min(255, b)),
    )


def print_statistics(
    _minutes: int,
    _seconds: float,
    l_min: float,
    l_max: float,
) -> None:
    print("########################################")
    print(f"l_min: {l_min}")
    print(f"l_max: {l_max}")
    print(f"Ratio of resulting drawing: {l_max / l_min}")
    print(f"The process took {_minutes:.0f} minutes and {_seconds:.3f} seconds!")
