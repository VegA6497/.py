from manim import *
import numpy as np

# ================================================================
# FORMATO VERTICAL 9:16
# ================================================================
config.pixel_width = 720
config.pixel_height = 1280
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = BLACK


class SolucionProyectil(Scene):
    """
    Solución animada del problema 07 de movimiento parabólico.

    Datos:
        altura inicial = 9 m
        tiempo de vuelo = 3 s
        ángulo = 53 grados
        g = 10 m/s² hacia abajo

    Resultado:
        rapidez en B = 9*sqrt(5) m/s

    Render de prueba:
        manim -pql problema_proyectil.py SolucionProyectil

    Render en alta calidad:
        manim -pqh problema_proyectil.py SolucionProyectil
    """

    def construct(self):
        # ============================================================
        # 1. DATOS FÍSICOS DEL PROBLEMA
        # ============================================================
        g = 10.0
        theta = 53 * DEGREES
        t_final = 3.0
        altura_inicial = 9.0

        # Del movimiento vertical:
        # -9 = v0y(3) - 5(3)^2
        v0y = 12.0

        # Usando sin(53°) ≈ 4/5:
        v0 = 15.0
        v0x = 9.0

        # Velocidad final:
        vBx = v0x
        vBy = v0y - g * t_final
        rapidez_B = np.sqrt(vBx**2 + vBy**2)

        def x_pos(t):
            return v0x * t

        def y_pos(t):
            return altura_inicial + v0y * t - 0.5 * g * t**2

        def vy(t):
            return v0y - g * t

        def rapidez(t):
            return np.sqrt(v0x**2 + vy(t)**2)

        # ============================================================
        # 2. ENCABEZADO
        # ============================================================
        titulo = Text(
            "Movimiento parabólico",
            font_size=42,
            font="DejaVu Serif"
        ).move_to(UP * 7.15)

        subtitulo = Text(
            "Problema 07 · rapidez de impacto",
            font_size=23,
            font="DejaVu Serif"
        ).next_to(titulo, DOWN, buff=0.12)

        formula_principal = MathTex(
            r"\Delta y=v_{0y}t-\frac{1}{2}gt^2"
        ).scale(0.68).next_to(subtitulo, DOWN, buff=0.20)

        separador = Line(
            LEFT * 1.35,
            RIGHT * 1.35,
            color=GREY_B,
            stroke_width=1.5
        ).next_to(formula_principal, DOWN, buff=0.16)

        self.play(
            FadeIn(titulo, shift=DOWN * 0.12),
            FadeIn(subtitulo, shift=DOWN * 0.12),
            Write(formula_principal),
            Create(separador),
            run_time=1.6
        )

        # ============================================================
        # 3. DIAGRAMA CENTRAL
        # ============================================================
        marco = Rectangle(
            width=7.45,
            height=5.65,
            stroke_color=GREY_B,
            stroke_width=2
        ).move_to(UP * 2.35)

        axes = Axes(
            x_range=[0, 30, 5],
            y_range=[0, 18, 3],
            x_length=6.75,
            y_length=5.05,
            axis_config={
                "include_ticks": False,
                "include_tip": True,
                "stroke_width": 1.4,
                "color": GREY_B
            }
        ).move_to(marco.get_center() + LEFT * 0.08 + DOWN * 0.08)

        suelo = Line(
            axes.c2p(0, 0),
            axes.c2p(30, 0),
            color=GREY_A,
            stroke_width=4
        )

        etiqueta_x = MathTex("x").scale(0.48).next_to(
            axes.x_axis.get_end(), DOWN, buff=0.05
        )
        etiqueta_y = MathTex("y").scale(0.48).next_to(
            axes.y_axis.get_end(), LEFT, buff=0.05
        )

        punto_A = Dot(axes.c2p(0, altura_inicial), radius=0.085, color=YELLOW)
        punto_B = Dot(axes.c2p(27, 0), radius=0.085, color=GREEN_C)

        rotulo_A = MathTex("A").scale(0.60).next_to(punto_A, LEFT, buff=0.10)
        rotulo_B = MathTex("B").scale(0.60).next_to(punto_B, RIGHT, buff=0.10)

        linea_altura = DoubleArrow(
            axes.c2p(0.75, 0),
            axes.c2p(0.75, altura_inicial),
            buff=0,
            color=BLUE_B,
            stroke_width=2.5
        )

        etiqueta_altura = MathTex(
            r"9\ \mathrm{m}"
        ).scale(0.52).next_to(linea_altura, RIGHT, buff=0.08)

        curva = axes.plot(
            lambda x: altura_inicial
                      + (v0y / v0x) * x
                      - (g / (2 * v0x**2)) * x**2,
            x_range=[0, 27],
            color=YELLOW,
            stroke_width=3.5
        )

        # Flecha de velocidad inicial
        escala_vec = 0.34
        flecha_v0 = Arrow(
            axes.c2p(0, altura_inicial),
            axes.c2p(v0x * escala_vec, altura_inicial + v0y * escala_vec),
            buff=0,
            color=WHITE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.18
        )

        rotulo_v0 = MathTex(r"\vec v_0").scale(0.55).next_to(
            flecha_v0.get_center(), UP + LEFT, buff=0.04
        )

        arco_theta = Arc(
            radius=0.55,
            start_angle=0,
            angle=theta,
            arc_center=axes.c2p(0, altura_inicial),
            color=RED_C,
            stroke_width=2.5
        )

        rotulo_theta = MathTex(r"53^\circ").scale(0.48).move_to(
            axes.c2p(2.7, 10.0)
        )

        datos = VGroup(
            MathTex(r"t=3\ \mathrm{s}"),
            MathTex(r"\vec g=-10\,\hat{\jmath}\ \mathrm{m/s^2}")
        ).arrange(RIGHT, buff=0.55).scale(0.50)
        datos.next_to(marco, DOWN, buff=0.25)

        self.play(
            Create(marco),
            Create(axes),
            Create(suelo),
            FadeIn(etiqueta_x),
            FadeIn(etiqueta_y),
            FadeIn(punto_A),
            FadeIn(punto_B),
            FadeIn(rotulo_A),
            FadeIn(rotulo_B),
            GrowArrow(linea_altura),
            FadeIn(etiqueta_altura),
            run_time=1.3
        )

        self.play(
            Create(curva),
            GrowArrow(flecha_v0),
            FadeIn(rotulo_v0),
            Create(arco_theta),
            FadeIn(rotulo_theta),
            FadeIn(datos),
            run_time=1.4
        )

        # ============================================================
        # 4. PASO 1: MOVIMIENTO VERTICAL
        # ============================================================
        mensaje_1 = Text(
            "1. Hallamos la velocidad inicial vertical",
            font_size=24,
            color=YELLOW
        ).move_to(DOWN * 4.35)

        ecuacion_1 = MathTex(
            r"-9=v_0\sin53^\circ(3)-\frac12(10)(3)^2"
        ).scale(0.61).move_to(DOWN * 5.05)

        ecuacion_2 = MathTex(
            r"-9=3v_0\left(\frac45\right)-45"
        ).scale(0.66).move_to(DOWN * 5.05)

        ecuacion_3 = MathTex(
            r"36=\frac{12}{5}v_0"
        ).scale(0.72).move_to(DOWN * 5.05)

        ecuacion_4 = MathTex(
            r"\boxed{v_0=15\ \mathrm{m/s}}"
        ).scale(0.73).move_to(DOWN * 5.05)

        aproximaciones = MathTex(
            r"\sin53^\circ\approx\frac45,\qquad"
            r"\cos53^\circ\approx\frac35"
        ).scale(0.50).move_to(DOWN * 5.75)

        self.play(FadeIn(mensaje_1, shift=UP * 0.10))
        self.play(Write(ecuacion_1), run_time=1.2)
        self.wait(0.7)

        self.play(
            TransformMatchingTex(ecuacion_1, ecuacion_2),
            FadeIn(aproximaciones),
            run_time=1.0
        )
        self.wait(0.7)

        self.play(TransformMatchingTex(ecuacion_2, ecuacion_3))
        self.wait(0.6)

        self.play(TransformMatchingTex(ecuacion_3, ecuacion_4))
        self.wait(1.0)

        # ============================================================
        # 5. PASO 2: COMPONENTES INICIALES
        # ============================================================
        mensaje_2 = Text(
            "2. Descomponemos la velocidad inicial",
            font_size=24,
            color=BLUE_B
        ).move_to(DOWN * 4.35)

        componentes = VGroup(
            MathTex(
                r"v_{0x}=15\cos53^\circ=15\left(\frac35\right)=9"
            ),
            MathTex(
                r"v_{0y}=15\sin53^\circ=15\left(\frac45\right)=12"
            )
        ).arrange(DOWN, buff=0.18).scale(0.57)
        componentes.move_to(DOWN * 5.25)

        flecha_vx0 = Arrow(
            axes.c2p(0, altura_inicial),
            axes.c2p(v0x * escala_vec, altura_inicial),
            buff=0,
            color=BLUE_B,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.22
        )

        flecha_vy0 = Arrow(
            axes.c2p(v0x * escala_vec, altura_inicial),
            axes.c2p(v0x * escala_vec, altura_inicial + v0y * escala_vec),
            buff=0,
            color=RED_B,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.22
        )

        self.play(
            ReplacementTransform(mensaje_1, mensaje_2),
            FadeOut(ecuacion_4),
            FadeOut(aproximaciones),
            TransformFromCopy(flecha_v0, flecha_vx0),
            TransformFromCopy(flecha_v0, flecha_vy0),
            FadeIn(componentes),
            run_time=1.2
        )
        self.wait(1.4)

        # ============================================================
        # 6. SIMULACIÓN DINÁMICA DEL VUELO
        # ============================================================
        self.play(
            FadeOut(componentes),
            FadeOut(flecha_v0),
            FadeOut(flecha_vx0),
            FadeOut(flecha_vy0),
            FadeOut(rotulo_v0),
            FadeOut(arco_theta),
            FadeOut(rotulo_theta),
            FadeOut(curva),
            FadeOut(mensaje_2),
            run_time=0.8
        )

        tiempo = ValueTracker(0.0)

        proyectil = always_redraw(
            lambda: Dot(
                axes.c2p(
                    x_pos(tiempo.get_value()),
                    max(0, y_pos(tiempo.get_value()))
                ),
                radius=0.09,
                color=RED_C
            )
        )

        trayectoria = TracedPath(
            proyectil.get_center,
            stroke_color=YELLOW,
            stroke_width=4
        )

        vector_v = always_redraw(
            lambda: Arrow(
                proyectil.get_center(),
                axes.c2p(
                    x_pos(tiempo.get_value()) + v0x * 0.22,
                    max(0, y_pos(tiempo.get_value())) + vy(tiempo.get_value()) * 0.22
                ),
                buff=0,
                color=WHITE,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.20
            )
        )

        vector_vx = always_redraw(
            lambda: Arrow(
                proyectil.get_center(),
                axes.c2p(
                    x_pos(tiempo.get_value()) + v0x * 0.22,
                    max(0, y_pos(tiempo.get_value()))
                ),
                buff=0,
                color=BLUE_B,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25
            )
        )

        vector_vy = always_redraw(
            lambda: Arrow(
                proyectil.get_center(),
                axes.c2p(
                    x_pos(tiempo.get_value()),
                    max(0, y_pos(tiempo.get_value())) + vy(tiempo.get_value()) * 0.22
                ),
                buff=0,
                color=RED_B,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25
            )
        )

        num_t = DecimalNumber(0, num_decimal_places=2).scale(0.50)
        num_x = DecimalNumber(0, num_decimal_places=1).scale(0.50)
        num_y = DecimalNumber(altura_inicial, num_decimal_places=1).scale(0.50)
        num_vy = DecimalNumber(v0y, num_decimal_places=1, include_sign=True).scale(0.50)
        num_v = DecimalNumber(v0, num_decimal_places=1).scale(0.50)

        num_t.add_updater(lambda m: m.set_value(tiempo.get_value()))
        num_x.add_updater(lambda m: m.set_value(x_pos(tiempo.get_value())))
        num_y.add_updater(
            lambda m: m.set_value(max(0, y_pos(tiempo.get_value())))
        )
        num_vy.add_updater(lambda m: m.set_value(vy(tiempo.get_value())))
        num_v.add_updater(lambda m: m.set_value(rapidez(tiempo.get_value())))

        fila_1 = VGroup(
            Text("t =", font_size=19),
            num_t,
            MathTex(r"\mathrm{s}")
        ).arrange(RIGHT, buff=0.08)

        fila_2 = VGroup(
            Text("(x, y) =", font_size=19),
            MathTex("("),
            num_x,
            MathTex(","),
            num_y,
            MathTex(r")\ \mathrm{m}")
        ).arrange(RIGHT, buff=0.06)

        fila_3 = VGroup(
            MathTex(r"v_y="),
            num_vy,
            MathTex(r"\mathrm{m/s}"),
            MathTex(r"\qquad |\vec v|="),
            num_v,
            MathTex(r"\mathrm{m/s}")
        ).arrange(RIGHT, buff=0.06)

        panel_dinamico = VGroup(
            fila_1,
            fila_2,
            fila_3
        ).arrange(DOWN, buff=0.10).scale(0.82)
        panel_dinamico.move_to(DOWN * 5.15)

        mensaje_vuelo = Text(
            "La componente horizontal permanece constante",
            font_size=22,
            color=BLUE_B
        ).move_to(DOWN * 4.30)

        self.add(trayectoria)
        self.play(
            FadeIn(proyectil),
            FadeIn(vector_v),
            FadeIn(vector_vx),
            FadeIn(vector_vy),
            FadeIn(panel_dinamico),
            FadeIn(mensaje_vuelo),
            run_time=0.8
        )

        self.play(
            tiempo.animate.set_value(t_final),
            run_time=5.2,
            rate_func=linear
        )

        # ============================================================
        # 7. PASO 3: VELOCIDAD EN B
        # ============================================================
        self.play(
            FadeOut(vector_v),
            FadeOut(vector_vx),
            FadeOut(vector_vy),
            FadeOut(panel_dinamico),
            FadeOut(mensaje_vuelo),
            run_time=0.6
        )

        mensaje_3 = Text(
            "3. Calculamos las componentes al llegar a B",
            font_size=23,
            color=RED_C
        ).move_to(DOWN * 4.30)

        ecuaciones_B = VGroup(
            MathTex(r"v_{Bx}=v_{0x}=9\ \mathrm{m/s}"),
            MathTex(
                r"v_{By}=v_{0y}-gt=12-10(3)=-18\ \mathrm{m/s}"
            )
        ).arrange(DOWN, buff=0.18).scale(0.56)
        ecuaciones_B.move_to(DOWN * 5.12)

        flecha_Bx = Arrow(
            axes.c2p(27, 0),
            axes.c2p(29.7, 0),
            buff=0,
            color=BLUE_B,
            stroke_width=4
        )

        flecha_By = Arrow(
            axes.c2p(27, 4.8),
            axes.c2p(27, 0),
            buff=0,
            color=RED_B,
            stroke_width=4
        )

        self.play(
            FadeIn(mensaje_3),
            FadeIn(ecuaciones_B),
            GrowArrow(flecha_Bx),
            GrowArrow(flecha_By),
            run_time=1.2
        )
        self.wait(1.4)

        # ============================================================
        # 8. RAPIDEZ FINAL
        # ============================================================
        mensaje_4 = Text(
            "4. Magnitud de la velocidad de impacto",
            font_size=23,
            color=GREEN_C
        ).move_to(DOWN * 4.30)

        rapidez_1 = MathTex(
            r"v_B=\sqrt{v_{Bx}^2+v_{By}^2}"
        ).scale(0.66).move_to(DOWN * 5.02)

        rapidez_2 = MathTex(
            r"v_B=\sqrt{9^2+(-18)^2}"
        ).scale(0.70).move_to(DOWN * 5.02)

        rapidez_3 = MathTex(
            r"v_B=\sqrt{405}=9\sqrt5\ \mathrm{m/s}"
        ).scale(0.70).move_to(DOWN * 5.02)

        respuesta = VGroup(
            MathTex(
                r"\boxed{v_B=9\sqrt5\ \mathrm{m/s}}"
            ).scale(0.78),
            Text(
                "Alternativa D",
                font_size=25,
                color=GREEN_C
            )
        ).arrange(DOWN, buff=0.16).move_to(DOWN * 6.20)

        self.play(
            ReplacementTransform(mensaje_3, mensaje_4),
            FadeOut(ecuaciones_B),
            Write(rapidez_1),
            run_time=0.9
        )
        self.wait(0.6)

        self.play(TransformMatchingTex(rapidez_1, rapidez_2))
        self.wait(0.6)

        self.play(TransformMatchingTex(rapidez_2, rapidez_3))
        self.wait(0.8)

        self.play(
            FadeIn(respuesta, shift=UP * 0.12),
            Circumscribe(
                rapidez_3,
                color=GREEN_C,
                fade_out=True
            ),
            run_time=1.3
        )

        self.wait(3)
