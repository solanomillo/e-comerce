class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        
        cart = self.session.get('cart')
        montoTotal = self.session.get('cartMontoTotal')
        
        if not cart:
            cart = self.session['cart'] = {}
            montoTotal = self.session['cartMontoTotal'] = '0'

        self.cart = cart
        self.montoTotal = float(montoTotal)    
    
    def add(self, producto, cantidad):
        # agrega un producto al carrito de compras
        if str(producto.id) not in self.cart.keys():
            self.cart[producto.id] = {
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio': str(producto.precio),
                'subtotal': str(producto.precio * cantidad),
                'imagen': producto.imagen.url,
                'categoria': producto.categoria.nombre
            }
        else:
            # si el producto ya existe en el carrito, actualiza la cantidad y el subtotal
            for key,value in self.cart.items():
                if key == str(producto.id):
                    value['cantidad'] += cantidad
                    value['subtotal'] = str(float(value['precio']) * float(value['cantidad']))
                    break

        self.save()
    
    def delete(self, producto):
        # elimina los productos del carrito
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()
            
    def clear(self):
        self.session['cart'] = {}
        self.session['cartMontoTotal'] = '0'
    
    def save(self):
        # guarda los cambios en el carrio de compras
        montoTotal = sum(float(item['subtotal']) for item in self.cart.values())
        self.session['cartMontoTotal'] = montoTotal
        self.session['cart'] = self.cart
        self.session.modified = True
    
    def items(self):
        return self.cart.values() 