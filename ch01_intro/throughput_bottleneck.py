"""
demo_throughput.py
====================
Animates "Throughput": bits flow from a server through link Rs, across the
network, through link Rc, to a client. Pipe HEIGHT encodes capacity, and
bits are emitted/served at a rate that actually reflects Rs and Rc — so
when Rs > Rc, a real FIFO queue visibly backs up at the narrow (Rc) pipe's
entrance, and when Rs < Rc it doesn't. Ends with the bottleneck-link
definition, matching the slide.

Render:
    manim -pql demo_throughput.py Throughput
"""

from manim import *
from shared.network_components import Server, Host, Cloud, pipe, LABEL_COLOR

BOTTLENECK_COLOR = "#FF5C5C"
FLOW_COLOR = "#4FA3FF"
THIN_H = 0.35
THICK_H = 0.9


class Throughput(Scene):
    def construct(self):
        title = Text("Throughput", font_size=40, color=BLUE).to_edge(UP, buff=0.3)
        self.play(Write(title))

        self.run_scenario(
            title,
            condition_markup="R<sub>s</sub> &lt; R<sub>c</sub>",
            rs_height=THIN_H, rc_height=THICK_H,
            t1=1.1, t2=0.4, emit_gap=0.9,
            bottleneck_is_rs=True,
        )
        self.run_scenario(
            title,
            condition_markup="R<sub>s</sub> &gt; R<sub>c</sub>",
            rs_height=THICK_H, rc_height=THIN_H,
            t1=0.4, t2=1.1, emit_gap=0.4,
            bottleneck_is_rs=False,
        )

        closing = VGroup(
            Text("bottleneck link", font_size=26, color=BOTTLENECK_COLOR, slant=ITALIC),
            Text("the link on the end-to-end path that constrains end-to-end throughput",
                 font_size=22, color=LABEL_COLOR),
        ).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        box = SurroundingRectangle(closing, color=BOTTLENECK_COLOR, buff=0.3)
        self.play(FadeIn(closing), Create(box))
        self.wait(1.5)

    def run_scenario(self, title, condition_markup, rs_height, rc_height, t1, t2, emit_gap, bottleneck_is_rs):
        header = MarkupText(
            f'<span foreground="{BOTTLENECK_COLOR}">{condition_markup}</span>'
            "  What is the average end-to-end throughput?",
            font_size=26,
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(header))

        y = -0.3
        server = Server("").scale(0.85).move_to([-6.3, y, 0])
        client = Host("").scale(0.85).move_to([6.2, y, 0])
        cloud = Cloud("").scale(1.1).move_to([-0.2, y, 0])

        pipe1_x0, pipe1_x1 = -5.3, -1.4
        pipe2_x0, pipe2_x1 = 1.0, 5.0

        pipe1 = pipe(pipe1_x1 - pipe1_x0, rs_height, "Rs bits/sec").move_to([(pipe1_x0 + pipe1_x1) / 2, y, 0])
        pipe2 = pipe(pipe2_x1 - pipe2_x0, rc_height, "Rc bits/sec").move_to([(pipe2_x0 + pipe2_x1) / 2, y, 0])

        arrows = VGroup(
            Arrow(server.icon.get_right(), [pipe1_x0, y, 0], buff=0.05, stroke_width=2,
                  color=BOTTLENECK_COLOR, max_tip_length_to_length_ratio=0.4),
            Arrow([pipe1_x1, y, 0], cloud.icon.get_left(), buff=0.05, stroke_width=2,
                  color=BOTTLENECK_COLOR, max_tip_length_to_length_ratio=0.4),
            Arrow(cloud.icon.get_right(), [pipe2_x0, y, 0], buff=0.05, stroke_width=2,
                  color=BOTTLENECK_COLOR, max_tip_length_to_length_ratio=0.4),
            Arrow([pipe2_x1, y, 0], client.icon.get_left(), buff=0.05, stroke_width=2,
                  color=BOTTLENECK_COLOR, max_tip_length_to_length_ratio=0.4),
        )

        self.play(
            FadeIn(server), FadeIn(client), FadeIn(cloud),
            FadeIn(pipe1), FadeIn(pipe2), Create(arrows),
        )

        # --- Flowing bits: emission rate & pipe crossing time literally
        # reflect Rs/Rc; pipe2 is a strict FIFO server (one bit at a time),
        # so if bits arrive faster than it can serve them, a real queue
        # backs up at its entrance. Each dot's entire journey (position +
        # visibility) is driven by ONE UpdateFromAlphaFunc as a pure
        # function of elapsed time — chaining several separate `.animate`
        # calls per dot doesn't compose correctly inside a Succession, since
        # each call snapshots the mobject's real (not-yet-animated) state.
        n = 6
        t_cloud = 0.25
        events = []  # (emit_time, arrival2, start2, end2)
        prev_end = 0
        for i in range(n):
            emit_time = i * emit_gap
            arrival2 = emit_time + t1 + t_cloud
            start2 = max(arrival2, prev_end)
            end2 = start2 + t2
            prev_end = end2
            events.append((emit_time, arrival2, start2, end2))

        total_time = events[-1][3] + 0.3

        def dot_state(i, t):
            """(x, opacity) for dot i at absolute local time t (seconds
            since this scenario's flow began)."""
            emit_time, arrival2, start2, end2 = events[i]
            hold_x = pipe2_x0 - 0.15 * i - 0.15
            if t < emit_time:
                return pipe1_x0, 0.0
            elif t < emit_time + t1:
                frac = (t - emit_time) / t1
                return pipe1_x0 + frac * (pipe1_x1 - pipe1_x0), 1.0
            elif t < arrival2:
                frac = (t - (emit_time + t1)) / t_cloud
                return pipe1_x1 + frac * (hold_x - pipe1_x1), 1.0
            elif t < start2:
                return hold_x, 1.0
            elif t < end2:
                frac = (t - start2) / t2
                return hold_x + frac * (pipe2_x1 - hold_x), 1.0
            else:
                return pipe2_x1, 0.0

        dots = VGroup(*[Dot(radius=0.09, color=FLOW_COLOR) for _ in range(n)])
        for d in dots:
            d.move_to([pipe1_x0, y, 0])
            d.set_opacity(0)
        self.add(dots)

        def make_updater(i):
            def updater(mob, alpha):
                t = alpha * total_time
                x, op = dot_state(i, t)
                mob.move_to([x, y, 0])
                mob.set_opacity(op)
            return updater

        anims = [UpdateFromAlphaFunc(dots[i], make_updater(i)) for i in range(n)]
        self.play(*anims, run_time=total_time, rate_func=linear)

        # --- Highlight the bottleneck link --------------------------------------
        bottleneck_pipe = pipe1 if bottleneck_is_rs else pipe2
        box = SurroundingRectangle(bottleneck_pipe, color=BOTTLENECK_COLOR, buff=0.08)
        label = Text("Throughput = min(Rs, Rc)", font_size=22, color=BOTTLENECK_COLOR)
        label.next_to(VGroup(pipe1, pipe2), DOWN, buff=0.6)
        self.play(Create(box), Write(label))
        self.wait(1)

        self.play(
            FadeOut(header), FadeOut(server), FadeOut(client), FadeOut(cloud),
            FadeOut(pipe1), FadeOut(pipe2), FadeOut(arrows), FadeOut(box), FadeOut(label),
        )
