from app.repositories.memory_store import clone, state


class ProfileRepository:
    def get_profile(self) -> dict | None:
        profile = state['profile']
        return clone(profile) if profile else None

    def save_profile(self, payload: dict) -> dict:
        state['profile'] = clone(payload)
        return clone(state['profile'])

    def get_interpretation(self) -> dict:
        return clone(state['interpretation'])
