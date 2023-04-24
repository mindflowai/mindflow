import click


def passthrough_command(*command_args, **command_kwargs):
    """Just like the @click.command decorator, but allows all args to pass through (for wrapper cli commands)."""

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


# def overloaded_option(*option_args, **option_kwargs):
# if message is not None:
#     click.echo(
#         f"Warning: Using message '{message}' instead of mindflow generated message."
#     )
#     click.echo("It's recommended that you don't use the -m/--message flag.")


# @click.option(
#     "-m",
#     "--message",
#     help="Don't use mindflow to generate a commit message, use this one instead.",
#     default=None,
# )

# def _decorator(func):
#     dec1 = click.option(*option_args, **option_kwargs)

#     func = dec1(func)
#     print(func)
#     # option_name = func.params[-1].name
#     option_name = func.__click_params__[-1].name

#     def wrapped_func(**kwargs):
#         if option_name in kwargs:
#             v = kwargs[option_name]
#             click.echo(
#                 f"Warning: MindFlow overrides {option_name}, but since you passed in it's value as '{v}', that will be used instead."
#             )
#             click.echo("We recommend not overriding options, but we understand sometimes it's necessary.")

#         return func(**kwargs)

#     return wrapped_func

# return _decorator
