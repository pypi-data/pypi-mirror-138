"""
@Project ：convenient_toolkit 
@File ：manager.py.py
@Author ：dengrunting
@Date ：2022/2/10 12:05 
@Desc : 各种manager
"""
import sys
import os
from easy_toolkit.utils import urljoin
import asyncclick as click
import github
import requests
from github import Github

from easy_toolkit.default_settings import SettingsHandler


class GithubManager:
    """github工具类"""

    raw_base_url = r"https://raw.githubusercontent.com/"
    repo_branch = "master"

    def __init__(self, cate="github"):
        if cate == "github":
            # using username and password
            github_token = SettingsHandler.read_property("github_token")
            if not github_token:
                github_username, github_password = \
                    SettingsHandler.read_property("github_username"), SettingsHandler.read_property(
                        "github_password")
                if not all([github_username, github_password]):
                    click.echo(
                        click.style(
                            "Please set [github_token] or [github_username、github_password] before use gitpic!",
                            fg="red"))
                    sys.exit(1)
                else:
                    g = Github(github_username, github_password)
            else:
                g = Github(github_token)
            self.g = g

    def upload_to_github(self, file, message=None, name=None, check_image=True):
        if file.startswith("http"):
            content = requests.get(file).content
        else:
            if not os.path.exists(file):
                click.echo(click.style("File [{}] not exists", fg="red").format(file))
                sys.exit(1)
            if check_image and not is_image(file):
                click.echo(click.style("Please choose a image type file!", fg="red"))
                sys.exit(1)
            content = open(file, 'br').read()

        if not name:
            name = os.path.basename(file)
        if not message:
            message = "add picture {}".format(name)

        repo_name = SettingsHandler.read_property("github_reponame")
        if repo_name is None:
            click.echo(click.style("Please set [github_reponame] before use gitpic!", fg="red"))
            sys.exit(1)

        picture_repo = self.g.get_repo(repo_name)
        try:
            ret = picture_repo.create_file(path=name,
                                           message=message,
                                           content=content,
                                           branch="master")["content"]
        except github.GithubException as e:
            if e.status == 422:
                # 文件名 已经存在 返回存在文件的路径
                click.echo(click.style("file [{}] already exists!", fg="red").format(name))
                ret = picture_repo.get_contents(name)
            else:
                click.echo(e)
                sys.exit(1)
        file_raw_url = urljoin(self.raw_base_url, repo_name, self.repo_branch, ret.path)
        return file_raw_url