from app.repositories.memory_store import clone, state


class GrowthRepository:
    def get_archive(self) -> dict:
        return clone(state['growth_archive'])
