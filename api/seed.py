from .dependencies.database import SessionLocal
from .models import model_loader
from .models.sandwiches import Sandwich
from .models.resources import Resource
from .models.recipes import Recipe
from .models.orders import Order
from .models.order_details import OrderDetail
from datetime import datetime, timedelta

model_loader.index()
db = SessionLocal()


def clear_all():
    db.query(OrderDetail).delete()
    db.query(Order).delete()
    db.query(Recipe).delete()
    db.query(Resource).delete()
    db.query(Sandwich).delete()
    db.commit()


def seed_sandwiches():
    sandwiches = [
        Sandwich(sandwich_name="Classic BLT", price=7.99),
        Sandwich(sandwich_name="Turkey Club", price=8.99),
        Sandwich(sandwich_name="Veggie Delight", price=6.99),
        Sandwich(sandwich_name="Spicy Italian", price=9.49),
        Sandwich(sandwich_name="Ham & Swiss", price=7.49),
        Sandwich(sandwich_name="Tuna Melt", price=8.49),
    ]
    db.add_all(sandwiches)
    db.commit()
    return db.query(Sandwich).all()


def seed_resources():
    resources = [
        Resource(item="Bread (slices)", amount=100),
        Resource(item="Bacon (strips)", amount=80),
        Resource(item="Lettuce (leaves)", amount=60),
        Resource(item="Tomato (slices)", amount=70),
        Resource(item="Turkey (slices)", amount=50),
        Resource(item="Ham (slices)", amount=50),
        Resource(item="Swiss Cheese (slices)", amount=40),
        Resource(item="Tuna (oz)", amount=60),
        Resource(item="Salami (slices)", amount=45),
        Resource(item="Pepperoni (slices)", amount=45),
        Resource(item="Mayonnaise (tbsp)", amount=200),
        Resource(item="Mustard (tbsp)", amount=150),
        Resource(item="Spinach (oz)", amount=30),
        Resource(item="Avocado (slices)", amount=25),
    ]
    db.add_all(resources)
    db.commit()
    return db.query(Resource).all()


def seed_recipes(sandwiches, resources):
    res = {r.item: r for r in resources}
    sw = {s.sandwich_name: s for s in sandwiches}
    recipes = [
        Recipe(
            sandwich_id=sw["Classic BLT"].id,
            resource_id=res["Bread (slices)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Classic BLT"].id,
            resource_id=res["Bacon (strips)"].id,
            amount=3,
        ),
        Recipe(
            sandwich_id=sw["Classic BLT"].id,
            resource_id=res["Lettuce (leaves)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Classic BLT"].id,
            resource_id=res["Tomato (slices)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Turkey Club"].id,
            resource_id=res["Bread (slices)"].id,
            amount=3,
        ),
        Recipe(
            sandwich_id=sw["Turkey Club"].id,
            resource_id=res["Turkey (slices)"].id,
            amount=4,
        ),
        Recipe(
            sandwich_id=sw["Turkey Club"].id,
            resource_id=res["Bacon (strips)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Veggie Delight"].id,
            resource_id=res["Bread (slices)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Veggie Delight"].id,
            resource_id=res["Spinach (oz)"].id,
            amount=1,
        ),
        Recipe(
            sandwich_id=sw["Veggie Delight"].id,
            resource_id=res["Avocado (slices)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Spicy Italian"].id,
            resource_id=res["Bread (slices)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Spicy Italian"].id,
            resource_id=res["Salami (slices)"].id,
            amount=4,
        ),
        Recipe(
            sandwich_id=sw["Spicy Italian"].id,
            resource_id=res["Pepperoni (slices)"].id,
            amount=4,
        ),
        Recipe(
            sandwich_id=sw["Ham & Swiss"].id,
            resource_id=res["Bread (slices)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Ham & Swiss"].id,
            resource_id=res["Ham (slices)"].id,
            amount=4,
        ),
        Recipe(
            sandwich_id=sw["Ham & Swiss"].id,
            resource_id=res["Swiss Cheese (slices)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Tuna Melt"].id,
            resource_id=res["Bread (slices)"].id,
            amount=2,
        ),
        Recipe(
            sandwich_id=sw["Tuna Melt"].id, resource_id=res["Tuna (oz)"].id, amount=3
        ),
        Recipe(
            sandwich_id=sw["Tuna Melt"].id,
            resource_id=res["Swiss Cheese (slices)"].id,
            amount=2,
        ),
    ]
    db.add_all(recipes)
    db.commit()


def seed_orders(sandwiches):
    sw = {s.sandwich_name: s for s in sandwiches}
    now = datetime.now()
    orders_data = [
        {
            "customer_name": "Alice Johnson",
            "description": "No pickles",
            "status": "completed",
            "days_ago": 2,
        },
        {
            "customer_name": "Bob Smith",
            "description": "Extra mayo",
            "status": "completed",
            "days_ago": 2,
        },
        {
            "customer_name": "Carol White",
            "description": None,
            "status": "completed",
            "days_ago": 1,
        },
        {
            "customer_name": "David Brown",
            "description": "Gluten free bread",
            "status": "completed",
            "days_ago": 1,
        },
        {
            "customer_name": "Alice Johnson",
            "description": "Extra bacon",
            "status": "completed",
            "days_ago": 0,
        },
        {
            "customer_name": "Eve Martinez",
            "description": None,
            "status": "ready",
            "days_ago": 0,
        },
        {
            "customer_name": "Frank Lee",
            "description": "No tomatoes",
            "status": "in-progress",
            "days_ago": 0,
        },
        {
            "customer_name": "Grace Kim",
            "description": None,
            "status": "in-progress",
            "days_ago": 0,
        },
        {
            "customer_name": "Henry Adams",
            "description": "Extra cheese",
            "status": "pending",
            "days_ago": 0,
        },
        {
            "customer_name": "Isla Turner",
            "description": None,
            "status": "pending",
            "days_ago": 0,
        },
        {
            "customer_name": "Jack Wilson",
            "description": "Light on sauce",
            "status": "pending",
            "days_ago": 0,
        },
        {
            "customer_name": "Bob Smith",
            "description": None,
            "status": "cancelled",
            "days_ago": 0,
        },
    ]
    order_objs = []
    for i, o in enumerate(orders_data):
        order_date = now - timedelta(days=o["days_ago"]) + timedelta(minutes=i * 3)
        obj = Order(
            customer_name=o["customer_name"],
            description=o["description"],
            status=o["status"],
            order_date=order_date,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        order_objs.append(obj)

    details = [
        OrderDetail(
            order_id=order_objs[0].id, sandwich_id=sw["Classic BLT"].id, amount=2
        ),
        OrderDetail(
            order_id=order_objs[0].id, sandwich_id=sw["Turkey Club"].id, amount=1
        ),
        OrderDetail(
            order_id=order_objs[1].id, sandwich_id=sw["Spicy Italian"].id, amount=2
        ),
        OrderDetail(
            order_id=order_objs[2].id, sandwich_id=sw["Veggie Delight"].id, amount=1
        ),
        OrderDetail(
            order_id=order_objs[2].id, sandwich_id=sw["Ham & Swiss"].id, amount=2
        ),
        OrderDetail(
            order_id=order_objs[3].id, sandwich_id=sw["Turkey Club"].id, amount=3
        ),
        OrderDetail(
            order_id=order_objs[4].id, sandwich_id=sw["Classic BLT"].id, amount=1
        ),
        OrderDetail(
            order_id=order_objs[4].id, sandwich_id=sw["Tuna Melt"].id, amount=1
        ),
        OrderDetail(
            order_id=order_objs[5].id, sandwich_id=sw["Veggie Delight"].id, amount=2
        ),
        OrderDetail(
            order_id=order_objs[6].id, sandwich_id=sw["Spicy Italian"].id, amount=1
        ),
        OrderDetail(
            order_id=order_objs[6].id, sandwich_id=sw["Ham & Swiss"].id, amount=1
        ),
        OrderDetail(
            order_id=order_objs[7].id, sandwich_id=sw["Tuna Melt"].id, amount=2
        ),
        OrderDetail(
            order_id=order_objs[8].id, sandwich_id=sw["Classic BLT"].id, amount=3
        ),
        OrderDetail(
            order_id=order_objs[9].id, sandwich_id=sw["Turkey Club"].id, amount=1
        ),
        OrderDetail(
            order_id=order_objs[9].id, sandwich_id=sw["Veggie Delight"].id, amount=1
        ),
        OrderDetail(
            order_id=order_objs[10].id, sandwich_id=sw["Ham & Swiss"].id, amount=2
        ),
        OrderDetail(
            order_id=order_objs[11].id, sandwich_id=sw["Spicy Italian"].id, amount=1
        ),
    ]
    db.add_all(details)
    db.commit()


if __name__ == "__main__":
    clear_all()
    sw = seed_sandwiches()
    res = seed_resources()
    seed_recipes(sw, res)
    seed_orders(sw)
    db.close()
    print("Database seeded successfully!")
