import json

# Cargar el catálogo de productos desde un archivo JSON
try:
    with open("productos.json", "r") as f:
        products = json.load(f)
except FileNotFoundError:
    print("Error: El archivo 'productos.json' no se encontró.")
    products = []
except json.JSONDecodeError:
    print("Error: El archivo 'productos.json' contiene errores de formato.")
    products = []

# Función para obtener información de un producto por nombre (coincidencia parcial)
def get_product_info(product_name):
    if not product_name:
        return None

    for product in products:
        if product_name.lower() in product.get("name", "").lower():
            return {
                "id": product.get("id", "N/A"),
                "name": product.get("name", "Unknown Product"),
                "description": product.get("description", "No description available."),
                "price": product.get("price", 0.0),
                "availability": "Available" if product.get("availability", False) else "Not available",
                "available_quantity": product.get("quantity_available", 0)
            }
    return None

# Función para verificar el stock de un producto y obtener detalles adicionales
def check_stock(product_name):
    if not product_name:
        return {"message": "El nombre del producto no puede estar vacío."}

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
