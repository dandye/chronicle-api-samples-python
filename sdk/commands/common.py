"""Common utilities for CLI commands."""

import os
from functools import wraps

import click
from dotenv import load_dotenv


def get_env_value(key, default=None):
    """Get value from environment variable with Chronicle prefix."""
    return os.getenv(f"CHRONICLE_{key}", default)


def add_common_options(func):
    """Add common options to a command."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Load environment variables from .env file
        load_dotenv()

        # If options not provided via CLI, try to get from environment
        if not kwargs.get("credentials_file"):
            kwargs["credentials_file"] = get_env_value("CREDENTIALS_FILE")
        if not kwargs.get("project_id"):
            kwargs["project_id"] = get_env_value("PROJECT_ID")
        if not kwargs.get("project_instance"):
            kwargs["project_instance"] = get_env_value("INSTANCE")
        if not kwargs.get("region"):
            kwargs["region"] = get_env_value("REGION")

        return func(*args, **kwargs)

    # Add CLI options
    wrapper = click.option(
        "--credentials-file",
        required=False,
        help="Path to service account credentials file. Can also be set via CHRONICLE_CREDENTIALS_FILE env var.",
    )(wrapper)
    wrapper = click.option(
        "--project-id",
        required=False,
        help="GCP project id or number. Can also be set via CHRONICLE_PROJECT_ID env var.",
    )(wrapper)
    wrapper = click.option(
        "--project-instance",
        required=False,
        help="Customer ID (uuid with dashes) for the Chronicle instance. Can also be set via CHRONICLE_INSTANCE env var.",
    )(wrapper)
    wrapper = click.option(
        "--region",
        required=False,
        help="Region in which the target project is located. Can also be set via CHRONICLE_REGION env var.",
    )(wrapper)

    # Ensure required options are provided either via CLI or environment
    @wraps(wrapper)
    def validate_options(*args, **kwargs):
        missing = []
        if not kwargs.get("credentials_file"):
            missing.append("credentials-file (or CHRONICLE_CREDENTIALS_FILE)")
        if not kwargs.get("project_id"):
            missing.append("project-id (or CHRONICLE_PROJECT_ID)")
        if not kwargs.get("project_instance"):
            missing.append("project-instance (or CHRONICLE_INSTANCE)")
        if not kwargs.get("region"):
            missing.append("region (or CHRONICLE_REGION)")

        if missing:
            raise click.UsageError(
                f"Missing required options: {', '.join(missing)}\n"
                "These can be provided via command line options or environment variables."
            )

        return wrapper(*args, **kwargs)

    return validate_options
