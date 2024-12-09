import openai
import json
from catalog import get_product_info, check_stock

# Configuración de la API de OpenAI
openai.api_key = COPY APY

# Contexto para almacenar mensajes de conversación
conversation_context = {"last_product": None, "messages": []}

# Función para procesar información del producto
def get_product_info_func(product_name):
    product = get_product_info(product_name)
    
    if product:
        conversation_context["last_product"] = product["name"]
        
        available_quantity = product.get("available_quantity", 0)
        availability = product["availability"]
        availability_message = f"I have {available_quantity} units in stock." if available_quantity > 0 else "It is out of stock right now."

        return (
            f"Product Information:\n"
            f"- ID: {product['id']}\n"
            f"- Name: {product['name']}\n"
            f"- Description: {product['description']}\n"
            f"- Price: ${product['price']}\n"
            f"- Status: {'Available' if availability else 'Not available'}\n"
            f"- {availability_message}\n"
            f"Would you like to know about similar products or check the stock?"
        )
    else:
        return "Sorry, I couldn't find the product you're looking for. Would you like to try another name or see the most popular products?"

# Función para verificar stock
def check_stock_func(product_name=None):
    product_name = product_name or conversation_context.get("last_product")
    
    if not product_name:
        return "Please provide a specific product first to check the stock."

    stock_result = check_stock(product_name)
    
    if isinstance(stock_result, dict):
        available_quantity = stock_result.get("available_quantity", 0)
        
        if available_quantity > 0:
            return f"The product '{product_name}' is in stock with {available_quantity} units available. Would you like to add it to your cart?"
        else:
            return f"Unfortunately, the product '{product_name}' is out of stock. Would you like to see similar alternatives?"
    else:
        return stock_result.get("message", "I couldn't retrieve stock information.")

# Configuración de funciones del asistente
def configure_assistant():
    return [
        {
            "name": "get_product_info",
            "description": "Gets full details of a product in the catalog, including availability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"}
                },
                "required": ["product_name"]
            }
        },
        {
            "name": "check_stock",
            "description": "Checks if a product is in stock, along with the available quantity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"}
                },
                "required": ["product_name"]
            }
        }
    ]

# Procesa el mensaje y genera una respuesta
def process_assistant_response(response):
    function_call = response['choices'][0]['message'].get('function_call')
    
    if function_call:
        function_name = function_call.get("name")
        parameters = json.loads(function_call.get("arguments", "{}"))
        
        if function_name == "get_product_info":
            return get_product_info_func(**parameters)
        elif function_name == "check_stock":
            return check_stock_func(**parameters)
    
    return response['choices'][0]['message'].get('content', "I'm sorry, I couldn't find an appropriate response.")

# Función principal para consultar al asistente
def query_assistant(user_message):
    # Almacenar el mensaje del usuario
    conversation_context["messages"].append({"role": "user", "content": user_message})
    
    try:
        # Generar la respuesta del asistente
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an e-commerce assistant. Your role is to help users find product information, check availability, and answer questions about the catalog."}
            ] + conversation_context["messages"],
            functions=configure_assistant(),
            function_call="auto"
        )
        
        # Procesar y retornar la respuesta del asistente
        assistant_message = process_assistant_response(response)
        conversation_context["messages"].append({"role": "assistant", "content": assistant_message})
        
        return assistant_message

    except openai.error.OpenAIError as api_error:
        print(f"OpenAI API Error: {api_error}")
        return f"There was a problem connecting to the assistant service. Please try again later. Error: {api_error}"
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"