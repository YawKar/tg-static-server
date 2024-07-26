from aiogram.filters.command import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, InaccessibleMessage
from aiogram.utils.formatting import Code
from aiogram import Dispatcher, Bot
import pathlib
import markup
import callback
import logging


dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def command_start(message: Message, root_dir: pathlib.Path) -> None:
    await message.answer(
        **Code(root_dir.as_posix()).as_kwargs(),
        reply_markup=markup.mk_file_browser_markup(root_dir),
    )


@dispatcher.callback_query(callback.ChangeDirCallback.filter())
async def callback_change_dir(
    query: CallbackQuery,
    callback_data: callback.ChangeDirCallback,
    bot: Bot,
    root_dir: pathlib.Path,
) -> None:
    if (
        query.message is None
        or isinstance(query.message, InaccessibleMessage)
        or query.message.reply_markup is None
    ):
        logging.error(
            f"{query.from_user.username=} {query.chat_instance=} {query.message=}"
        )
        query.answer(text="An error occurred.")
        return
    relative_path: str | pathlib.Path | None = markup.find_relative_path_by_hash(
        query.message.reply_markup, callback_data.relative_path_hash
    )
    if relative_path is None:
        logging.error(
            f"relative_path is None for {query.from_user.username=} {query.chat_instance=} {query.inline_message_id=}"
        )
        query.answer(text="An error occurred.")
        return
    relative_path = pathlib.Path(relative_path)
    if query.message.text is None:
        logging.error(
            f"{query.message.text=} for {query.from_user.username=} {query.chat_instance=} {query.inline_message_id=}"
        )
        query.answer(text="An error occurred.")
        return
    current_path: pathlib.Path = pathlib.Path(query.message.text)
    if relative_path == pathlib.Path("../"):
        new_path: pathlib.Path = current_path.parent
    else:
        new_path: pathlib.Path = current_path / relative_path
    if not new_path.is_relative_to(root_dir):
        await query.answer(text="You cannot go further up.")
        return
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        **Code(new_path).as_kwargs(),
        reply_markup=markup.mk_file_browser_markup(new_path),
    )
    await query.answer()


@dispatcher.callback_query(callback.DownloadFileCallback.filter())
async def callback_download_file(
    query: CallbackQuery,
    callback_data: callback.DownloadFileCallback,
    bot: Bot,
    root_dir: pathlib.Path,
):
    if (
        query.message is None
        or isinstance(query.message, InaccessibleMessage)
        or query.message.reply_markup is None
    ):
        logging.error(
            f"{query.from_user.username=} {query.chat_instance=} {query.message=}"
        )
        query.answer(text="An error occurred.")
        return
    relative_path: str | pathlib.Path | None = markup.find_relative_path_by_hash(
        query.message.reply_markup, callback_data.relative_path_hash
    )
    if relative_path is None:
        logging.error(
            f"relative_path is None for {query.from_user.username=} {query.chat_instance=} {query.inline_message_id=}"
        )
        query.answer(text="An error occurred.")
        return
    relative_path = pathlib.Path(relative_path)
    if query.message.text is None:
        logging.error(
            f"{query.message.text=} for {query.from_user.username=} {query.chat_instance=} {query.inline_message_id=}"
        )
        query.answer(text="An error occurred.")
        return
    current_path: pathlib.Path = pathlib.Path(query.message.text)
    file_path = current_path / relative_path
    if not file_path.is_relative_to(root_dir):
        query.answer(text="You cannot go further up.")
        return
    if not file_path.is_file():
        logging.error(
            f"{file_path.is_file()=} for {query.from_user.username=} {query.chat_instance=} {query.inline_message_id=}"
        )
        query.answer(text="An error occurred.")
        return
    file: FSInputFile = FSInputFile(
        file_path,
        filename=file_path.name,
    )
    await bot.send_document(
        chat_id=query.message.chat.id,
        document=file,
    )
    await query.answer()
