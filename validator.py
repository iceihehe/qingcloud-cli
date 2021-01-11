import click


def login_mode_union_validate(login_mode, login_keypair, login_passwd):
    if login_mode == "keypair" and not login_keypair:
        raise click.BadParameter("缺失login-keypair")
    if login_mode == "passwd" and not login_passwd:
        raise click.BadParameter("缺失login-passwd")
