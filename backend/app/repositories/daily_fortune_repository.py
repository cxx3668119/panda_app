from app.repositories.memory_store import clone, state


class DailyFortuneRepository:
    def get_today(self) -> dict:
        return clone(state['daily_today'])

    def get_history(self) -> list[dict]:
        return clone(state['daily_history'])
