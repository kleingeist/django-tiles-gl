def split_floats(input, sep=","):
    return [float(val.strip()) for val in input.split(sep)]


def center_from_bounds(bounds, zoom):
    return [(bounds[0] + bounds[2]) / 2.0, (bounds[1] + bounds[3]) / 2.0, zoom]
