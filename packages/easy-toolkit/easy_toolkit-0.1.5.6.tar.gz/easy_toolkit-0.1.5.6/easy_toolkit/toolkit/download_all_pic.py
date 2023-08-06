"""
下载页面所有的图片
"""

import os
import asyncio

import requests
from urllib import parse
from lxml import etree
from pyppeteer import launch
import asyncclick as click

from easy_toolkit.utils import MeasuredEventLoop
from easy_toolkit.default_settings import SettingsHandler


@click.command(name="get_all_pic")
@click.option('-u', '--url', required=True, help='url')
async def get_all_pic(url):
    loop = MeasuredEventLoop()
    asyncio.set_event_loop(loop)

    async def real_run(url):
        executable_path = SettingsHandler.read_property("chrome_path")
        launch_args = {}
        if executable_path:
            click.echo(click.style(text="User customer chrome.exe: {}", fg="green").format(executable_path))
            launch_args.update({"executablePath": executable_path})
        else:
            click.echo(click.style(text="Tips: You can set [chrome_path] to assign your chrome.exe", fg='green'))
        # 使用launch方法调用浏览器，其参数可以传递关键字参数也可以传递字典。
        browser = await launch(
            {'headless': True, 'args': ['--disable-infobars', '--window-size=1920,1080', '--no-sandbox']})
        # 打开一个页面
        page = await browser.newPage()
        # await page.setViewport({'width': 1920, 'height': 1080})   # 设置页面的大小
        # 打开链接
        await page.goto(url)
        page_content = await page.content()
        folder = await page.title()
        await page.close()
        await browser.close()
        page = etree.HTML(page_content)
        all_img = page.xpath("//img/@src")

        os.makedirs(folder, exist_ok=True)

        for img in all_img:
            with open(folder + "/" + parse.urlparse(img).path.split("/")[-1], "wb") as f:
                f.write(requests.get(img).content)
        click.echo("save all pictures to ：%s" % (os.path.join(os.getcwd(), folder)))

    loop.run_until_complete(real_run(url))
    loop.close()
