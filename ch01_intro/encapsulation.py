"""
demo_encapsulation.py
======================
Animates "Services, Layering and Encapsulation": a message is wrapped with
a header at each layer going down the source's protocol stack
(encapsulation), sent across the network, then unwrapped one header at a
time going up the destination's stack (decapsulation).

Render:
    manim -pql demo_encapsulation.py Encapsulation
"""

from manim import *
from shared.network_components import (
    Host, Server, layer_stack, header_box, message_box, build_packet,
    place_packet, step_caption,
    HT_COLOR, HN_COLOR, HL_COLOR,
)


class Encapsulation(Scene):
    def construct(self):
        title = Text("Services, Layering and Encapsulation", font_size=34).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Fixed vertical slot for the step caption, between the title and
        # the top of the protocol stacks.
        caption_y = title.get_bottom()[1] - 0.6

        # --- Build both protocol stacks -----------------------------------
        left_stack = layer_stack().scale(0.8)
        left_stack.to_edge(LEFT, buff=0.6)
        right_stack = layer_stack().scale(0.8)
        right_stack.to_edge(RIGHT, buff=0.6)

        # Place stacks just below the caption slot, and low enough that the
        # bottom ("physical") row plus the host/server icon stay on screen.
        stack_top_y = caption_y - 0.7
        stack_center_y = stack_top_y - left_stack.height / 2
        left_stack.set_y(stack_center_y)
        right_stack.set_y(stack_center_y)

        source_icon = Host("source").scale(0.7).next_to(left_stack, DOWN, buff=0.35)
        dest_icon = Server("destination").scale(0.7).next_to(right_stack, DOWN, buff=0.35)

        self.play(
            FadeIn(left_stack), FadeIn(right_stack),
            FadeIn(source_icon), FadeIn(dest_icon),
        )

        # Row y-coordinates: index 0=application ... 4=physical
        left_y = [left_stack[i].get_center()[1] for i in range(5)]
        right_y = [right_stack[i].get_center()[1] for i in range(5)]
        left_anchor_x = left_stack.get_right()[0] + 1.6
        right_anchor_x = right_stack.get_left()[0] - 0.3

        def target_center(packet, y, right_x):
            """Center point that puts `packet`'s right edge at right_x and
            vertical center at y, without mutating the packet (for use in
            .animate.move_to(), unlike place_packet which moves immediately)."""
            half_w = packet.get_width() / 2
            return [right_x - half_w, y, 0]

        # --- ENCAPSULATION (down the source stack) -------------------------
        caption = step_caption("Application creates the message", y=caption_y)
        self.play(Write(caption))
        packet = place_packet(message_box(), left_y[0], left_anchor_x)
        self.play(FadeIn(packet))
        self.wait(0.3)

        steps_down = [
            (1, "Transport adds header Hₜ  →  segment",
             build_packet(header_box("t", HT_COLOR), message_box())),
            (2, "Network adds header Hₙ  →  datagram",
             build_packet(header_box("n", HN_COLOR), header_box("t", HT_COLOR), message_box())),
            (3, "Link adds header Hₗ  →  frame",
             build_packet(header_box("l", HL_COLOR), header_box("n", HN_COLOR),
                           header_box("t", HT_COLOR), message_box())),
        ]
        for row, text, new_packet in steps_down:
            new_caption = step_caption(text, y=caption_y)
            place_packet(new_packet, left_y[row], left_anchor_x)
            self.play(FadeOut(caption), FadeIn(new_caption))
            self.play(ReplacementTransform(packet, new_packet))
            packet, caption = new_packet, new_caption
            self.wait(0.3)

        # --- TRANSMISSION across the physical medium ------------------------
        transmit_caption = step_caption("Physical layer transmits the frame as bits", y=caption_y)
        self.play(FadeOut(caption), FadeIn(transmit_caption))
        self.play(packet.animate.move_to([left_stack.get_center()[0], left_y[4], 0]))
        self.play(packet.animate.move_to([right_stack.get_center()[0], left_y[4], 0]))
        self.play(packet.animate.move_to(target_center(packet, right_y[4], right_anchor_x)))
        self.wait(0.3)

        receive_caption = step_caption("Physical layer at destination receives the frame", y=caption_y)
        self.play(FadeOut(transmit_caption), FadeIn(receive_caption))
        caption = receive_caption
        self.wait(0.3)

        # --- DECAPSULATION (up the destination stack) -----------------------
        # Each layer receives the packet still carrying its own header, then
        # strips that header and passes the packet up to the layer above —
        # so the packet without H_l lives at the network row, without H_n at
        # the transport row, and without H_t at the application row.
        strip_steps = [
            (3, "Link layer strips Hₗ",
             build_packet(header_box("n", HN_COLOR), header_box("t", HT_COLOR), message_box())),
            (2, "Network layer strips Hₙ",
             build_packet(header_box("t", HT_COLOR), message_box())),
            (1, "Transport layer strips Hₜ",
             message_box()),
        ]
        for row, text, stripped_packet in strip_steps:
            # Packet arrives intact at this layer's row.
            self.play(packet.animate.move_to(target_center(packet, right_y[row], right_anchor_x)))
            # This layer strips its header and passes the packet up.
            new_caption = step_caption(text, y=caption_y)
            place_packet(stripped_packet, right_y[row - 1], right_anchor_x)
            self.play(FadeOut(caption), FadeIn(new_caption))
            self.play(ReplacementTransform(packet, stripped_packet))
            packet, caption = stripped_packet, new_caption
            self.wait(0.3)

        final_caption = step_caption("Application receives the original message M", y=caption_y)
        place_packet(packet, right_y[0], right_anchor_x)
        self.play(FadeOut(caption), FadeIn(final_caption))
        self.play(Indicate(packet, color=YELLOW), Indicate(dest_icon, color=YELLOW))
        self.wait(1)