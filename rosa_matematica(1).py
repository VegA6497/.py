from manim import *
import numpy as np


# ============================================================
# ROSA MATEMATICA 3D
# Manim Community v0.21.0
#
# Salida:
#   1080 x 1920
#   formato vertical 9:16
#   60 FPS
# ============================================================

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color = BLACK
config.disable_caching = False
config.max_files_cached = 1000


def crear_paneles():
    """Crea los tres paneles fijos con las ecuaciones."""

    paneles = []

    # --------------------------------------------------------
    # Ecuacion superior
    # --------------------------------------------------------
    formula_phi = MathTex(
        r"\varphi(\theta)=\frac{\pi}{2}e^{-\theta/(8\pi)}",
        font_size=40,
        color=BLUE_B,
    )
    formula_phi.move_to(UP * 6.55)

    caja_phi = RoundedRectangle(
        corner_radius=0.16,
        width=formula_phi.width + 0.60,
        height=formula_phi.height + 0.40,
        stroke_color=BLUE_B,
        stroke_width=2,
        fill_color=BLACK,
        fill_opacity=0,
    ).move_to(formula_phi)

    paneles.append((caja_phi, formula_phi))

    # --------------------------------------------------------
    # Ecuacion inferior izquierda
    # --------------------------------------------------------
    posicion_izquierda = LEFT * 2.28 + DOWN * 5.82

    formula_x = MathTex(
        r"X(\theta)=1-\frac12\left["
        r"\frac54\left(1-"
        r"\frac{(3.6\theta)\operatorname{mod}2\pi}{\pi}"
        r"\right)^2-\frac14"
        r"\right]^2",
        font_size=19,
        color=BLUE_B,
    )

    if formula_x.width > 3.88:
        formula_x.scale_to_fit_width(3.88)

    formula_x.move_to(posicion_izquierda)

    caja_x = RoundedRectangle(
        corner_radius=0.15,
        width=4.20,
        height=1.25,
        stroke_color=BLUE_B,
        stroke_width=2,
        fill_color=BLACK,
        fill_opacity=0,
    ).move_to(posicion_izquierda)

    paneles.append((caja_x, formula_x))

    # --------------------------------------------------------
    # Ecuacion inferior derecha
    # Una sola linea y ligeramente mayor.
    # --------------------------------------------------------
    posicion_derecha = RIGHT * 2.28 + DOWN * 5.82

    formula_xyz = MathTex(
        r"(x,y,z)=\left("
        r"r\sin\theta,"
        r"r\cos\theta,"
        r"X(x\cos\varphi-y\sin\varphi)"
        r"\right)",
        font_size=18,
        color=BLUE_B,
    )

    if formula_xyz.width > 4.02:
        formula_xyz.scale_to_fit_width(4.02)

    formula_xyz.move_to(posicion_derecha)

    caja_xyz = RoundedRectangle(
        corner_radius=0.15,
        width=4.20,
        height=1.25,
        stroke_color=BLUE_B,
        stroke_width=2,
        fill_color=BLACK,
        fill_opacity=0,
    ).move_to(posicion_derecha)

    paneles.append((caja_xyz, formula_xyz))

    return paneles


class RosaMatematica(ThreeDScene):
    """Animacion completa de una rosa matematica tridimensional."""

    def punto_rosa(self, x, theta):
        """Parametrizacion cartesiana usada para construir la superficie."""

        phi = (np.pi / 2) * np.exp(-theta / (8 * np.pi))

        X = 1 - 0.5 * (
            (5 / 4)
            * (
                1
                - np.mod(3.6 * theta, 2 * np.pi) / np.pi
            ) ** 2
            - 1 / 4
        ) ** 2

        y = (
            1.95653
            * x**2
            * (1.27689 * x - 1) ** 2
            * np.sin(phi)
        )

        r = X * (
            x * np.sin(phi)
            + y * np.cos(phi)
        )

        z = X * (
            x * np.cos(phi)
            - y * np.sin(phi)
        )

        return np.array([
            r * np.sin(theta),
            r * np.cos(theta),
            z,
        ])

    def construct(self):
        # ----------------------------------------------------
        # Camara inicial
        # ----------------------------------------------------
        self.set_camera_orientation(
            phi=72 * DEGREES,
            theta=-50 * DEGREES,
            zoom=1.12,
        )

        # ----------------------------------------------------
        # Ejes
        # ----------------------------------------------------
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-3, 4, 1],
            x_length=7,
            y_length=7,
            z_length=6,
            axis_config={
                "color": GREY_B,
                "stroke_width": 2,
                "include_ticks": True,
                "include_tip": True,
            },
        )

        x_label = MathTex(
            "x",
            font_size=28,
            color=WHITE,
        ).next_to(
            axes.x_axis.get_end(),
            RIGHT,
            buff=0.15,
        )

        y_label = MathTex(
            "y",
            font_size=28,
            color=WHITE,
        ).next_to(
            axes.y_axis.get_end(),
            UP,
            buff=0.15,
        )

        z_label = MathTex(
            "z",
            font_size=28,
            color=WHITE,
        ).next_to(
            axes.z_axis.get_end(),
            UP,
            buff=0.15,
        )

        # ----------------------------------------------------
        # Paneles fijos
        # ----------------------------------------------------
        paneles = crear_paneles()

        caja_phi, formula_phi = paneles[0]
        caja_x, formula_x = paneles[1]
        caja_xyz, formula_xyz = paneles[2]

        for caja, formula in paneles:
            caja.set_stroke(opacity=0)
            formula.set_opacity(0)
            self.add_fixed_in_frame_mobjects(caja, formula)

        # ----------------------------------------------------
        # Ejes
        # ----------------------------------------------------
        self.play(
            Create(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(z_label),
            run_time=2.5,
        )

        self.wait(0.5)

        # ----------------------------------------------------
        # Ecuacion superior: escritura real de Manim
        # ----------------------------------------------------
        formula_phi.set_opacity(1)

        self.play(
            caja_phi.animate.set_stroke(opacity=1),
            Write(formula_phi),
            run_time=1.8,
            rate_func=linear,
        )

        self.wait(0.35)

        # ----------------------------------------------------
        # Ecuacion inferior izquierda
        # ----------------------------------------------------
        formula_x.set_opacity(1)

        self.play(
            caja_x.animate.set_stroke(opacity=1),
            Write(formula_x),
            run_time=1.30,
            rate_func=linear,
        )

        # ----------------------------------------------------
        # Ecuacion inferior derecha
        # ----------------------------------------------------
        formula_xyz.set_opacity(1)

        self.play(
            caja_xyz.animate.set_stroke(opacity=1),
            Write(formula_xyz),
            run_time=1.30,
            rate_func=linear,
        )

        self.wait(0.40)

        # ----------------------------------------------------
        # Construccion segmentada de la rosa
        # ----------------------------------------------------
        numero_segmentos = 42

        valores_theta = np.linspace(
            -2 * PI,
            15 * PI,
            numero_segmentos + 1,
        )

        segmentos = []

        for i in range(numero_segmentos):
            segmento = Surface(
                lambda u, v: self.punto_rosa(u, v),
                u_range=[0, 1],
                v_range=[
                    valores_theta[i],
                    valores_theta[i + 1],
                ],
                resolution=(24, 8),
                fill_color=BLUE_D if i % 2 == 0 else BLUE_E,
                fill_opacity=0.96,
                stroke_color=BLUE_A,
                stroke_width=0.45,
            )

            segmento.scale(2.8)
            segmento.shift(UP * 0.15)
            segmentos.append(segmento)

        self.play(
            LaggedStart(
                *[
                    FadeIn(segmento, scale=0.15)
                    for segmento in segmentos
                ],
                lag_ratio=0.055,
            ),
            run_time=11,
            rate_func=smooth,
        )

        self.wait(1)

        # ----------------------------------------------------
        # Recorrido de camara
        # ----------------------------------------------------
        movimientos = [
            (60, -20, 1.12),
            (78, 35, 1.18),
            (30, 80, 1.12),
            (70, 125, 1.18),
            (85, 170, 1.15),
        ]

        for phi, theta, zoom in movimientos:
            self.move_camera(
                phi=phi * DEGREES,
                theta=theta * DEGREES,
                zoom=zoom,
                run_time=4,
            )
            self.wait(1)

        # ----------------------------------------------------
        # Rotacion continua
        # ----------------------------------------------------
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(12)
        self.stop_ambient_camera_rotation()

        # ----------------------------------------------------
        # Posicion final
        # ----------------------------------------------------
        self.move_camera(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            zoom=1.12,
            run_time=4,
        )

        self.wait(3)
