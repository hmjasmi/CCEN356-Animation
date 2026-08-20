"""
packet_delays.py
=================
Kurose & Ross §1.4 — "Delay, Loss, and Throughput in Packet-Switched
Networks": nodal processing delay, queueing delay, transmission delay,
and propagation delay.

Physical intuition encoded here:
  1. Processing delay  — packet arrives, router briefly "inspects" it.
  2. Queueing delay    — packet waits in a buffer because the outgoing
                          link is busy with other packets.
  3. Transmission delay (L/R) — the packet's leading edge stays anchored
                          while its trailing edge stretches out onto the
                          wire ("uncoiling a rope").
  4. Propagation delay (d/s)  — once fully on the wire, the whole packet
                          slides at signal speed to the next router.

A synchronized delay-breakdown timeline bar under the diagram fills in
color-coded segments in real time as each phase happens above.

Render:
    manim -pql packet_delays.py PacketDelays
"""

from manim import *
from shared.network_components import (
    Router, connect, REQUEST_COLOR, RESPONSE_COLOR, RETRANSMIT_COLOR,
    SECURE_COLOR, LABEL_COLOR,
)

PROCESSING_COLOR = SECURE_COLOR
QUEUEING_COLOR = RETRANSMIT_COLOR
TRANSMISSION_COLOR = REQUEST_COLOR
PROPAGATION_COLOR = RESPONSE_COLOR


class PacketDelays(Scene):
    def construct(self):
        title = Text("The Four Delays", font_size=40, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title))

        router_a = Router("Router A").move_to([-4, 0.5, 0])
        router_b = Router("Router B").move_to([2, 0.5, 0])
        link = connect(router_a, router_b)
        self.play(FadeIn(router_a), FadeIn(router_b), Create(link))

        # Timeline bar showing the four phases filling in, left to right
        bar_bg = Rectangle(width=10, height=0.5, color=GRAY, stroke_width=1).move_to([-1, -2.5, 0])
        bar_label = Text("Delay breakdown", font_size=20, color=LABEL_COLOR).next_to(bar_bg, UP, buff=0.15)
        self.play(Create(bar_bg), Write(bar_label))

        segments = [
            ("Processing", PROCESSING_COLOR, 1.5),
            ("Queueing", QUEUEING_COLOR, 2.0),
            ("Transmission", TRANSMISSION_COLOR, 3.0),
            ("Propagation", PROPAGATION_COLOR, 3.5),
        ]
        total_width = 10
        total_weight = sum(w for _, _, w in segments)
        x = bar_bg.get_left()[0]

        # 1. Processing delay — brief pulse at the router
        packet = RoundedRectangle(corner_radius=0.05, width=0.6, height=0.3,
                                   fill_color=TRANSMISSION_COLOR, fill_opacity=1, stroke_width=0)
        packet.move_to(router_a.icon.get_right() + RIGHT * 0.4)
        self.play(FadeIn(packet))
        self.play(Indicate(packet, color=PROCESSING_COLOR, scale_factor=1.3), run_time=0.8)
        seg_w = total_width * segments[0][2] / total_weight
        seg = Rectangle(width=seg_w, height=0.5, fill_color=PROCESSING_COLOR, fill_opacity=0.8,
                         stroke_width=0).move_to([x + seg_w / 2, -2.5, 0])
        self.play(GrowFromEdge(seg, LEFT), run_time=0.8)
        x += seg_w

        # 2. Queueing delay — packet waits (shown as a brief pause with a second packet arriving)
        packet2 = RoundedRectangle(corner_radius=0.05, width=0.6, height=0.3,
                                    fill_color=TRANSMISSION_COLOR, fill_opacity=0.6, stroke_width=0)
        packet2.move_to(packet.get_center() + UP * 0.5)
        self.play(FadeIn(packet2))
        self.wait(0.6)
        seg_w = total_width * segments[1][2] / total_weight
        seg = Rectangle(width=seg_w, height=0.5, fill_color=QUEUEING_COLOR, fill_opacity=0.8,
                         stroke_width=0).move_to([x + seg_w / 2, -2.5, 0])
        self.play(GrowFromEdge(seg, LEFT), FadeOut(packet2), run_time=0.8)
        x += seg_w

        # 3. Transmission delay — packet stretches onto the wire (leading edge anchored)
        stretched = Rectangle(width=2.5, height=0.3, fill_color=TRANSMISSION_COLOR,
                               fill_opacity=1, stroke_width=0)
        stretched.move_to(packet.get_center() + RIGHT * 1.25)
        self.play(Transform(packet, stretched), run_time=1.2)
        seg_w = total_width * segments[2][2] / total_weight
        seg = Rectangle(width=seg_w, height=0.5, fill_color=TRANSMISSION_COLOR, fill_opacity=0.8,
                         stroke_width=0).move_to([x + seg_w / 2, -2.5, 0])
        self.play(GrowFromEdge(seg, LEFT), run_time=1.2)
        x += seg_w

        # 4. Propagation delay — the fully-formed packet slides to Router B
        self.play(packet.animate.move_to(router_b.icon.get_left() + LEFT * 0.4), run_time=1.5)
        seg_w = total_width * segments[3][2] / total_weight
        seg = Rectangle(width=seg_w, height=0.5, fill_color=PROPAGATION_COLOR, fill_opacity=0.8,
                         stroke_width=0).move_to([x + seg_w / 2, -2.5, 0])
        self.play(GrowFromEdge(seg, LEFT), FadeOut(packet), run_time=1.5)

        legend = VGroup(*[
            VGroup(
                Square(side_length=0.2, fill_color=c, fill_opacity=1, stroke_width=0),
                Text(name, font_size=18, color=LABEL_COLOR),
            ).arrange(RIGHT, buff=0.1)
            for name, c, _ in segments
        ]).arrange(RIGHT, buff=0.5).next_to(bar_bg, DOWN, buff=0.4)
        self.play(FadeIn(legend))

        self.wait(2)
