from ..db.db_models import ToDo
from ..repositories.base_repo import Repository


class ToDoRepository(Repository):
    model = ToDo
