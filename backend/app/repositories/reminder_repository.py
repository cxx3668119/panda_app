from app.repositories.memory_store import clone, state


class ReminderRepository:
    def get_settings(self) -> dict:
        return clone(state['reminder'])

    def save_settings(self, payload: dict) -> dict:
        state['reminder'] = clone(payload)
        return clone(state['reminder'])
