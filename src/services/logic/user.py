from aiogram.fsm.context import FSMContext


class UserService:
    def __init__(self, state: FSMContext):
        self.state = state

    async def get_dates_chosen(self) -> list[str]:
        if dates_data := await self.state.get_data():
            return dates_data["dates_chosen"]

    # async def get_or_create_user(self) -> :
    #     user_data = await self.state.get_data()
    #     if not user_data:
