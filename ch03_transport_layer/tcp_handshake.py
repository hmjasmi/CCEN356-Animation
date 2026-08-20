"""
demo_tcp_handshake.py
======================
Example of using network_components.py to build a topic animation.

Render:
    manim -pql demo_tcp_handshake.py TCPHandshake
"""

from manim import *
from shared.network_components import (
    Host, Server, connect, send_packet, step_caption,
    REQUEST_COLOR, RESPONSE_COLOR,
)


class TCPHandshake(Scene):
    def construct(self):
        client = Host("Client").to_edge(LEFT, buff=1.5)
        server = Server("Server").to_edge(RIGHT, buff=1.5)
        link = connect(client, server)

        self.play(FadeIn(client), FadeIn(server))
        self.play(Create(link))

        caption = step_caption("Step 1: Client sends SYN")
        self.play(Write(caption))
        self.play(*send_packet(client, server, "SYN", color=REQUEST_COLOR))
        self.play(FadeOut(caption))

        caption = step_caption("Step 2: Server responds SYN-ACK")
        self.play(Write(caption))
        self.play(*send_packet(server, client, "SYN-ACK", color=RESPONSE_COLOR))
        self.play(FadeOut(caption))

        caption = step_caption("Step 3: Client sends ACK — connection established")
        self.play(Write(caption))
        self.play(*send_packet(client, server, "ACK", color=REQUEST_COLOR))
        self.play(FadeOut(caption))

        self.wait(1)
