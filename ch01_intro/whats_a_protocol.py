"""
whats_a_protocol.py
====================
Kurose & Ross §1.2 — "What is a protocol?"

Animates a human conversation (Hi / Hi / Got the time? / 2:00) side by
side with the analogous computer network exchange (TCP handshake +
HTTP GET/response), revealed as a sequence diagram with messages
appearing top to bottom.

Render:
    manim -pql whats_a_protocol.py WhatsAProtocol
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

        # --- Left: human protocol ---
        person_a = Person().scale(0.9).move_to([-6.0, icon_y, 0])
        person_b = Person().scale(0.9).move_to([-3.0, icon_y, 0])
        line_a = lifeline(person_a)
        line_b = lifeline(person_b)

        # --- Right: computer protocol ---
        client = Host("").scale(0.8).move_to([1.4, icon_y, 0])
        server = Server("").scale(0.8).move_to([5.6, icon_y, 0])
        line_c = lifeline(client)
        line_s = lifeline(server)

        divider = Line([-0.8, icon_y + 0.5, 0], [-0.8, icon_y - 4.3, 0], color=GRAY, stroke_width=1)
        time_label = Text("time", font_size=22, color=LABEL_COLOR).move_to([-0.8, icon_y - 4.7, 0])
        time_arrow = Arrow([-0.8, icon_y - 5.0, 0], [-0.8, icon_y - 5.6, 0], color=GRAY, stroke_width=2)

        self.play(
            FadeIn(person_a), FadeIn(person_b), Create(line_a), Create(line_b),
            FadeIn(client), FadeIn(server), Create(line_c), Create(line_s),
            Create(divider),
        )
        self.play(Write(time_label), Create(time_arrow))

        ax, bx = person_a.icon.get_center()[0], person_b.icon.get_center()[0]
        cx, sx = client.icon.get_center()[0], server.icon.get_center()[0]

        human_messages = [
            (ax, bx, "Hi", REQUEST_COLOR),
            (bx, ax, "Hi", REQUEST_COLOR),
            (ax, bx, "Got the time?", REQUEST_COLOR),
            (bx, ax, "2:00", RESPONSE_COLOR),
        ]
        computer_messages = [
            (cx, sx, "SYN", REQUEST_COLOR),
            (sx, cx, "SYN ACK", RESPONSE_COLOR),
            (cx, sx, "ACK", REQUEST_COLOR),
            (cx, sx, "GET index.html", REQUEST_COLOR),
            (sx, cx, "200 OK", RESPONSE_COLOR),
        ]

        y = icon_y - 0.9
        step = 0.75
        for (x1, x2, label, color), (hx1, hx2, hlabel, hcolor) in zip(computer_messages, human_messages + [None] * 10):
            pass  # placeholder to keep structure explicit if you want to interleave timing

        y = icon_y - 0.9
        for x1, x2, label, color in human_messages:
            arrow = message_arrow(x1, x2, y, label, color=color, label_size=18)
            self.play(Create(arrow), run_time=0.5)
            y -= step

        y = icon_y - 0.9
        for x1, x2, label, color in computer_messages:
            arrow = message_arrow(x1, x2, y, label, color=color, label_size=16)
            self.play(Create(arrow), run_time=0.5)
            y -= step * 0.85

        self.wait(2)
