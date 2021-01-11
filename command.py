import click

from sdk import QingCloudApi
from util import save_config


@click.group()
def cli():
    pass

@cli.command()
@click.option("--access_key_id", help="申请的API密钥ID")
def config(access_key_id):
    save_config(access_key_id)
    click.echo("密钥ID配置成功")

@cli.command()
@click.argument("instance_id")
def run(instance_id):

    qing_obj = QingCloudApi()
    qing_obj.run_instances(instance_id)


if __name__ == '__main__':
    cli()
