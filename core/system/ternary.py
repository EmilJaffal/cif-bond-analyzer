import numpy as np
import matplotlib.pyplot as plt
from core.system import ternary_handler, hexagon
from core.util import string_parser, formula_parser
from core.system.figure_util import (
    shift_points_xy,
)


def get_point_in_triangle_from_ternary_index(
    v0, v1, v2, R_norm_index, M_norm_index
):
    # R_norm_index corresponds to v2
    # M_norm_index corresponds to v1
    R = R_norm_index
    M = M_norm_index

    # Calculate the third weight for v0
    X = 1 - R - M

    # Compute the position using the barycentric coordinates
    point_position = R * v0 + M * v1 + X * v2
    return point_position


def generate_traingle_vertex_points():
    """
    Generate 3 x,y positions of traingle vertices
    """
    v0 = np.array([0, 0])
    v1 = np.array([1, 0])
    v2 = np.array([0.5, np.sqrt(3) / 2])
    return v0, v1, v2


def draw_ternary_frame(v0, v1, v2):
    """
    Draw traingle vertices.
    """
    # Triangle vertices
    # Plotting the enhanced triangle
    plt.figure(figsize=(8, 6))
    triangle = plt.Polygon(
        [v0, v1, v2],
        edgecolor="k",
        facecolor="none",
        zorder=3,
    )
    plt.gca().add_patch(triangle)
    # Set new plot limits here
    plt.xlim(-0.3, 1.3)  # Extend x-axis limits
    plt.ylim(-0.4, 1.0)  # Extend y-axis limits

    plt.tight_layout(pad=0.2)
    plt.gca().set_aspect("equal", adjustable="box")


def draw_extra_frame_for_binary_tags(v0, v1, v2, unique_formulas, RMX):
    """
    Draw extra edges on the traingle with tags found on binary compounds
    """
    print("Print unique formulas", unique_formulas)
    # First from the structure dict, we get all unique formulas
    formula_tag_tuples = string_parser.parse_formulas_with_underscore(
        unique_formulas
    )

    tags_count = formula_parser.count_formula_with_tags_in_ternary(
        formula_tag_tuples, RMX
    )
    # Draw edges of the traingle
    # The following is the not refactored logic at the moment for flexibility

    edges = {
        (tuple(v0), tuple(v1)): "RM",
        (tuple(v0), tuple(v2)): "RX",
        (tuple(v1), tuple(v2)): "MX",
    }

    print(tags_count)

    extra_edge_line_width = 0.5
    for (start, end), key in edges.items():
        start_vertex = np.array(start)
        end_vertex = np.array(end)
        x_shift, y_shift = 0, 0

        # Handle 'lt' condition
        if tags_count.get(f"{key}_lt", 0):
            # Smaller shifts
            shift_amount = 0.1
            if key == "RM":
                y_shift = -shift_amount
            elif key == "MX":
                x_shift = shift_amount
            elif key == "RX":
                x_shift = -shift_amount
            new_p1 = shift_points_xy(start_vertex, x_shift, y_shift)
            new_p2 = shift_points_xy(end_vertex, x_shift, y_shift)
            plt.plot(
                [new_p1[0], new_p2[0]],
                [new_p1[1], new_p2[1]],
                "k--",
                zorder=2,
                lw=extra_edge_line_width,
            )

        # Handle 'ht' condition
        if tags_count.get(f"{key}_ht", 0):
            # Custom shifts based on the key
            shift_amount = 0.2
            if key == "RM":
                y_shift = -shift_amount
            elif key == "MX":
                x_shift = shift_amount
            elif key == "RX":
                x_shift = -shift_amount
            new_p1 = shift_points_xy(start_vertex, x_shift, y_shift)
            new_p2 = shift_points_xy(end_vertex, x_shift, y_shift)
            plt.plot(
                [new_p1[0], new_p2[0]],
                [new_p1[1], new_p2[1]],
                "k--",
                zorder=2,
                lw=extra_edge_line_width,
            )

        # Assume handling 'others' or any condition needing a larger shift
        if tags_count.get(f"{key}_others", 0):
            # Larger shifts, example with a hypothetical 'others' condition
            shift_amount = 0.3
            if key == "RM":
                y_shift = -shift_amount
            elif key == "MX":
                x_shift = shift_amount
            elif key == "RX":
                x_shift = -shift_amount
            new_p1 = shift_points_xy(start_vertex, x_shift, y_shift)
            new_p2 = shift_points_xy(end_vertex, x_shift, y_shift)
            plt.plot(
                [new_p1[0], new_p2[0]],
                [new_p1[1], new_p2[1]],
                "k--",
                zorder=2,
                lw=extra_edge_line_width,
            )


def add_vertex_labels(v0, v1, v2, RMX):
    # Labeling the vertices
    plt.text(
        v0[0] - 0.02,
        v0[1] - 0.02,
        RMX[0],
        fontsize=14,
        ha="right",
        va="top",
    )
    plt.text(
        v1[0] + 0.02,
        v1[1] - 0.02,
        RMX[1],
        fontsize=14,
        ha="left",
        va="top",
    )
    plt.text(
        v2[0],
        v2[1] + 0.02,
        RMX[2],
        fontsize=14,
        ha="center",
        va="bottom",
    )


def draw_filled_edges(v0, v1, v2, fraction=0.02, alpha=1):
    # Calculate points along the edges at the given fraction of their lengths
    p0_blue = [
        (1 - fraction) * v0[0] + (1 - fraction) * v1[0],
        (1 - fraction) * v0[1] + fraction * v1[1],
    ]

    p0_red = [
        (1 - fraction) * v0[0] + fraction * v1[0],
        (1 - fraction) * v0[1] + fraction * v1[1],
    ]

    p1_red = [
        (1 - fraction) * v0[0] + fraction * v2[0],
        (1 - fraction) * v0[1] + fraction * v2[1],
    ]

    p2_blue = [
        (1 - fraction) * v1[0] + fraction * v2[0],
        (1 - fraction) * v1[1] + fraction * v2[1],
    ]

    p1_green = [
        (1 - fraction) * v2[0] + fraction * v0[0],  # x coordinate
        (1 - fraction) * v2[1] + fraction * v0[1],  # y coordinate
    ]
    p2_green = [
        (1 - fraction) * v2[0] + fraction * v1[0],  # x coordinate
        (1 - fraction) * v2[1] + fraction * v1[1],  # y coordinate
    ]

    # Create filled polygons along the edges
    filled_edge1 = plt.Polygon(
        [v0, p0_red, p1_red],
        closed=True,
        color="blue",
        alpha=alpha,
    )
    filled_edge2 = plt.Polygon(
        [v1, p0_blue, p2_blue],
        closed=True,
        color="green",
        alpha=alpha,
    )
    filled_edge3 = plt.Polygon(
        [v2, p1_green, p2_green],
        closed=True,
        color="red",
        alpha=alpha,
    )

    plt.gca().add_patch(filled_edge1)
    plt.gca().add_patch(filled_edge2)
    plt.gca().add_patch(filled_edge3)


def draw_triangular_grid(v0, v1, v2, alpha, line_width, n_lines=10):
    # Line parallel to v2v0 (right slant)
    for i in range(1, n_lines):
        t = i / n_lines

        # Compute intermediate points on the edges
        p0 = (1 - t) * v0 + t * v1  # from v0 to v1
        p1 = (1 - t) * v0 + t * v2  # from v0 to v2
        p2 = (1 - t) * v1 + t * v2  # from v1 to v2
        p3 = (t) * v1 + (1 - t) * v2  # from v1 to v2

        plt.plot(
            [p0[0], p3[0]],
            [p0[1], p3[1]],
            "k",
            alpha=alpha,
            lw=line_width,
        )
        # Line parallel to v1v2 (left slant)
        plt.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            "k",
            alpha=alpha,
            lw=line_width,
        )
        # Line parallel to v0v1 (base)
        plt.plot(
            [p0[0], p1[0]],
            [p0[1], p1[1]],
            "k",
            alpha=alpha,
            lw=line_width,
        )


def draw_legend(bond_pairs_ordered, x_position):
    legend_center_point = (0 + x_position, 0.8)
    legend_bond_label_font_size = 10
    legend_radius = 0.06

    hexagon.draw_single_hexagon_and_lines_per_center_point(
        legend_center_point,
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        radius=legend_radius,
        hex_inner_color="#D3D3D3",
        hex_outer_color="black",
        hex_inner_line_width=0.5,
        hex_outer_line_width=0.5,
        color_line_width=3,
        is_for_individual_hexagon=False,
    )
    plt.scatter(
        legend_center_point[0],
        legend_center_point[1],
        color="black",
        s=14,
        zorder=5,
    )
    # Add legend labels
    label_offset = 0.05

    # Get the points for label positioning using the increased radius
    x_label_pts, y_label_pts = hexagon.get_hexagon_points(
        legend_center_point, legend_radius + label_offset
    )
    for i, (x, y, label) in enumerate(
        zip(x_label_pts, y_label_pts, bond_pairs_ordered)
    ):
        plt.text(
            x,
            y,
            label,
            fontsize=legend_bond_label_font_size,
            ha="center",  # Horizontal alignment
            va="center",  # Vertical alignment
        )

    # Add legend description
    legend_y_offset = 0.2
    plt.text(
        legend_center_point[0],
        legend_center_point[1] - legend_y_offset,
        "Bar length\nrepresents bond fraction",
        horizontalalignment="center",
        fontsize=8,
    )


def draw_center_dot_formula(center_pt, formula):
    # Config for hexagon
    center_dot_radius = 8
    formula_offset = -0.07
    formula_font_size = 9
    formula_formatted = formula_parser.get_subscripted_string(formula)

    plt.text(
        center_pt[0],
        center_pt[1] + formula_offset,
        f"{formula_formatted}",
        fontsize=formula_font_size,
        ha="center",
    )

    # Add the "center dot" in each hexagon
    plt.scatter(
        center_pt[0],
        center_pt[1],
        color="black",
        s=center_dot_radius,
        zorder=6,
    )


def draw_hexagon_for_ternary_formula(
    vertices,
    parsed_normalized_formula,
    bond_fractions,
    bnod_fractions_CN,
    is_CN_used,
):
    R_norm_index = parsed_normalized_formula[0][1]
    M_norm_index = parsed_normalized_formula[1][1]
    v0, v1, v2 = vertices

    center_pt = get_point_in_triangle_from_ternary_index(
        v0,
        v1,
        v2,
        float(R_norm_index),
        float(M_norm_index),
    )

    if is_CN_used:
        hexagon.draw_single_hexagon_and_lines_per_center_point(
            center_pt,
            bnod_fractions_CN,
        )
    else:
        hexagon.draw_single_hexagon_and_lines_per_center_point(
            center_pt,
            bond_fractions,
        )
    return center_pt


def draw_hexagon_for_binary_formula(
    vertices,
    parsed_normalized_formula,
    bond_fractions,
    bnod_fractions_CN,
    RMX,
    tag,
    is_CN_used,
):
    center_pt = None
    R, M, X = RMX
    A_norm_index = float(parsed_normalized_formula[0][1])
    B_norm_index = float(parsed_normalized_formula[1][1])
    A_label = parsed_normalized_formula[0][0]
    B_label = parsed_normalized_formula[1][0]
    v0, v1, v2 = vertices

    if A_label == R and B_label == M:
        # ErCo
        center_pt = get_point_in_triangle_from_ternary_index(
            v0,
            v1,
            v2,
            A_norm_index,
            B_norm_index,
        )
        if tag == "hex" or tag == "rt":
            center_pt = center_pt
        elif tag == "lt":
            center_pt = shift_points_xy(center_pt, 0.0, -0.1)
        elif tag == "ht":
            center_pt = shift_points_xy(center_pt, 0.0, -0.2)
        elif tag is not None:
            center_pt = shift_points_xy(center_pt, 0.0, -0.1)

        if is_CN_used:
            hexagon.draw_single_hexagon_and_lines_per_center_point(
                center_pt,
                bnod_fractions_CN,
            )
        else:
            hexagon.draw_single_hexagon_and_lines_per_center_point(
                center_pt,
                bond_fractions,
            )

    if A_label == R and B_label == X:
        center_pt = get_point_in_triangle_from_ternary_index(
            v0,
            v1,
            v2,
            A_norm_index,
            0.0,
        )
        if tag == "hex" or tag == "rt":
            center_pt = center_pt
        elif tag == "lt":
            center_pt = shift_points_xy(center_pt, -0.1, 0.0)
        elif tag == "ht":
            center_pt = shift_points_xy(center_pt, -0.2, 0.0)
        elif tag is not None:
            center_pt = shift_points_xy(center_pt, -0.1, 0.0)

        if is_CN_used:
            hexagon.draw_single_hexagon_and_lines_per_center_point(
                center_pt,
                bnod_fractions_CN,
            )
        else:
            hexagon.draw_single_hexagon_and_lines_per_center_point(
                center_pt,
                bond_fractions,
            )

    if A_label == M and B_label == X:
        # CoIn2
        center_pt = get_point_in_triangle_from_ternary_index(
            v0,
            v1,
            v2,
            0,
            (1 - B_norm_index),
        )
        if tag == "hex" or tag == "rt":
            center_pt = center_pt
        elif tag == "lt":
            center_pt = shift_points_xy(center_pt, 0.1, 0.0)
        elif tag == "ht":
            center_pt = shift_points_xy(center_pt, 0.2, 0.0)
        elif tag is not None:
            center_pt = shift_points_xy(center_pt, 0.1, 0.0)

        if is_CN_used:
            hexagon.draw_single_hexagon_and_lines_per_center_point(
                center_pt,
                bnod_fractions_CN,
            )
        else:
            hexagon.draw_single_hexagon_and_lines_per_center_point(
                center_pt,
                bond_fractions,
            )
    return center_pt
