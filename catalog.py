import json

# Load the product catalog from a JSON file
with open("productos.json", "r") as f:
    products = json.load(f)

# Function to get product information by name with partial match
def get_product_info(product_name):
    for product in products:
        if product_name.lower() in product["name"].lower():
            return {
                "id": product["id"],
                "name": product["name"],
                "description": product["description"],
                "price": product["price"],
                "availability": "Available" if product["availability"] else "Not available",
                "available_quantity": product["quantity_available"]
            }
    return None

# Function to check stock of a product and get additional details
def check_stock(product_name):
    product = get_product_info(product_name)
    
    if product:
        quantity = product["available_quantity"]
        availability_status = "in stock" if quantity > 0 else "out of stock"
        return {
            "name": product["name"],
            "available_quantity": quantity,
            "status": availability_status,
            "message": f"The product '{product['name']}' is {availability_status} with {quantity} units available."
        }
    else:
        return {"message": "Product not found in the catalog."}
