"""
@Project ：convenient_toolkit 
@File ：upload.py.py
@Author ：dengrunting
@Date ：2022/2/10 12:02 
@Desc : 上传文件到github
"""
import asyncclick as click

from easy_toolkit.manager import GithubManager


@click.command(name="upload")
@click.option('-f', '--file', required=True, help='Your file path')
@click.option('-m', '--message', default="", help='commit message')
@click.option('-n', '--name', default="", help='file name.')
@click.option('-s', '--source', default="github", help='文件存储源，默认为【github】')
async def picture_file_command(file, message, name, source):
    if source == "github":
        manager = GithubManager()
    else:
        click.echo("{}".format("目前只支持github作为源"))
        return
    file_raw_url = manager.upload_to_github(file, message, name, check_image=False)
    click.echo("{}".format(file_raw_url))

