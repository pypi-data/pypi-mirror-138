import io
from os.path import dirname

from httpx import AsyncClient
from lxml import etree
from nonebot import require

new_page = require("nonebot_plugin_htmlrender").get_new_page


async def get_tvseries(week: str = None) -> bytes:
    url = "https://huo720.com/calendar"

    # if week:
    #     url += f"?{parse_week(week)}"

    async with AsyncClient() as client:
        res = await client.get(url)
        result = parse_data(res.text)
        if __name__ == "__main__":
            with open("./test/out.html", "w+") as f:
                f.write(result)
    image = await create_image(result)
    return image


def parse_date(date: str = None) -> str:
    import datetime

    now = datetime.datetime.now()
    return now.strftime(r"%Y-%m-%d")


def parse_data(content: str) -> str:
    with open(dirname(__file__) + "/css.css", "r") as f:
        css = f.read()

    dom = etree.HTML(content)
    result = dom.xpath(f'//*[@id="{parse_date()}"]')[0]

    html_init = f"""<html><head><meta charset="utf-8"><style type="text/css">{css}</style></head><body><div id="main-container"></div></body></html>"""
    new_dom = etree.HTML(html_init)
    container = new_dom.xpath("//body/div")[0]

    container.append(result)
    html = etree.tostring(new_dom, encoding="utf-8", method="html").decode()

    return html


async def create_image(html: str, wait: int = 0) -> bytes:
    async with new_page(viewport={"width": 1200, "height": 600}) as page:
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(wait)
        img_raw = await page.screenshot(full_page=True)
    return img_raw


if __name__ == "__main__":
    print("Testing...")
    import asyncio
    from PIL import Image

    img_bytes = asyncio.run(get_tvseries(week="一"))
    img = Image.open(io.BytesIO(img_bytes))
    img.save("./test/out.png")
