"""Common utilities for CLI commands."""

import click


def add_common_options(func):
    """Add common options to a command."""
    func = click.option(
        "--credentials-file",
        required=True,
        help="Path to service account credentials file.",
    )(func)
    func = click.option(
        "--project-id",
        required=True,
        help="GCP project id or number to which the target instance belongs.",
    )(func)
    func = click.option(
        "--project-instance",
        required=True,
        help="Customer ID (uuid with dashes) for the Chronicle instance.",
    )(func)
    func = click.option(
        "--region",
        required=True,
        help="Region in which the target project is located.",
    )(func)
    return func
