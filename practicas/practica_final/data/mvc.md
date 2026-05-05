# Patron MVC (Model-View-Controller)

## Categoria
Arquitectural (no es un patron GoF puro, pero es uno de los patrones de diseño mas extendidos en aplicaciones interactivas).

## Proposito
Separar la aplicacion en tres componentes con responsabilidades bien diferenciadas para reducir el acoplamiento y facilitar el mantenimiento, las pruebas y la evolucion del software.

## Componentes

### Modelo
Encapsula los datos y la logica de negocio del dominio. Es independiente de la interfaz: no sabe como se muestran los datos. Responsabilidades tipicas: validar datos, persistir en base de datos, ejecutar reglas de negocio, notificar cambios.

### Vista
Renderiza al usuario los datos del modelo en un formato visual (HTML, ventana de escritorio, terminal, JSON). Captura las interacciones del usuario (clicks, teclas, formularios) y las traslada al controlador. No contiene logica de negocio: solo muestra y recoge entradas.

### Controlador
Actua como intermediario entre la vista y el modelo. Recibe los eventos de la vista, decide que accion tomar, ordena al modelo que se actualice y selecciona la vista adecuada para la respuesta.

## Cuando usarlo
- En aplicaciones con interfaz de usuario, especialmente web (Django, Spring MVC, Ruby on Rails, ASP.NET MVC).
- Cuando varios equipos trabajan en paralelo: backend en el modelo, frontend en la vista, integracion en el controlador.
- Cuando se necesita exponer los mismos datos a traves de varias vistas (web, movil, API REST).

## Flujo tipico de una peticion
1. El usuario interactua con la vista (envia un formulario web).
2. La vista envia la peticion al controlador correspondiente.
3. El controlador valida la peticion, instruye al modelo que realice la operacion necesaria.
4. El modelo procesa los datos y los devuelve al controlador.
5. El controlador selecciona la vista adecuada y le pasa los datos.
6. La vista renderiza la respuesta y la entrega al usuario.

## Ejemplo conceptual en Python
```python
class ModeloUsuario:
    def __init__(self):
        self.usuarios = []

    def crear(self, nombre):
        self.usuarios.append(nombre)
        return nombre

class VistaUsuario:
    def mostrar_lista(self, usuarios):
        for u in usuarios:
            print(f"- {u}")

    def confirmar_creacion(self, nombre):
        print(f"Usuario {nombre} creado correctamente.")

class ControladorUsuario:
    def __init__(self):
        self.modelo = ModeloUsuario()
        self.vista = VistaUsuario()

    def crear_usuario(self, nombre):
        creado = self.modelo.crear(nombre)
        self.vista.confirmar_creacion(creado)

    def listar(self):
        self.vista.mostrar_lista(self.modelo.usuarios)
```

## Ventajas
- Separacion clara de responsabilidades, facilita el mantenimiento a largo plazo.
- Permite reusar el modelo en varias vistas (web, movil, API).
- Facilita el testing: se puede testear el modelo sin levantar la interfaz.

## Desventajas
- Para aplicaciones muy simples puede ser demasiada estructura.
- La frontera entre controlador y modelo no siempre es clara y puede generar discusiones de equipo.
- Variantes modernas como MVP o MVVM resuelven mejor algunos casos especificos.
