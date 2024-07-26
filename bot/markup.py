import pathlib
import re
from itertools import chain
from humanize.filesize import naturalsize
import callback
from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hash_functions import mk_base85_hash


def find_relative_path_by_hash(
    inlineKbdMarkup: InlineKeyboardMarkup,
    hash: str,
) -> str | None:
    # Need to find the corresponding path mentioned in one of the visible inline keyboard buttons
    # "📁relative_path/"
    dir_pattern = r"📁(.+)/"
    # "📄relative_path (size)"
    file_pattern = r"📄(.+) \("
    for button in chain(*inlineKbdMarkup.inline_keyboard):
        if (match := re.match(dir_pattern, button.text)) is not None and mk_base85_hash(
            match.group(1)
        ) == hash:
            return match.group(1)
        elif (
            match := re.match(file_pattern, button.text)
        ) is not None and mk_base85_hash(match.group(1)) == hash:
            return match.group(1)
    return


def mk_file_browser_markup(root: pathlib.Path) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    sub_dirs: list[pathlib.Path] = [
        root.parent  # initialize with the parent so ../ will be in the list by default
    ]
    sub_files: list[pathlib.Path] = []
    for child in root.iterdir():
        if child.is_dir():
            sub_dirs.append(child)
        elif child.is_file():
            sub_files.append(child)

    for sub_dir in sub_dirs:
        relative_path: str = sub_dir.relative_to(root, walk_up=True).as_posix()

        builder.button(
            text=f"📁{relative_path}/",
            callback_data=callback.ChangeDirCallback(
                relative_path_hash=mk_base85_hash(relative_path)
            ),
        )
    for sub_file in sub_files:
        relative_path: str = sub_file.relative_to(root).as_posix()
        builder.button(
            text=f"📄{relative_path} ({naturalsize(sub_file.stat().st_size, binary=True)})",
            callback_data=callback.DownloadFileCallback(
                relative_path_hash=mk_base85_hash(relative_path)
            ),
        )

    builder.adjust(1, repeat=True)
    return builder.as_markup()
