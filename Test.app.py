from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake in-memory "database" so we don't need a real one for this exercise.
# Think of this like a whiteboard in the workshop. It resets every time the
# server restarts, which is fine for a practice project.
orders = [
    {"id": 1, "customer": "Tony Stark", "item": "AeroBrew 300", "status": "shipped"},
    {"id": 2, "customer": "Pepper Potts", "item": "AeroBrew 300 - Replacement Filter", "status": "processing"},
]


# 1. GET endpoint - simple health check.
# This is the one Quick (or anyone) hits first to confirm the server is alive.
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "AeroBrew API is running"})


# 2. GET endpoint - list all orders.
@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)


# 3. GET endpoint - get one specific order by id.
# Example: /orders/1
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    for order in orders:
        if order["id"] == order_id:
            return jsonify(order)
    return jsonify({"error": "Order not found"}), 404


# 4. POST endpoint - create a new order.
# This is the "write" action, the kind of thing an agent could trigger
# on your behalf through the REST API connector.
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data or "customer" not in data or "item" not in data:
        return jsonify({"error": "Request must include 'customer' and 'item'"}), 400

    new_order = {
        "id": len(orders) + 1,
        "customer": data["customer"],
        "item": data["item"],
        "status": "processing",
    }
    orders.append(new_order)
    return jsonify(new_order), 201


if __name__ == "__main__":
    # 0.0.0.0 so it's reachable from outside this one machine once deployed.
    app.run(host="0.0.0.0", port=5000)
