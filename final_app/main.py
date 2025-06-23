import os
import sys
import time

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
from notion_utils.relate_databases_to_one.relate_databases_add_new_target_database import *
from notion_utils.relate_databases_to_one.relate_databases_format import *
from notion_utils.relate_databases_to_one.relate_databases_to_one_update import *
from notion_utils.log import log_error, log_error_with_traceback, write_log_header
from notion_utils.internet_check import check_internet_connection


def ensure_standard_fields(combination_database_id, target_database_list):
    try:
        start1 = time.time()
        # Update any mismatched relation field names in combination database
        print("Starting relation sync process...")
        sync_relation_names_with_database_titles(combination_database_id)

        print("Adding relation fields...(Make sure all target database titles are unique!)")

        for target_database in target_database_list:
            # Add relation fields if they do not already exist
            try:
                add_new_relate_database_property(target_database, combination_database_id)
            except ValueError as ve:
                log_error("Failed to add new relation property to combination database.", ve)
                continue
            except RuntimeError as re:
                log_error("Failed to add new relation property to combination database.", re)
        log_print_green(f"All relation fields successfully added to database {combination_database_id}")
        end1 = time.time()
        log_print_green(f"Setting runtime：{end1 - start1:.4f} seconds.")
    except Exception as re:
        log_error("Part 1: Ensure standard fields failed.")
        log_error_with_traceback(re)


def sync_relation_field_names(combination_database_id, target_database_list):
    try:
        start2 = time.time()
        # Make sure relation field names match the corresponding database titles
        print("Re-syncing relation names to ensure accuracy...")
        sync_relation_names_with_database_titles(combination_database_id)

        # Validate that each page has at most one valid relation and no duplicate names
        print("Validating combination database structure...")
        check_combination_database_pages_format(combination_database_id)

        # Ensure required fields like Name, Database Address, Created/Edited Time exist
        print("Ensuring required dynamic fields exist...")
        update_standard_database_property(combination_database_id)
        log_print_green("Field check complete. Renamed fields will be preserved and new ones created if needed.")

        # Merge all pages from target databases into the combination database
        print("Updating combination database with all target data...")
        update_all_target_database_to_combi(target_database_list, combination_database_id)
        log_print_green("✅ Merge process complete.")
        end2 = time.time()
        log_print_green(f"Sync runtime：{end2 - start2:.4f} seconds.")
    except Exception as ve:
        log_error("Part 2: Sync relation field names failed.")
        log_error_with_traceback(ve)


def main():
    """
    Main execution flow:
    - Link all target databases to the combination database
    - Validate schema consistency
    - Normalize format
    - Perform page synchronization
    """

    # Retrieve combination database ID and target database IDs
    combination_database_C_id = os.getenv("PHASE_5_COMBINATION_DATABASE_C_ID")

    # Retrieve target database IDs
    target_databases_A_id = os.getenv("PHASE_4_TARGET_DATABASE_A_ID")
    target_databases_B_id = os.getenv("PHASE_4_TARGET_DATABASE_B_ID")
    target_database_list = []
    target_database_list.append(target_databases_A_id)
    target_database_list.append(target_databases_B_id)
    target_database_list.append("205b82c9b09480a79deaec0b8c3a6369")

    # === Part 1: Ensure standard fields ===
    ensure_standard_fields(combination_database_C_id, target_database_list)

    # === Part 2: Sync relation field names ===
    sync_relation_field_names(combination_database_C_id, target_database_list)


if __name__ == "__main__":
    try:
        if not check_internet_connection():
            print("No Internet connection.")
            sys.exit(1)
        write_log_header()
        start = time.time()
        main()
        end = time.time()
        log_print_green(f"Total runtime：{end - start:.4f} seconds.")
    except KeyboardInterrupt:
        log_error("Program terminated by user (KeyboardInterrupt).")
    except Exception as e:
        log_error("Program terminated by pc.")
        log_error_with_traceback(e)
