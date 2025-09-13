from nextcord.ext import commands


def has_any_role(role_ids):
    async def predicate(ctx):
        return any(role.id in role_ids for role in ctx.author.roles)

    return commands.check(predicate)
