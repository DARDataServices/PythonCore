import os

def get_env_var(key):
    """Get environment variable with error handling."""
    value = os.getenv(key.upper())
    if value is None:
        raise EnvironmentError(f"Missing environment variable: {key}")
    return value
