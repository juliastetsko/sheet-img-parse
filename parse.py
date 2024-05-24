import asyncio
import os

import aiohttp
import gspread
from gspread import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO
from PIL import Image

GSPREAD_ACCOUNT_JSON = os.environ["GSPREAD_ACCOUNT_JSON"]
SHEET_LINK = os.environ["GOOGLE_SHEET_LINK"]
WORKSHEET_TITLE = "feed"
BATCH_SIZE = 1000


async def main():
    client = create_gspread_client()
    worksheet = client.open_by_url(SHEET_LINK).worksheet(WORKSHEET_TITLE)
    async with aiohttp.ClientSession(
            raise_for_status=True, connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        for i in range(0, len(worksheet.col_values(1)), BATCH_SIZE):
            start = 2 if i < 2 else i
            end = i + BATCH_SIZE
            await process_images(worksheet, session, start, end)


async def process_images(
        worksheet: Worksheet, session: aiohttp.ClientSession, start: int, end: int
):
    cells_range = f"B{start}:B{end}"
    print(f"Processing range {cells_range}")
    urls = worksheet.col_values(1)[start - 1: end]
    tasks = [get_image_size(session, url) for url in urls]
    image_sizes = await asyncio.gather(*tasks)
    cells = worksheet.range(cells_range)
    for i in range(len(urls)):
        cells[i].value = image_sizes[i]
    worksheet.update_cells(cells)


async def get_image_size(session, url) -> str:
    try:
        async with session.get(url) as response:
            img_data = await response.read()
            img = Image.open(BytesIO(img_data))
            return f"{img.size[0]}x{img.size[1]}"
    except Exception:
        return "-"


def create_gspread_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        GSPREAD_ACCOUNT_JSON, scope
    )
    client = gspread.authorize(creds)
    return client


if __name__ == "__main__":
    asyncio.run(main())
