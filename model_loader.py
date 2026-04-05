from . import orders, order_details, recipes, sandwiches, resources
from ..dependencies.database import Base, engine


def index():
    Base.metadata.create_all(bind=engine)
