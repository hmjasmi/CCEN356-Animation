"""
demo_protocol.py
=================
Animates "What's a protocol?": a human conversation (Hi / Hi / Got the
time? / 2:00) shown side by side with the analogous computer network
exchange (TCP handshake + HTTP GET/response), revealed as a sequence
diagram with messages appearing top to bottom.

Render:
    manim -pql demo_protocol.py WhatsAProtocol
"""

from manim import *
from shared.network_components import (
    Person, Host, Server, lifeline, message_arrow,
    REQUEST_COLOR, RESPONSE_COLOR, LABEL_COLOR,
)


class WhatsAProtocol(Scene):
    def construct(self):
        title = Text("What's a protocol?", font_size=40, color=BLUE).to_edge(UP, buff=0.3)
        subtitle = Text(
            "A human protocol and a computer network protocol:",
            font_size=24, color=LABEL_COLOR,
        ).next_to(title, DOWN, buff=0.25)
        self.play(Write(title))
        self.play(Write(subtitle))

        icon_y = subtitle.get_bottom()[1] - 0.7

        # --- Left: human protocol -------------------------------------------
        person_a = Person().scale(0.9).move_to([-6.0, icon_y, 0])
        person_b = Person().scale(0.9).move_to([-3.0, icon_y, 0])
        line_a = lifeline(person_a)
        line_b = lifeline(person_b)

        # --- Right: computer protocol ----------------------------------------
        client = Host("").scale(0.8).move_to([1.4, icon_y, 0])
        server = Server("").scale(0.8).move_to([5.6, icon_y, 0])
        line_c = lifeline(client)
        line_s = lifeline(server)

        # Divider between the two halves + shared "time" axis
        divider = Line([-0.8, icon_y + 0.5, 0], [-0.8, icon_y - 4.3, 0], color=GRAY, stroke_width=1)
        time_label = Text("time", font_size=22, color=LABEL_COLOR).move_to([-0.8, icon_y - 4.7, 0])
        time_arrow = Arrow([-0.8, icon_y - 5.0, 0], [-0.8, icon_y - 5.6, 0], color=GRAY, stroke_width=2)

        self.play(
            FadeIn(person_a), FadeIn(person_b), Create(line_a), Create(line_b),
            FadeIn(client), FadeIn(server), Create(line_c), Create(line_s),
            Create(divider),
        )
        self.play(Write(time_label), Create(time_arrow))

        # --- Message sequences (top to bottom) --------------------------------
        ax, bx = person_a.icon.get_center()[0], person_b.icon.get_center()[0]
        cx, sx = client.icon.get_center()[0], server.icon.get_center()[0]

        human_messages = [
            (ax, bx, "Hi", REQUEST_COLOR),
            (bx, ax, "Hi", REQUEST_COLOR),
            (ax, bx, "Got the time?", RESPONSE_COLOR),
            (bx, ax, "2:00", RESPONSE_COLOR),
        ]
        computer_messages = [
            (cx, sx, "TCP connection request", REQUEST_COLOR),
            (sx, cx, "TCP connection response", REQUEST_COLOR),
            (cx, sx, "GET http://gaia.cs.umass.edu/kurose_ross", RESPONSE_COLOR),
            (sx, cx, "<file>", RESPONSE_COLOR),
        ]

        start_y = icon_y - 1.1
        spacing = 0.85
        for i, ((hx1, hx2, htext, hcolor), (cx1, cx2, ctext, ccolor)) in enumerate(
            zip(human_messages, computer_messages)
        ):
            y = start_y - i * spacing
            human_arrow = message_arrow(hx1, hx2, y, htext, color=hcolor, label_size=22)
            comp_label_size = 14 if len(ctext) > 25 else 18
            comp_arrow = message_arrow(cx1, cx2, y, ctext, color=ccolor, label_size=comp_label_size)
            self.play(
                GrowArrow(human_arrow[0]), FadeIn(human_arrow[1]),
                GrowArrow(comp_arrow[0]), FadeIn(comp_arrow[1]),
            )

        # --- Closing question --------------------------------------------------
        question = Text("Q: other human protocols?", font_size=26, color=RED, slant=ITALIC)
        question.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(question))
        self.wait(1)
