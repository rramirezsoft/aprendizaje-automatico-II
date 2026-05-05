# Patron Singleton

## Categoria
Creacional.

## Proposito
Garantizar que una clase tenga una unica instancia en toda la aplicacion y proporcionar un punto de acceso global a esa instancia.

## Cuando usarlo
- Cuando exactamente una instancia de una clase es necesaria y debe ser accesible desde cualquier punto del codigo.
- Recursos compartidos como un logger, una conexion a la base de datos, una cache global o el gestor de configuracion.
- Cuando crear multiples instancias provoca conflictos (acceso concurrente al mismo fichero, contadores duplicados, conexiones redundantes).

## Estructura
La clase Singleton oculta su constructor (privado en lenguajes que lo permiten) y expone un metodo estatico, normalmente llamado `getInstance()`, que devuelve siempre la misma instancia. Internamente la instancia se almacena como atributo de clase y se crea perezosamente la primera vez que se solicita.

## Ejemplo en Python
```python
class Logger:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def log(self, mensaje):
        print(f"[LOG] {mensaje}")

a = Logger()
b = Logger()
assert a is b  # misma instancia
```

## Ventajas
- Acceso global controlado al recurso compartido.
- Inicializacion perezosa (solo se crea cuando hace falta).
- Ahorra memoria al evitar copias innecesarias.

## Desventajas
- Introduce estado global, lo que dificulta el testing aislado.
- Puede ocultar dependencias entre clases.
- Problemas con multithreading si no se sincroniza correctamente la creacion.
