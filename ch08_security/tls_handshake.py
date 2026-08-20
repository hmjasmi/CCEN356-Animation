"""
tls_handshake.py
==================
Kurose & Ross §8.6 — Securing TCP Connections: TLS.

A simplified TLS handshake: ClientHello -> ServerHello + certificate ->
key exchange -> both sides derive a shared session key (padlock closes) ->
subsequent application data is shown encrypted (purple/SECURE_COLOR).

This is a new scene (no earlier draft of it existed in prior sessions) —
written in the same visual language as the rest of the course: `Host`/
`Server` icons, `send_packet` for message motion, `step_caption` for
narration, and the shared color code (blue = request, green = response,
purple = secure/encrypted).

Render:
    manim -pql tls_handshake.py TLSHandshake
"""

from manim import *
from shared.network_components import (
    Host, Server, Lock, connect, send_packet, step_caption,
    REQUEST_COLOR, RESPONSE_COLOR, SECURE_COLOR, ERROR_COLOR, LABEL_COLOR,
)


class TLSHandshake(Scene):
    def construct(self):
        title = Text("TLS Handshake", font_size=40, color=BLUE).to_edge(UP, buff=0.3)
        self.play(Write(title))

        client = Host("Client").to_edge(LEFT, buff=1.8)
        server = Server("Server").to_edge(RIGHT, buff=1.8)
        link = connect(client, server)
        self.play(FadeIn(client), FadeIn(server), Create(link))

        # An open padlock hovers over the link — closes once the shared
        # key is established
        lock = Lock("", locked=False).scale(0.7).move_to(link.get_center() + UP * 1.3)
        self.play(FadeIn(lock))

        def step(label_text, from_node, to_node, msg, color):
            caption = step_caption(label_text)
            caption.next_to(title, DOWN, buff=0.3)
            self.play(Write(caption))
            self.play(*send_packet(from_node, to_node, msg, color=color))
            self.play(FadeOut(caption))

        step("Step 1: Client sends supported cipher suites",
             client, server, "ClientHello", REQUEST_COLOR)

        step("Step 2: Server chooses a cipher suite, sends its certificate",
             server, client, "ServerHello + Cert", RESPONSE_COLOR)

        step("Step 3: Client verifies the certificate, sends key material",
             client, server, "Key Exchange", REQUEST_COLOR)

        # Both sides now derive the same session key — close the padlock
        closing_caption = step_caption("Both sides derive a shared session key")
        closing_caption.next_to(title, DOWN, buff=0.3)
        self.play(Write(closing_caption))
        closed_lock = Lock("", locked=True).scale(0.7).move_to(lock.get_center())
        self.play(Transform(lock, closed_lock), lock.animate.set_color(SECURE_COLOR))
        self.play(FadeOut(closing_caption))

        step("Step 4: Application data now flows encrypted",
             client, server, "Encrypted HTTP GET", SECURE_COLOR)
        step("Server responds — still encrypted",
             server, client, "Encrypted 200 OK", SECURE_COLOR)

        note = Text(
            "An eavesdropper on the link sees only ciphertext, not the request/response content.",
            font_size=20, color=LABEL_COLOR,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(2)


class TLSDowngradeWarning(Scene):
    """Optional companion scene: what it looks like when a connection is
    NOT secured (e.g. plain HTTP) — useful for a side-by-side comparison
    slide with TLSHandshake above."""

    def construct(self):
        title = Text("Without TLS", font_size=40, color=ERROR_COLOR).to_edge(UP, buff=0.3)
        self.play(Write(title))

        client = Host("Client").to_edge(LEFT, buff=1.8)
        server = Server("Server").to_edge(RIGHT, buff=1.8)
        link = connect(client, server, color=ERROR_COLOR)
        self.play(FadeIn(client), FadeIn(server), Create(link))

        open_lock = Lock("", locked=False).scale(0.7).move_to(link.get_center() + UP * 1.3)
        open_lock.set_color(ERROR_COLOR)
        self.play(FadeIn(open_lock))

        caption = step_caption("Plain-text HTTP — anyone on the path can read this")
        caption.next_to(title, DOWN, buff=0.3)
        self.play(Write(caption))
        self.play(*send_packet(client, server, "GET /login?pwd=1234", color=ERROR_COLOR))
        self.wait(1.5)
