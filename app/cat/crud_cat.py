

from app.core.crud_base import BaseCRUD
from app.cat.model import Cat


class CatCrud(BaseCRUD):
    model = Cat