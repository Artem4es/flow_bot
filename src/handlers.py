from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram_calendar import (
    SimpleCalendar,
    SimpleCalendarCallback,
)

# TODO: часовой пояс?

router = Router()


MARK_SIGN = "+"


class CustomCalendar(SimpleCalendar):
    def __init__(self, state: FSMContext | None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state
        self.dates_chosen = None

    async def start_calendar_custom(
        self,
        dates_chosen: list[datetime] | None = None,
        year: int = datetime.now().year,
        month: int = datetime.now().month,
    ) -> InlineKeyboardMarkup:
        markup = await super().start_calendar(year, month)
        curr_markup = markup.inline_keyboard
        if dates_chosen:
            self.dates_chosen = dates_chosen
            for date in dates_chosen:
                if self._date_in_widget_month(curr_markup[1][1].text, date):
                    for idx, row in enumerate(curr_markup[3:], start=3):
                        curr_markup[idx] = self.mark_button(row, date)

        return markup

    @staticmethod
    def _date_in_widget_month(month_name: str, target_month: datetime) -> bool:
        """Выбранная дата относится к месяцу в отображаемом виджете"""
        return target_month.strftime("%b") in month_name

    @staticmethod
    def mark_button(row: list[InlineKeyboardButton], date_add: datetime):
        for idx, button in enumerate(row, start=0):
            if button.text == str(date_add.day):
                row[idx].text = f"{button.text} {MARK_SIGN}"

        return row

    async def _update_calendar(self, query: CallbackQuery, with_date: datetime):
        if self.state:
            dates_chosen = (await self.state.get_data())["dates_chosen"]
            dates_chosen_datetime = [
                datetime.strptime(date, "%d/%m/%Y") for date in dates_chosen
            ]
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar_custom(
                    year=int(with_date.year),
                    month=int(with_date.month),
                    dates_chosen=dates_chosen_datetime,
                )
            )

        else:
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar(
                    int(with_date.year), int(with_date.month)
                )
            )


@router.message(CommandStart())
async def nav_cal_handler_date(message: Message, state: FSMContext):

    user_data = await state.get_data()
    if not user_data:
        await state.set_data(dict(dates_chosen=[]))
        user_data = await state.get_data()

    dates_chosen = user_data["dates_chosen"]
    dates_chosen_datetime = [
        datetime.strptime(date, "%d/%m/%Y") for date in dates_chosen
    ]
    calendar = CustomCalendar(
        # locale=await get_user_locale(message.from_user),
        show_alerts=True,
        state=state,
    )
    await message.answer(
        text=f"Выбери дату, {message.from_user.username}",
        reply_markup=await calendar.start_calendar_custom(
            year=datetime.now().year,
            month=datetime.now().month,
            dates_chosen=dates_chosen_datetime,
        ),
    )


@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(
    callback_query: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext,
):
    calendar = CustomCalendar(
        # locale=await get_user_locale(callback_query.from_user),
        show_alerts=True,
        state=state,
    )
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        date_string = date.strftime("%d/%m/%Y")
        dates_chosen = set((await state.get_data())["dates_chosen"])
        if date_string in dates_chosen:
            dates_chosen.remove(date_string)

        else:
            dates_chosen.add(date_string)

        await state.update_data(dict(dates_chosen=list(dates_chosen)))
        dates_chosen_datetime = [
            datetime.strptime(date, "%d/%m/%Y") for date in dates_chosen
        ]
        reply_mkp = await calendar.start_calendar_custom(
            year=date.year,
            month=date.month,
            dates_chosen=dates_chosen_datetime,
        )

        await callback_query.message.edit_reply_markup(
            text="Календарик",
            reply_markup=reply_mkp,
        )
