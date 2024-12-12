def convert_to_bounds(range_str):
    """
    Converts a string a share range into a tuple of lower and upper bounds.

    Cases:
        - "50-67%" -> (50, 67)
        - "100%" -> (100, 100)
        - "<5%" -> (0, 5)

    Args:
        range_str (str): The range string in the format 'lower-upper%', 'value%', or '<value%'.

    Returns:
        tuple: A tuple of (lower_bound, upper_bound) as integers.
    """
    clean_str = range_str.replace('%', '').strip()

    if '-' in clean_str:
        lower, upper = map(lambda x: int(x) / 100, clean_str.split('-'))
        return lower, upper
    elif clean_str.startswith('<'):
        upper = int(clean_str[1:]) / 100
        # Assume 0 is lower bound in this case
        return 0, upper
    else:
        value = int(clean_str) / 100
        return value, value
