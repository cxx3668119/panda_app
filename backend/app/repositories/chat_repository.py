from app.repositories.memory_store import clone, state


class ChatRepository:
    def get_quota(self) -> dict:
        return clone(state['quota'])

    def get_messages(self) -> list[dict]:
        return clone(state['messages'])

    def append_message(self, payload: dict) -> dict:
        state['messages'].append(clone(payload))
        return clone(payload)

    def update_quota(self, payload: dict) -> dict:
        state['quota'] = clone(payload)
        return clone(state['quota'])
