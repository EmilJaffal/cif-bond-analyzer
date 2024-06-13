import os
import json
import time
import click
from click import echo
from util import prompt, folder
from preprocess import format
from postprocess.system import (
    system_util,
    system_excel,
    system_figure,
    system_handler,
    system_color,
)
from run import site


def run_system_analysis(script_path):
    prompt.prompt_system_analysis_intro()

    # Display folders containing up to 3 unique elements per folder
    dir_paths = folder.choose_binary_ternary_dir(script_path)

    for idx, dir_path in enumerate(dir_paths, start=1):
        prompt.echo_folder_progress(idx, dir_path, len(dir_paths))
        process_system_analysis_by_folder(dir_path)


def process_system_analysis_by_folder(dir_path):
    format.preprocess_move_files_based_on_format_error(dir_path)
    file_path_list = folder.get_file_path_list(dir_path)

    folder_name = os.path.basename(dir_path)

    json_file_path = os.path.join(
        dir_path, "output", f"{folder_name}_site_pairs.json"
    )
    updated_json_file_path = (
        f"{dir_path}/output/updated_{folder_name}_site_pairs.json"
    )

    overall_start_time = time.perf_counter()
    (
        global_site_pair_dict,
        global_element_pair_dict,
        log_list,
    ) = site.get_bond_data(file_path_list)

    site.save_outputs(
        global_site_pair_dict,
        global_element_pair_dict,
        dir_path,
        file_path_list,
        log_list,
        overall_start_time,
    )

    # Read the JSON file
    with open(json_file_path, "r") as file:
        bond_data = json.load(file)

    """
    Step 1. Update JSON with formula and structural info
    """

    (
        updated_data,
        _,
        unique_structure_types,
        unique_formulas,
    ) = system_util.parse_data_from_json_and_file(bond_data, dir_path)

    system_util.write_json_data(updated_json_file_path, updated_data)

    output_dir = folder.create_folder_under_output_dir(
        dir_path, "system_analysis"
    )

    """
    Step 2. Build dict containing bond/formula/file info per structure
    """

    possible_bond_pairs = system_util.generate_unique_pairs_from_formulas(
        updated_json_file_path
    )

    structure_dict = system_handler.get_structure_dict(
        unique_structure_types,
        possible_bond_pairs,
        updated_json_file_path,
    )

    """
    Step 3. Generate Excel file
    """
    prompt.print_dict_in_json(structure_dict)

    # Save Structure Analysis and Overview Excel
    system_excel.save_structure_analysis_excel(structure_dict, output_dir)
    system_excel.save_bond_overview_excel(
        structure_dict, possible_bond_pairs, output_dir
    )
    """
    Step 4. Generate hexagonal figures and color maps
    """
    # prompt.print_dict_in_json(structure_dict)

    # Check whether binary or ternary
    is_single_binary = system_util.get_is_single_binary(updated_json_file_path)

    is_double_binary = system_util.get_is_double_binary(updated_json_file_path)

    is_ternary = system_util.get_is_ternary(updated_json_file_path)

    is_binary_ternary_combined = system_util.get_is_binary_ternary_combined(
        updated_json_file_path
    )

    # Draw individual hexagon
    system_figure.draw_hexagon_for_individual_figure(
        structure_dict,
        unique_structure_types,
        output_dir,
        possible_bond_pairs,
    )
    if is_ternary or is_binary_ternary_combined:
        system_figure.draw_ternary_figure(
            structure_dict,
            unique_structure_types,
            unique_formulas,
            output_dir,
            is_binary_ternary_combined,
        )

        # system_color.plot_ternary_color_map(
        #     unique_formulas,
        #     structure_dict,
        #     possible_bond_pairs,
        #     output_dir,
        # )

    # Plot binary
    if is_single_binary or is_double_binary:
        system_figure.draw_binary_figure(
            unique_formulas,
            structure_dict,
            possible_bond_pairs,
            output_dir,
            is_single_binary,
        )
