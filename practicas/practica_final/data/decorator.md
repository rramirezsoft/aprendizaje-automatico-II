# Patron Decorator

## Categoria
Estructural.

## Proposito
Añadir funcionalidad adicional a un objeto de forma dinamica, envolviendolo en otro objeto que ofrece la misma interfaz pero amplia o modifica su comportamiento. Es una alternativa flexible a la herencia para extender funcionalidad.

## Cuando usarlo
- Cuando se quiere añadir comportamiento a objetos individuales sin afectar al resto de instancias de la clase.
- Cuando la herencia produciria una explosion combinatoria de subclases (por ejemplo, una clase Cafe con variantes para CafeConLeche, CafeConAzucar, CafeConLecheYAzucar, CafeConLecheAzucarYCanela...).
- Para añadir aspectos transversales como logging, autenticacion, cache, validacion o medicion de tiempos sin tocar la logica de negocio.
- Para componer comportamientos en tiempo de ejecucion combinando varios decoradores en cadena.

## Estructura
Existe una interfaz Component comun. Tanto el ConcreteComponent (la clase base) como los Decorator concretos la implementan. Cada decorador contiene una referencia a otro Component y delega en el, añadiendo su propia logica antes o despues. Los decoradores pueden anidarse formando una cadena.

## Ejemplo en Python
```python
class Texto:
    def __init__(self, contenido):
        self.contenido = contenido

    def render(self):
        return self.contenido

class Negrita:
    def __init__(self, componente):
        self.componente = componente

    def render(self):
        return f"<b>{self.componente.render()}</b>"

class Cursiva:
    def __init__(self, componente):
        self.componente = componente

    def render(self):
        return f"<i>{self.componente.render()}</i>"

t = Cursiva(Negrita(Texto("Hola")))
print(t.render())  # <i><b>Hola</b></i>
```

En Python, los decoradores de funcion (`@decorator`) son una aplicacion sintactica directa de este patron a nivel de funciones.

## Ventajas
- Mas flexible que la herencia: combinas comportamientos en tiempo de ejecucion.
- Cumple el principio de responsabilidad unica al separar cada aspecto en su decorador.
- Permite añadir o quitar funcionalidad sin modificar la clase original.

## Desventajas
- Crear muchos pequeños objetos con la misma interfaz puede dificultar el debugging.
- El orden en que se aplican los decoradores afecta al resultado final.
- Identificar a un decorador especifico dentro de una cadena es complicado.

## Casos reales
Streams de I/O en Java (BufferedReader envolviendo InputStreamReader), middlewares en frameworks web (cada middleware decora la siguiente capa), decoradores `@property`, `@staticmethod` y `@cache` en Python.
