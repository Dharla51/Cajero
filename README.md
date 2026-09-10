# Cajero Automático — Metodología del Acarreo

Prototipo funcional de un cajero automático desarrollado para la actividad
**"Cajero automático con base a los tipos de sistemas de información"**
(Universidad Popular del Cesar — Momento 2, Ingeniería de Software II).

Construido en **Python 3 + tkinter**, con persistencia simple en archivos
JSON (sin necesidad de base de datos externa).

---

## 1. ¿Qué hace?

Permite realizar **3 tipos de retiro**, cada uno con sus propias reglas de
validación tal como lo exige la guía de actividad:

| Tipo | Vector de identificación | Clave |
|---|---|---|
| **NEQUI** | 10 dígitos (celular), debe iniciar en `3` | Clave temporal de 6 dígitos, visible 60 s y se regenera sola |
| **Ahorro a la mano** | 11 dígitos — 1er dígito en `{0,1}`, 2do dígito obligatorio `3` | PIN de 4 dígitos (oculto en pantalla) |
| **Cuenta de ahorros** | 11 dígitos, solo `0-9` | PIN de 4 dígitos (oculto en pantalla) |

Ningún vector admite letras ni caracteres especiales. **En ningún momento se
muestra en pantalla un vector modificado** (ni con ceros añadidos, ni
normalizado) — el usuario solo ve exactamente lo que digitó.

**Importante: el dinero es del cajero, no de la cuenta.** Las cuentas
(Nequi, ahorro a la mano, cuenta de ahorros) sirven únicamente para
identificar quién retira y validar su clave — no tienen saldo propio. El
único saldo que existe es el **efectivo físico disponible en el cajero**
(su inventario de billetes), que es de donde sale cualquier retiro y sobre
el cual se calculan la predicción de retiros futuros y el efectivo
restante que se muestra al final.

Cada retiro ofrece **montos fijos** para escoger + una opción **"Otro monto"**
libre. El cajero **no maneja billetes de $5.000**; solo dispensa en
$10.000, $20.000, $50.000 y $100.000. Si el monto no es múltiplo de
$10.000 (ej. $145.000), se muestra un error y el proceso se reinicia.

Al confirmar el retiro, la pantalla muestra:
- La cantidad exacta de billetes por denominación.
- La **matriz de intentos** del acarreo (ver sección 3).
- Una **predicción** de cuántos retiros similares podría seguir entregando
  el cajero con el efectivo que le queda.

---

## 2. Cómo ejecutarlo

Requiere Python 3.10+ (usa `dict | None` en type hints).

```bash
cd cajero_automatico
python -m venv .venv          # opcional pero recomendado
source .venv/bin/activate     # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

`tkinter` viene incluido con la instalación estándar de Python en Windows
y macOS. En Linux, si falta, instálalo con:
```bash
sudo apt install python3-tk
```

Cada vez que se ejecuta `python main.py`, las cuentas y el inventario del
cajero **arrancan limpios** (es un cajero de prueba, no hay datos
"guardados" de sesiones anteriores).

### Cómo probarlo

No hay cuentas pre-registradas: para los 3 tipos de retiro, la **primera
vez** que se usa un vector con formato válido, el cajero crea esa cuenta
automáticamente (solo para poder validar la clave en usos siguientes). Por
ejemplo:
- Nequi: cualquier número de 10 dígitos que empiece en `3` (ej. `3001234567`).
- Ahorro a la mano: 11 dígitos, 1er dígito `0` o `1`, 2do dígito `3` (ej. `03345566778`) + cualquier clave de 4 dígitos.
- Cuenta de ahorros: 11 dígitos (ej. `50123456789`) + cualquier clave de 4 dígitos.

Si vuelves a usar el mismo vector, debes ingresar la misma clave con la
que se registró la primera vez.

### Correr las pruebas

```bash
pytest tests/ -v
```

---

## 3. La lógica del acarreo (algoritmo por niveles)

Esta es una traducción directa del algoritmo de referencia que se
validó contra los ejemplos manuscritos del profesor ($200.000 y
$300.000). La idea: hay 4 "niveles", cada uno permitiendo menos
denominaciones que el anterior, y siempre se evalúa en orden
**ascendente empezando por el billete de 10.000**:

```
nivel 1: 100k, 50k, 20k, 10k   (las 4 denominaciones)
nivel 2: 100k, 50k, 20k         (sin el billete de 10.000)
nivel 3: 100k, 50k              (solo 100k y 50k)
nivel 4: 100k                   (solo 100k)
```

Para cada fila, se recorren las denominaciones permitidas del nivel
actual en orden ascendente y se coloca un billete de cada una que
quepa en lo que resta. Si la fila resultante tiene al menos un billete,
se pasa al siguiente nivel (ciclando: después del nivel 4 se vuelve al
nivel 1). Si en cambio el nivel actual ya NO cabe en absoluto (fila de
puros ceros), eso dispara el **reinicio**: se registra esa fila de
ceros como marca visual, se vuelve a intentar inmediatamente con las 4
denominaciones completas, y se continúa desde el nivel 2 en adelante.

### Verificado contra tus dos ejemplos manuscritos

**$200.000** → 2 filas, sin reinicio:
```
             10k   20k   50k   100k
Intento 1      1     1     1     1      (180.000)
Intento 2      0     1     0     0      ( 20.000)
```
Total: 10.000(1) 20.000(2) 50.000(1) 100.000(1) = $200.000 ✔

**$300.000** → 3 filas, sin reinicio:
```
             10k   20k   50k   100k
Intento 1      1     1     1     1      (180.000)
Intento 2      0     1     1     0      ( 70.000)
Intento 3      0     0     1     0      ( 50.000)
```
Total: 10.000(1) 20.000(2) 50.000(3) 100.000(1) = $300.000 ✔ — coincide
exacto con la hoja manuscrita.

Para montos más grandes que sí alcanzan a agotar un nivel (ej. cuando el
nivel 4 ya no tiene ni para un solo billete de 100.000), aparece una
fila de puros ceros marcada **"↺ Reinicio"** en la tabla, y el contador
de intentos vuelve a 1.

### Predicción de combinaciones posibles

Además del efectivo que le queda al cajero, se muestra cuántas
**combinaciones distintas de billetes** podrían sumar exactamente ese
mismo monto (programación dinámica, igual al clásico problema de
monedas) — esto responde directamente al requerimiento de la guía de
"mostrar la cantidad de retiros posibles a través de la predicción del
mismo".

### Otros detalles de negocio

- **Vectores de cuenta normalizados a 16 dígitos** internamente (rellenados
  con ceros a la izquierda) como llave de almacenamiento — el usuario
  jamás ve este relleno, solo su vector original.
- **Inventario de billetes del cajero**: arranca con una cantidad
  predeterminada (`INVENTARIO_INICIAL` en `src/utils/constantes.py`) y se
  descuenta con cada retiro. La recarga **solo ocurre cuando el cajero
  realmente se queda sin los billetes necesarios** para completar el
  retiro en curso. La recarga se calcula como un **top-up por déficit**:
  para cada denominación se resta `inventario_inicial - lo_que_hay`, y
  esa diferencia exacta es la cantidad de billetes que se agrega (nunca
  se sobrescribe el inventario completo a ciegas). Al usuario se le avisa
  que el cajero se está cargando de dinero — mostrando el detalle de
  billetes agregados por denominación — y el retiro se completa
  normalmente.

---

## 4. Estructura del proyecto

Se simplificó a los archivos realmente necesarios: nada de clases o
capas "por si acaso" — cada carpeta tiene un solo archivo cuando con
uno bastaba (por ejemplo, las 3 pantallas de retiro son la MISMA clase
`RetiroView`, parametrizada, en vez de 3 archivos casi idénticos).

```
cajero_automatico/
├── main.py                       # Punto de entrada (reinicia datos de prueba al arrancar)
├── requirements.txt
├── src/
│   ├── ui/
│   │   ├── main_window.py        # Ventana + navegación entre pantallas
│   │   ├── home_view.py          # Selección del tipo de retiro
│   │   ├── retiro_view.py        # Pantalla ÚNICA para los 3 tipos de retiro (parametrizada)
│   │   └── result_view.py        # Pantalla de resultado
│   ├── controller/
│   │   └── cajero.py             # Fachada que usa la UI + bitácora de transacciones
│   ├── services/
│   │   ├── retiro_service.py     # Orquesta un retiro completo (valida, ejecuta, arma resultado)
│   │   └── inventario_service.py # Efectivo del cajero: disponibilidad y recarga por déficit
│   ├── validators/
│   │   └── validadores.py        # TODAS las validaciones (vectores, PIN, monto) en un solo lugar
│   ├── algorithms/
│   │   └── acarreo.py            # El algoritmo de acarreo (niveles) + matriz + combinaciones
│   ├── utils/
│   │   ├── constantes.py         # Denominaciones, longitudes, montos fijos, inventario inicial
│   │   └── helpers.py            # Normalización de vectores/moneda + clave temporal de NEQUI
│   └── repositories/
│       ├── cuenta_repository.py     # Persistencia de cuentas (identidad, sin saldo)
│       └── inventario_repository.py # Persistencia del efectivo del cajero
├── data/                          # cuentas.json, inventario.json, configuracion.json
└── tests/                         # Pruebas unitarias (pytest) — 32 casos, 4 archivos
```

---

## 5. Qué extendería primero

1. **Probar con más montos "de la vida real"** el algoritmo por niveles
   (ya es un port directo del que compartiste, no una inferencia mía) —
   coincide exacto con $200.000 y $300.000; sería bueno que lo corras con
   otros montos que uses en clase para confirmar que el patrón de
   reinicios también se ve como lo esperas para casos con varios niveles
   seguidos.
2. **Persistir la bitácora de transacciones** (`controller/transaccion.py`)
   a un archivo JSON/CSV, para tener historial real entre ejecuciones (hoy
   vive solo en memoria mientras la app está abierta).
3. **Empaquetar como ejecutable** (`pyinstaller`) para poder entregar un
   `.exe`/binario sin que el profesor tenga que instalar Python.
#   C a j e r o  
 