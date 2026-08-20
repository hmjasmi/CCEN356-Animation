"""
demo_security.py
==================
Animates three "bad guys" scenarios:
    1. Packet sniffing  — a packet broadcast on a shared medium is copied
       by an eavesdropper (C) even though it's addressed to A
    2. IP spoofing      — C forges the source address on a packet so A
       can't tell it didn't really come from B
    3. DoS / DDoS       — a botnet floods a target with bogus traffic,
       drowning out legitimate requests

Render:
    manim -pql demo_security.py NetworkSecurity
"""

from manim import *
from shared.network_components import (
    Server, Host, Router, Attacker, network_packet, send_packet, step_caption,
    NODE_STROKE, LABEL_COLOR, ERROR_COLOR, RESPONSE_COLOR,
)
import math


class NetworkSecurity(Scene):
    def construct(self):
        title = Text("Bad Guys: Network Security Threats", font_size=32, color=BLUE).to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.caption_y = title.get_bottom()[1] - 0.5

        self.sniffing_scenario()
        self.spoofing_scenario()
        self.dos_scenario()

        self.wait(1)

    def caption(self, text):
        return step_caption(text, y=self.caption_y, font_size=24)

    # -----------------------------------------------------------------------
    def sniffing_scenario(self):
        header = self.caption('packet "sniffing": a shared medium lets C read traffic never addressed to it')
        self.play(Write(header))

        a = Server("A").scale(0.8).move_to([-5.0, 1.0, 0])
        c = Attacker("C").scale(0.8).move_to([1.5, 1.0, 0])
        b = Host("B").scale(0.8).move_to([4.8, -1.0, 0])
        router = Router("").scale(0.8).move_to([-1.5, 0.1, 0])

        bus_y = 0.1
        bus = Line([-5.3, bus_y, 0], [5.1, bus_y, 0], color=NODE_STROKE, stroke_width=2)
        stub_a = Line([-5.0, a.icon.get_bottom()[1], 0], [-5.0, bus_y, 0], color=NODE_STROKE, stroke_width=2)
        stub_c = Line([1.5, c.icon.get_bottom()[1], 0], [1.5, bus_y, 0], color=NODE_STROKE, stroke_width=2)
        stub_b = Line([4.8, bus_y, 0], [4.8, b.icon.get_top()[1], 0], color=NODE_STROKE, stroke_width=2)

        self.play(
            FadeIn(a), FadeIn(c), FadeIn(b), FadeIn(router),
            Create(bus), Create(stub_a), Create(stub_c), Create(stub_b),
        )

        packet = network_packet("B", "A", payload="pwd:••••").scale(0.7)
        packet.move_to([4.8, b.icon.get_top()[1] + 0.3, 0])
        self.play(FadeIn(packet))

        # B -> bus
        self.play(packet.animate.move_to([4.8, bus_y, 0]))
        # along bus to C's position (still addressed to A, just passing by)
        self.play(packet.animate.move_to([1.5, bus_y, 0]))

        # split: original continues toward A: a COPY peels off to C
        copy_caption = self.caption("C's network card reads every packet passing by — even this one")
        self.play(FadeOut(header), FadeIn(copy_caption))
        packet_copy = packet.copy()
        self.play(
            packet.animate.move_to([-5.0, bus_y, 0]),
            packet_copy.animate.move_to(c.icon.get_center()),
        )
        self.play(packet.animate.move_to(a.icon.get_center()))

        # highlight the captured password
        self.play(Circumscribe(packet_copy.payload_cell, color=ERROR_COLOR, time_width=0.6))
        self.wait(0.3)

        self.play(
            FadeOut(copy_caption), FadeOut(a), FadeOut(c), FadeOut(b), FadeOut(router),
            FadeOut(bus), FadeOut(stub_a), FadeOut(stub_c), FadeOut(stub_b),
            FadeOut(packet), FadeOut(packet_copy),
        )

    # -----------------------------------------------------------------------
    def spoofing_scenario(self):
        header = self.caption("IP spoofing: injection of a packet with a false source address")
        self.play(Write(header))

        a = Server("A").scale(0.8).move_to([-5.0, 1.0, 0])
        c = Attacker("C").scale(0.8).move_to([1.5, 1.0, 0])
        b = Host("B").scale(0.8).move_to([4.8, -1.0, 0])
        router = Router("").scale(0.8).move_to([-1.5, 0.1, 0])

        bus_y = 0.1
        bus = Line([-5.3, bus_y, 0], [5.1, bus_y, 0], color=NODE_STROKE, stroke_width=2)
        stub_a = Line([-5.0, a.icon.get_bottom()[1], 0], [-5.0, bus_y, 0], color=NODE_STROKE, stroke_width=2)
        stub_c = Line([1.5, c.icon.get_bottom()[1], 0], [1.5, bus_y, 0], color=NODE_STROKE, stroke_width=2)
        stub_b = Line([4.8, bus_y, 0], [4.8, b.icon.get_top()[1], 0], color=NODE_STROKE, stroke_width=2)

        self.play(
            FadeIn(a), FadeIn(c), FadeIn(b), FadeIn(router),
            Create(bus), Create(stub_a), Create(stub_c), Create(stub_b),
        )

        # C forges a packet with src:B, even though C is really sending it
        forge_caption = self.caption("C writes a false source address into the packet: src:B")
        self.play(FadeOut(header), FadeIn(forge_caption))
        packet = network_packet("B", "A", src_color=ERROR_COLOR).scale(0.7)
        packet.move_to(c.icon.get_center())
        self.play(FadeIn(packet))
        self.play(Circumscribe(packet.src_cell, color=ERROR_COLOR, time_width=0.6))

        deliver_caption = self.caption("A has no way to tell this didn't really come from B")
        self.play(FadeOut(forge_caption), FadeIn(deliver_caption))
        self.play(packet.animate.move_to([1.5, bus_y, 0]))
        self.play(packet.animate.move_to([-5.0, bus_y, 0]))
        self.play(packet.animate.move_to(a.icon.get_center()))
        self.wait(0.3)

        self.play(
            FadeOut(deliver_caption), FadeOut(a), FadeOut(c), FadeOut(b), FadeOut(router),
            FadeOut(bus), FadeOut(stub_a), FadeOut(stub_c), FadeOut(stub_b), FadeOut(packet),
        )

    # -----------------------------------------------------------------------
    def dos_scenario(self):
        header = self.caption("Denial of Service: a botnet floods the target with bogus traffic")
        self.play(Write(header))

        target = Server("target").scale(0.9).move_to([0, -0.3, 0])

        n_ring = 10
        radius = 3.0
        attackers = []
        legit_hosts = []
        legit_indices = {2, 7}
        ring_nodes = []
        for i in range(n_ring):
            angle = 2 * math.pi * i / n_ring
            pos = [radius * math.cos(angle), -0.3 + radius * math.sin(angle) * 0.7, 0]
            if i in legit_indices:
                node = Host("").scale(0.55).move_to(pos)
                legit_hosts.append(node)
            else:
                node = Attacker("").scale(0.55).move_to(pos)
                attackers.append(node)
            ring_nodes.append(node)

        self.play(FadeIn(target), *[FadeIn(n) for n in ring_nodes])
        self.wait(0.2)

        # --- Flood: every compromised host fires at the target, twice -----------
        for _ in range(2):
            anims = []
            for att in attackers:
                anims += send_packet(att, target, "", color=ERROR_COLOR, shape="square", run_time=0.7)
            self.play(*anims)

        # --- Target overloads ------------------------------------------------------
        overload_caption = self.caption("Target's resources are overwhelmed")
        self.play(FadeOut(header), FadeIn(overload_caption))
        self.play(target.icon.animate.set_color(ERROR_COLOR), Flash(target.icon, color=ERROR_COLOR, line_length=0.4))
        overloaded_label = Text("OVERLOADED", font_size=18, color=ERROR_COLOR).next_to(target, DOWN, buff=0.2)
        self.play(Write(overloaded_label))

        # --- A legitimate request gets dropped --------------------------------------
        drop_caption = self.caption("Legitimate traffic can no longer get through")
        self.play(FadeOut(overload_caption), FadeIn(drop_caption))
        legit = legit_hosts[0]
        request = network_packet("user", "target", payload="request", cell_width=0.6, payload_width=0.8, height=0.32, font_size=12).scale(0.7)
        request.move_to(legit.icon.get_center())
        self.play(FadeIn(request))
        midpoint = [(legit.get_center()[0] + target.get_center()[0]) / 2,
                    (legit.get_center()[1] + target.get_center()[1]) / 2, 0]
        self.play(request.animate.move_to(midpoint), run_time=0.8)
        x_mark = Text("✗", font_size=36, color=ERROR_COLOR).move_to(midpoint)
        self.play(FadeIn(x_mark, scale=1.5), FadeOut(request))
        self.wait(0.4)

        self.play(
            FadeOut(drop_caption), FadeOut(x_mark), FadeOut(overloaded_label),
            FadeOut(target), *[FadeOut(n) for n in ring_nodes],
        )
