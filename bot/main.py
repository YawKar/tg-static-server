import typer
from typing import Annotated
from dispatcher import dispatcher
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
import logging
import pathlib


async def main(bot: Bot, root_dir: pathlib.Path) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(
        bot,
        root_dir=root_dir,
    )


def cli_main(
    api_token: Annotated[str, typer.Option(help="Telegram bot API token")],
    root_dir: Annotated[pathlib.Path, typer.Option(help="Root directory to serve")],
) -> None:
    bot = Bot(token=api_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.run(main(bot, root_dir))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    typer.run(cli_main)
