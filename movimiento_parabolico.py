from manim import *
import numpy as np


class MovimientoParabolico(Scene):
    """
    Animación didáctica del movimiento parabólico.

    Compatible con Manim Community 0.19.x.
    Render de prueba:
        manim -pql movimiento_parabolico.py MovimientoParabolico

    Render en alta calidad:
        manim -pqh movimiento_parabolico.py MovimientoParabolico
    """

    def construct(self):
        # ============================================================
        # 1. PARÁMETROS FÍSICOS
        # ============================================================
        v0 = 8.0                         # rapidez inicial, en m/s
        theta = 55 * DEGREES             # ángulo de lanzamiento
        g = 9.8                          # aceleración gravitatoria, en m/s²

        vx0 = v0 * np.cos(theta)
        vy0 = v0 * np.sin(theta)

        tiempo_subida = vy0 / g
        tiempo_vuelo = 2 * vy0 / g
        alcance = vx0 * tiempo_vuelo
        altura_maxima = vy0**2 / (2 * g)

        # Funciones cinemáticas
        def x_pos(t):
            return vx0 * t

        def y_pos(t):
            return vy0 * t - 0.5 * g * t**2

        def vy(t):
            return vy0 - g * t

        # ============================================================
        # 2. TÍTULO
        # ============================================================
        titulo = Text(
            "Movimiento parabólico de un proyectil",
            font_size=40,
            weight=BOLD
        ).to_edge(UP)

        subtitulo = Text(
            "Composición de un movimiento horizontal uniforme y uno vertical acelerado",
            font_size=22
        ).next_to(titulo, DOWN, buff=0.12)

        self.play(Write(titulo), FadeIn(subtitulo, shift=DOWN))
        self.wait(0.5)

        # ============================================================
        # 3. SISTEMA DE COORDENADAS
        # ============================================================
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 3, 0.5],
            x_length=8.3,
            y_length=4.6,
            axis_config={
                "include_tip": True,
                "stroke_width": 2,
            },
            x_axis_config={
                "numbers_to_include": np.arange(0, 8, 1),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0.5, 3.1, 0.5),
            },
            tips=True,
        ).shift(LEFT * 2.0 + DOWN * 0.9)

        labels_ejes = axes.get_axis_labels(
            x_label=MathTex("x\\;(\\mathrm{m})"),
            y_label=MathTex("y\\;(\\mathrm{m})")
        )

        suelo = Line(
            axes.c2p(0, 0),
            axes.c2p(7, 0),
            stroke_width=5
        )

        self.play(
            Create(axes),
            FadeIn(labels_ejes),
            Create(suelo)
        )

        # ============================================================
        # 4. PANEL DE ECUACIONES
        # ============================================================
        parametros = VGroup(
            MathTex(r"v_0 = 8.0\ \mathrm{m/s}"),
            MathTex(r"\theta = 55^\circ"),
            MathTex(r"g = 9.8\ \mathrm{m/s^2}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).scale(0.58)

        ecuaciones = VGroup(
            MathTex(r"x(t)=v_0\cos\theta\,t"),
            MathTex(r"y(t)=v_0\sin\theta\,t-\frac{1}{2}gt^2"),
            MathTex(r"v_x=v_0\cos\theta"),
            MathTex(r"v_y=v_0\sin\theta-gt")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20).scale(0.54)

        panel = VGroup(parametros, ecuaciones).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.38
        )

        caja_panel = SurroundingRectangle(
            panel,
            buff=0.22,
            corner_radius=0.12,
            stroke_width=1.5
        )

        grupo_panel = VGroup(caja_panel, panel)
        grupo_panel.to_corner(UR).shift(DOWN * 1.15 + LEFT * 0.05)

        self.play(FadeIn(grupo_panel, shift=LEFT))
        self.wait(0.5)

        # ============================================================
        # 5. PROYECTIL Y VELOCIDAD INICIAL
        # ============================================================
        tiempo = ValueTracker(0.0)

        proyectil = always_redraw(
            lambda: Dot(
                axes.c2p(x_pos(tiempo.get_value()), y_pos(tiempo.get_value())),
                radius=0.10
            )
        )

        punto_inicial = axes.c2p(0, 0)

        # Las flechas se construyen en coordenadas físicas:
        # una pequeña fracción de segundo convierte velocidad en longitud visual.
        escala_vector = 0.16

        vector_v0 = Arrow(
            start=punto_inicial,
            end=axes.c2p(vx0 * escala_vector, vy0 * escala_vector),
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.20
        )

        componente_x0 = Arrow(
            start=punto_inicial,
            end=axes.c2p(vx0 * escala_vector, 0),
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.25
        )

        componente_y0 = Arrow(
            start=axes.c2p(vx0 * escala_vector, 0),
            end=axes.c2p(vx0 * escala_vector, vy0 * escala_vector),
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.25
        )

        etiqueta_v0 = MathTex(r"\vec v_0").scale(0.65).next_to(
            vector_v0.get_center(), UP + LEFT, buff=0.05
        )
        etiqueta_vx0 = MathTex(r"v_{0x}=v_0\cos\theta").scale(0.50).next_to(
            componente_x0, DOWN, buff=0.08
        )
        etiqueta_vy0 = MathTex(r"v_{0y}=v_0\sin\theta").scale(0.50).next_to(
            componente_y0, RIGHT, buff=0.08
        )

        arco_angulo = Arc(
            radius=0.65,
            start_angle=0,
            angle=theta,
            arc_center=punto_inicial
        )
        etiqueta_theta = MathTex(r"\theta").scale(0.55).next_to(
            arco_angulo.point_from_proportion(0.55),
            RIGHT,
            buff=0.04
        )

        self.play(FadeIn(proyectil))
        self.play(
            GrowArrow(vector_v0),
            Create(arco_angulo),
            FadeIn(etiqueta_v0),
            FadeIn(etiqueta_theta)
        )
        self.play(
            TransformFromCopy(vector_v0, componente_x0),
            TransformFromCopy(vector_v0, componente_y0),
            FadeIn(etiqueta_vx0),
            FadeIn(etiqueta_vy0)
        )
        self.wait(1.2)

        self.play(
            FadeOut(
                vector_v0,
                componente_x0,
                componente_y0,
                etiqueta_v0,
                etiqueta_vx0,
                etiqueta_vy0,
                arco_angulo,
                etiqueta_theta
            )
        )

        # ============================================================
        # 6. ELEMENTOS DINÁMICOS DURANTE EL VUELO
        # ============================================================
        trayectoria = TracedPath(
            proyectil.get_center,
            stroke_width=5
        )

        vector_vx = always_redraw(
            lambda: Arrow(
                start=axes.c2p(
                    x_pos(tiempo.get_value()),
                    y_pos(tiempo.get_value())
                ),
                end=axes.c2p(
                    x_pos(tiempo.get_value()) + vx0 * escala_vector,
                    y_pos(tiempo.get_value())
                ),
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25
            )
        )

        vector_vy = always_redraw(
            lambda: Arrow(
                start=axes.c2p(
                    x_pos(tiempo.get_value()),
                    y_pos(tiempo.get_value())
                ),
                end=axes.c2p(
                    x_pos(tiempo.get_value()),
                    y_pos(tiempo.get_value()) + vy(tiempo.get_value()) * escala_vector
                ),
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25
            )
        )

        etiqueta_vx = always_redraw(
            lambda: MathTex(r"v_x").scale(0.48).next_to(
                vector_vx.get_end(),
                DOWN,
                buff=0.05
            )
        )

        etiqueta_vy = always_redraw(
            lambda: MathTex(r"v_y").scale(0.48).next_to(
                vector_vy.get_end(),
                RIGHT,
                buff=0.05
            )
        )

        flecha_gravedad = Arrow(
            start=axes.c2p(6.4, 2.6),
            end=axes.c2p(6.4, 1.9),
            buff=0,
            stroke_width=5
        )
        etiqueta_g = MathTex(r"\vec g").scale(0.62).next_to(
            flecha_gravedad,
            RIGHT,
            buff=0.10
        )

        reloj_numero = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=False
        ).scale(0.58)

        reloj_numero.add_updater(
            lambda m: m.set_value(tiempo.get_value())
        )

        reloj = VGroup(
            MathTex(r"t="),
            reloj_numero,
            MathTex(r"\ \mathrm{s}")
        ).arrange(RIGHT, buff=0.07).scale(0.80)

        reloj.next_to(axes, UP, buff=0.12).shift(LEFT * 1.0)

        self.add(trayectoria)
        self.play(
            FadeIn(vector_vx),
            FadeIn(vector_vy),
            FadeIn(etiqueta_vx),
            FadeIn(etiqueta_vy),
            GrowArrow(flecha_gravedad),
            FadeIn(etiqueta_g),
            FadeIn(reloj)
        )

        # ============================================================
        # 7. ASCENSO HASTA LA ALTURA MÁXIMA
        # ============================================================
        texto_ascenso = Text(
            "Durante el ascenso:  vᵧ > 0",
            font_size=26
        ).next_to(axes, DOWN, buff=0.42).shift(LEFT * 0.7)

        self.play(FadeIn(texto_ascenso))
        self.play(
            tiempo.animate.set_value(tiempo_subida),
            run_time=3.2,
            rate_func=linear
        )

        self.play(FadeOut(texto_ascenso))

        # Punto y líneas auxiliares en la altura máxima
        punto_cima = Dot(
            axes.c2p(alcance / 2, altura_maxima),
            radius=0.08
        )

        linea_altura = DashedLine(
            axes.c2p(alcance / 2, 0),
            axes.c2p(alcance / 2, altura_maxima),
            dash_length=0.12
        )

        etiqueta_cima = MathTex(
            r"v_y=0"
        ).scale(0.65).next_to(punto_cima, UP, buff=0.12)

        texto_cima = Text(
            "En la altura máxima, la velocidad vertical se anula",
            font_size=24
        ).next_to(axes, DOWN, buff=0.42).shift(LEFT * 0.55)

        self.play(
            FadeIn(punto_cima),
            Create(linea_altura),
            FadeIn(etiqueta_cima),
            FadeIn(texto_cima)
        )
        self.wait(1.5)

        # ============================================================
        # 8. DESCENSO
        # ============================================================
        self.play(FadeOut(texto_cima))

        texto_descenso = Text(
            "Durante el descenso:  vᵧ < 0",
            font_size=26
        ).next_to(axes, DOWN, buff=0.42).shift(LEFT * 0.7)

        self.play(FadeIn(texto_descenso))
        self.play(
            tiempo.animate.set_value(tiempo_vuelo),
            run_time=3.2,
            rate_func=linear
        )
        self.play(FadeOut(texto_descenso))

        # ============================================================
        # 9. RESULTADOS: ALTURA, ALCANCE Y TIEMPO DE VUELO
        # ============================================================
        curva_teorica = axes.plot(
            lambda x: x * np.tan(theta)
                      - (g * x**2) / (2 * v0**2 * np.cos(theta)**2),
            x_range=[0, alcance],
            stroke_width=3
        )

        linea_alcance = DoubleArrow(
            axes.c2p(0, -0.12),
            axes.c2p(alcance, -0.12),
            buff=0,
            stroke_width=3
        )

        etiqueta_alcance = MathTex(
            rf"R={alcance:.2f}\ \mathrm{{m}}"
        ).scale(0.62).next_to(linea_alcance, DOWN, buff=0.08)

        etiqueta_altura = MathTex(
            rf"h_{{\max}}={altura_maxima:.2f}\ \mathrm{{m}}"
        ).scale(0.58).next_to(linea_altura, LEFT, buff=0.10)

        resultados = VGroup(
            MathTex(
                rf"t_{{\mathrm{{vuelo}}}}={tiempo_vuelo:.2f}\ \mathrm{{s}}"
            ),
            MathTex(
                rf"R=\frac{{v_0^2\sin(2\theta)}}{{g}}={alcance:.2f}\ \mathrm{{m}}"
            ),
            MathTex(
                rf"h_{{\max}}=\frac{{v_0^2\sin^2\theta}}{{2g}}={altura_maxima:.2f}\ \mathrm{{m}}"
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).scale(0.48)

        caja_resultados = SurroundingRectangle(
            resultados,
            buff=0.18,
            corner_radius=0.10,
            stroke_width=1.4
        )

        grupo_resultados = VGroup(caja_resultados, resultados)
        grupo_resultados.next_to(grupo_panel, DOWN, buff=0.25).align_to(
            grupo_panel,
            LEFT
        )

        self.play(
            Create(curva_teorica),
            Create(linea_alcance),
            FadeIn(etiqueta_alcance),
            FadeIn(etiqueta_altura),
            FadeIn(grupo_resultados)
        )

        texto_final = Text(
            "La trayectoria es una parábola",
            font_size=30,
            weight=BOLD
        ).next_to(axes, DOWN, buff=0.42).shift(LEFT * 0.65)

        self.play(Write(texto_final))
        self.wait(3)
