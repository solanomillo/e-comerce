# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .gemini_cliente import llm, SALUDO_INICIAL
from .utils import obtener_catalogo

# Diccionario para almacenar chats por usuario (temporal)
# Para producción usar Redis o base de datos
chats = {}

@csrf_exempt
def chat_api(request):
    # Obtener ID de sesión único
    user_id = request.session.session_key or request.session.save() or request.session.session_key
    user_message = request.GET.get("message", "")

    # Mensaje de saludo inicial
    if user_message == "__init__":
        return JsonResponse({"respuesta": SALUDO_INICIAL})

    # Recuperar o crear el chat para el usuario
    if user_id not in chats:
        chats[user_id] = []  # Lista de mensajes históricos

    historial = chats[user_id]

    # Añadir mensaje del usuario al historial
    historial.append({"role": "user", "content": user_message})

    # Obtener catálogo de productos
    catalogo = obtener_catalogo()

    # Construir prompt para Gemini
    prompt = (
        "Contexto del catálogo:\n"
        f"{catalogo}\n\n"
        "Historial de conversación:\n"
    )
    for m in historial:
        role = "Usuario" if m["role"] == "user" else "Tic"
        prompt += f"{role}: {m['content']}\n"

    prompt += "Tic:"

    # Llamada al modelo Gemini
    respuesta = llm.generate_content(prompt)

    # Limpiar texto: eliminar asteriscos y convertir saltos de línea en lista HTML
    texto = respuesta.text.replace("*", "")
    lineas = [l.strip() for l in texto.split("\n") if l.strip()]
    if len(lineas) > 1:
        texto_html = "<ul>" + "".join([f"<li>{l}</li>" for l in lineas]) + "</ul>"
    else:
        texto_html = texto

    # Guardar respuesta del bot en historial
    historial.append({"role": "assistant", "content": texto})

    return JsonResponse({"respuesta": texto_html})
