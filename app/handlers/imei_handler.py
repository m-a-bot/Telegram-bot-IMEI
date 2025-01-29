import json
import logging
from typing import Any

import aiohttp
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.markdown import pre
from aiohttp.client_exceptions import ClientResponseError
from redis import Redis

from app.config import settings
from app.database.database import async_redis
from app.exceptions import (
    AccessDeniedError,
    InvalidDataError,
    UserAlreadyExistsError,
)
from app.services.imei_validation_service import IMEIValidationService
from app.services.token_service import TokenService
from app.services.whitelist_service import WhitelistService


class CheckProcess(StatesGroup):
    question = State()
    get_data = State()
    check_imei = State()


check_router = Router()


@check_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    try:
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        await WhitelistService().add_to_whitelist(user_id, user_name)
    except UserAlreadyExistsError:
        logging.error("User already exists in whitelist")
    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    await state.set_state(CheckProcess.question)

    await which_imei(message, state)


@check_router.message(Command("help"))
async def help_command(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer("/help - \n\n" "/check_imei - ")


@check_router.message(Command("check_imei"))
async def check_command(message: Message, state: FSMContext) -> None:
    try:
        await WhitelistService().check_access(message.from_user.id)
    except AccessDeniedError:
        logging.error("User doesn't exists in whitelist")
        await state.clear()
        await message.answer(f"access is restricted")
        return
    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    await state.set_state(CheckProcess.question)

    await which_imei(message, state)


@check_router.message(CheckProcess.question)
async def which_imei(message: Message, state: FSMContext) -> None:
    try:
        await WhitelistService().check_access(message.from_user.id)
    except AccessDeniedError:
        logging.error("User doesn't exists in whitelist")
        await state.clear()
        await message.answer(f"access is restricted")
        return
    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    await state.set_state(CheckProcess.get_data)

    await message.answer(
        (
            "Write your *IMEI* \n\nto get detailed info about your phone\n\n"
            "*example* \- `356735111052198`"
        ),
        parse_mode="MarkdownV2",
    )


@check_router.message(CheckProcess.get_data)
async def get_imei(message: Message, state: FSMContext) -> None:
    try:
        await WhitelistService().check_access(message.from_user.id)
    except AccessDeniedError:
        logging.error("User doesn't exists in whitelist")
        await state.clear()
        await message.answer(f"access is restricted")
        return
    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    imei = message.text
    if imei and len(imei) == 15:
        await state.set_state(CheckProcess.check_imei)

        await message.answer(f"Check *IMEI*: {imei}", parse_mode="MarkdownV2")

        await check_imei(message, state, imei)
        return

    if "cancel" in message.text.lower():
        await state.clear()
        await message.answer(f"Cancel")
        return

    await message.answer(f"Try again, please")


@check_router.message(CheckProcess.check_imei)
async def check_imei(message: Message, state: FSMContext, imei: str) -> None:
    try:
        await WhitelistService().check_access(message.from_user.id)
    except AccessDeniedError:
        logging.error("User doesn't exists in whitelist")
        await state.clear()
        await message.answer(f"access is restricted")
        return
    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    user_id = message.from_user.id

    try:
        async with async_redis.client() as db:
            try:
                token = await TokenService(db).load_token(user_id)

                if token is None:
                    token = await TokenService(db).get_token(user_id)

                imei_json_info = await IMEIValidationService().verify_imei(
                    imei, token, user_id
                )
            finally:
                await db.close()
    except AccessDeniedError:
        await state.clear()
        await message.answer(f"access is restricted")
        return
    except InvalidDataError as exc:
        logging.error("Invalid data", exc_info=exc)
        await message.answer(f"Try again. Invalid data")
        await state.set_state(CheckProcess.get_data)
        return

    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    await state.clear()
    await message.answer(
        (
            f"*IMEI*: {imei}\n"
            + pre(json.dumps(imei_json_info, indent=2, ensure_ascii=False))
        ),
        parse_mode="MarkdownV2",
    )


@check_router.message()
async def unknown_command(message: Message) -> None:
    await message.answer("Unknown command. Use /start or /check_imei.")
