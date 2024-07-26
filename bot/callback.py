from aiogram.filters.callback_data import CallbackData


class ChangeDirCallback(CallbackData, prefix="cd"):
    relative_path_hash: str


class DownloadFileCallback(CallbackData, prefix="d"):
    relative_path_hash: str
