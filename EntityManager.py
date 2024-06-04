from Entities.Entity import Entity


class EntityManager:

    def __init__(self):
        self.entities: list[Entity] = []

    def add(self, e: Entity) -> None:
        self.entities.append(e)

    def write(self) -> None:
        for e in self.entities:
            if e.alive:
                e.draw()
            else:
                self.entities.remove(e)
