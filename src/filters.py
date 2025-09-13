from nextcord.ext import commands

"""
Функция декоратор для проверки есть ли у пользователя одна из предоставленных ролей.

Аргументы:
    role_ids - массив из int значений, ID дискорд ролей.
Возвращает:
    Декоратор проверки для класса Command и его подклассов.
"""


def has_any_role(role_ids):
    async def predicate(ctx):
        return any(role.id in role_ids for role in ctx.author.roles)

    return commands.check(predicate)
