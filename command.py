import click

from error import LoadConfigError
from sdk import QingCloudApi
from util import save_config
from validator import login_mode_union_validate


@click.group()
def cli():
    pass


@cli.command()
@click.option("--access-key-id", help="申请的API密钥ID")
@click.option("--secret-access-key", help="申请的API密钥secret key")
def config(access_key_id, secret_access_key):
    save_config(access_key_id=access_key_id, secret_access_key=secret_access_key)
    click.echo("密钥ID配置成功")


@cli.command()
@click.argument("image_id")
@click.argument("login_mode", type=click.Choice(["keypair", "passwd"]))
@click.argument("zone", type=click.Choice(["pek3", "pek3a", "pek3b", "gd2", "sh1a", "ap2a"], case_sensitive=True))
@click.option("--instance-type", help="主机类型")
@click.option("--login-keypair", help="登录密钥ID")
@click.option("--login-passwd", help="登录密码")
@click.option("--cpu", help="CPU核心", type=click.Choice(["1", "2", "4", "8", "16"]))
@click.option("--memory", help="内存", type=click.Choice(["1024", "2048", "4096", "6144", "8192", "12288", "16384", "24576", "32768"]))
def run_instances(image_id, login_mode, zone, instance_type, login_keypair, login_passwd, cpu, memory):
    """
    创建指定配置，指定数量的主机

    IMAGE_ID 映像ID，此映像将作为主机的模板。可传青云提供的映像ID，或自己创建的映像ID

    LOGIN_MODE 指定登录方式

    ZONE 区域 ID，注意要小写
    """
    try:
        login_mode_union_validate(login_mode, login_keypair, login_passwd)
    except click.BadParameter as e:
        click.echo(e)
        return

    if cpu:
        cpu = int(cpu)

    if memory:
        memory = int(memory)

    try:
        qing_obj = QingCloudApi()
    except LoadConfigError as e:
        click.echo(e)
        return
    click.echo(f"创建主机请求发送中...")
    resp = qing_obj.run_instances(
        image_id, login_mode, zone,
        instance_type=instance_type, login_keypair=login_keypair, login_passwd=login_passwd, cpu=cpu, memory=memory
    )
    click.echo(f"创建主机请求发送成功，平台返回\n**************\n{resp}")


@cli.command()
@click.argument("zone", type=click.Choice(["pek3", "pek3a", "pek3b", "gd2", "sh1a", "ap2a"], case_sensitive=True))
@click.option("--instance-id", help="主机ID", multiple=True)
@click.option("--instance-class", type=click.Choice(["0", "1", "101", "201"]), help="主机ID")
def describe_instances(zone, instance_id, instance_class):
    """
    获取一个或多个主机

    ZONE 区域 ID，注意要小写
    """
    if instance_class:
        instance_class = int(instance_class)

    try:
        qing_obj = QingCloudApi()
    except LoadConfigError as e:
        click.echo(e)
        return

    click.echo(f"获取主机请求发送中...")
    resp = qing_obj.describe_instances(
        zone,
        instances__n=instance_id or None,
        instance_class=instance_class
    )
    click.echo(f"获取主机请求发送成功，结果如下\n****************\n{resp}")


@cli.command()
@click.argument("zone", type=click.Choice(["pek3", "pek3a", "pek3b", "gd2", "sh1a", "ap2a"], case_sensitive=True))
@click.option("--instance-id", help="主机ID", multiple=True)
@click.option("--direct-cease", type=click.Choice(["0", "1"]), help="1/0 直接销毁/进入回收站")
def terminate_instances(zone, instance_id, direct_cease):
    """
    获取一个或多个主机

    ZONE 区域 ID，注意要小写
    """
    if direct_cease:
        direct_cease = int(direct_cease)

    try:
        qing_obj = QingCloudApi()
    except LoadConfigError as e:
        click.echo(e)
        return

    click.echo(f"销毁主机请求发送中...")
    resp = qing_obj.terminate_instances(
        zone,
        instances__n=instance_id or None,
        direct_cease=direct_cease
    )
    click.echo(f"销毁主机请求发送成功，结果如下\n****************\n{resp}")


if __name__ == '__main__':
    cli()
