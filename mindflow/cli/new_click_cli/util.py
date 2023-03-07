import click


def passthrough_command(*command_args, **command_kwargs):
    # this function is a decorator that takes the input function and wraps it
    def _decorator(func):
        context_settings = command_kwargs.get("context_settings", {})

        if "ignore_unknown_options" in context_settings:
            raise ValueError(
                "The context_settings argument already has an entry for 'ignore_unknown_options'"
            )

        dec1 = click.command(
            *command_args,
            context_settings=dict(context_settings, ignore_unknown_options=True),
            **command_kwargs
        )

        dec2 = click.argument("args", nargs=-1, type=click.UNPROCESSED)

        func = dec1(func)
        func = dec2(func)
        return func

    return _decorator
