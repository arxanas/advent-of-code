def split_line_groups(input: str) -> list[str]:
    """Split the input into groups of lines separated by blank lines."""
    return input.strip().split("\n\n")
