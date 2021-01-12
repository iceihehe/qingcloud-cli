import click


def login_mode_union_validate(login_mode, login_keypair, login_passwd):
    if login_mode == "keypair" and not login_keypair:
        raise click.BadParameter("缺失login-keypair")
    if login_mode == "passwd" and not login_passwd:
        raise click.BadParameter("缺失login-passwd")


def instance_type_union_validate(instance_type, cpu, memory):
    if not instance_type and not all([cpu, memory]):
        raise click.BadParameter("缺少必要CPU内存参数")
