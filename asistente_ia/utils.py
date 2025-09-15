from web.models import Producto

def obtener_catalogo():
    productos = Producto.objects.all()
    texto = "Catálogo de productos:\n"
    for p in productos:
        if p.precio:
            # Formato: $15.000 (en vez de 15000.00)
            precio = f"${p.precio:,.0f}".replace(",", ".")
        else:
            precio = "Precio no disponible"

        descripcion = p.descripcion if p.descripcion else "Sin descripción"

        texto += f"- {p.nombre}: {descripcion} | {precio}\n"
    return texto
