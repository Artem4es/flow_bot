from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from datetime import date

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar


from src.keyboards import MAIN_MENU_MARKUP
from src.services.logic.user import UserService


class StartMenuServ:
    def __init__(self, mes_or_call: CallbackQuery | Message, state: FSMContext):
        self.mes_or_call = mes_or_call
        self.state = state
        self.user_serv = UserService(state)

    async def process(self) -> None:
        dates_chosen = await self.user_serv.get_dates_chosen()
        reply_markup = self._create_reply_markup(dates_chosen)
        text = self._get_text()
        if isinstance(self.mes_or_call, CallbackQuery):
            await self.mes_or_call.message.edit_text(
                text=text, reply_markup=reply_markup
            )
            await self.mes_or_call.answer()
            return

        await self.mes_or_call.answer(text=text, reply_markup=reply_markup)

    def _get_text(self) -> str:
        username = self.mes_or_call.message.from_user.username
        return f"Привет {username}! Выбери даты для отслеживания:"

    @staticmethod
    def _create_reply_markup(date_chosen: list[str] | None) -> InlineKeyboardMarkup:
        base_keyboard = MAIN_MENU_MARKUP.model_copy(deep=True)

        # rows =
        # if user_data and SubLogicService.has_active_sub(user_data):
        #     sub_button = InlineKeyboardButton(
        #         text="😎 Моя подписка",
        #         callback_data=CallbackDataEnum.MY_SUBSCRIPTION,
        #     )
        #     base_keyboard.inline_keyboard.append([sub_button])
        #
        # return base_keyboard
