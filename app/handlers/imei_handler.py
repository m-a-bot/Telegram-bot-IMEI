import json
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.markdown import pre
from redis import Redis
from app.config import settings

from app.dependencies import get_dependency
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
    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    await state.set_state(CheckProcess.get_data)

    await message.answer(
        (
            "Write your *IMEI* \n\nto get detailed info about your phone\n\n"
            "*example* \- `000000000000000`"
        ),
        parse_mode="MarkdownV2",
    )


@check_router.message(CheckProcess.get_data)
async def get_imei(message: Message, state: FSMContext) -> None:
    try:
        await WhitelistService().check_access(message.from_user.id)
    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    imei = message.text
    if imei and len(imei) == 15:
        await state.set_state(CheckProcess.check_imei)

        await message.answer(f"Check *IMEI*: {imei}", parse_mode="MarkdownV2")
        await check_imei(message, state)
        return

    if "cancel" in message.text.lower():
        await state.clear()
        await message.answer(f"Cancel")
        return

    await message.answer(f"Try again, please")


@check_router.message(CheckProcess.check_imei)
async def check_imei(message: Message, state: FSMContext) -> None:
    try:
        await WhitelistService().check_access(message.from_user.id)
    except Exception as exc:
        logging.error("Exception", exc_info=exc)
        await state.clear()
        await message.answer(f"Something wrong")
        return

    db: Redis = get_dependency("get_db")
    if not db:
        await state.clear()
        await message.answer(f"Bot broke down")
        return

    user_id = message.from_user.id

    try:
        token = await TokenService(db).load_token(user_id)

        # if not token:
        #     token = await TokenService(db).get_token(user_id)

        token = settings.VALID_TOKEN

        imei = message.text
        imei_json_info = await IMEIValidationService().verify_imei(imei, token, user_id)
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
