import toml


class ConfigLoadError(Exception):
    pass


def load_config_file(file_path: str):
    try:
        with open(file_path, "r") as config_file:
            config = toml.load(config_file)
        return config
    except (FileNotFoundError, toml.TomlDecodeError) as e:
        raise ConfigLoadError(f"Error loading config file: {file_path}") from e


def tokens_to_chars(token_count: int):
    """Estimate the approximate character count based on a given token count."""
    avg_token_length = 4
    char_count = token_count * avg_token_length

    return char_count


def make_bold(text: str):
    return f"\033[1m{text}\033[0m"
