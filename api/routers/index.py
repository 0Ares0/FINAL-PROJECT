from . import orders, order_details, sandwiches, resources, recipes


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(sandwiches.router)
    app.include_router(resources.router)
    app.include_router(recipes.router)
