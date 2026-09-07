# Rosa matemática 3D con Manim

Animación vertical de una **rosa matemática tridimensional** creada con [Manim Community](https://www.manim.community/).

El proyecto genera la animación completa desde cero: ejes cartesianos, ecuaciones con efecto de escritura, construcción progresiva de la superficie y recorrido de cámara en 3D.

## Resultado

- Resolución: **1080 × 1920**
- Relación de aspecto: **9:16**
- Frecuencia: **60 FPS**
- Fondo: negro
- Render: Manim Community
- Escena principal: `RosaMatematica`

## Matemática usada

La animación parte de

\[
\varphi(\theta)=\frac{\pi}{2}e^{-\theta/(8\pi)}
\]

y de

\[
X(\theta)=
1-\frac12
\left[
\frac54
\left(
1-\frac{(3.6\theta)\operatorname{mod}2\pi}{\pi}
\right)^2
-\frac14
\right]^2.
\]

Se introduce además la función auxiliar

\[
y=
1.95653\,x^2(1.27689x-1)^2\sin\varphi,
\]

con

\[
r=X(x\sin\varphi+y\cos\varphi),
\]

y finalmente la parametrización cartesiana

\[
(x_{\mathrm{3D}},y_{\mathrm{3D}},z)
=
\left(
r\sin\theta,\,
r\cos\theta,\,
X(x\cos\varphi-y\sin\varphi)
\right).
\]

El código implementa directamente estas expresiones en `punto_rosa()`.

## Requisitos

- Python 3.11 o superior
- Manim Community 0.21.0
- NumPy
- FFmpeg
- Una distribución LaTeX compatible con `MathTex`

En Windows puedes usar, por ejemplo, **MiKTeX** o **TeX Live** para LaTeX.

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/TU-USUARIO/rosa-matematica-manim.git
cd rosa-matematica-manim
```

Crea un entorno virtual:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias de Python:

```bash
pip install -r requirements.txt
```

Comprueba Manim:

```bash
manim --version
```

## Renderizar

El archivo ya configura internamente 1080 × 1920 y 60 FPS.

```bash
manim rosa_matematica.py RosaMatematica
```

Para abrir automáticamente el resultado al terminar:

```bash
manim -p rosa_matematica.py RosaMatematica
```

El video se guardará dentro de la carpeta `media/` creada automáticamente por Manim.

## Estructura

```text
rosa-matematica-manim/
├── rosa_matematica.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Detalles de la animación

Las ecuaciones se mantienen fijas respecto de la pantalla mientras la cámara gira en el espacio 3D. El efecto de escritura utiliza `Write()` de Manim; no es una superposición añadida posteriormente.

La superficie se divide en 42 segmentos y aparece mediante `LaggedStart`, lo que produce la sensación de crecimiento progresivo de la rosa.

## Personalización rápida

En `rosa_matematica.py` puedes modificar:

- `numero_segmentos`: cantidad de secciones de la rosa.
- `resolution=(24, 8)`: resolución de cada sección.
- `segmento.scale(2.8)`: tamaño de la rosa.
- `run_time=11`: duración de su construcción.
- `movimientos`: posiciones utilizadas durante el recorrido de cámara.
- `config.frame_rate`: FPS del video.

## Licencia

El código puede publicarse con la licencia que prefieras. Si quieres distribuirlo como software libre, puedes añadir una licencia MIT, BSD o GPL al repositorio.
