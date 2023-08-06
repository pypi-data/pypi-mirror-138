"""Main entrypoint logic"""

import argparse
import logging
import os
from renamerename.handlers.handlers import FileListHandler
from renamerename.executor.executor import RenameExecutor, DuplicateFilenamesError
from renamerename import __version__

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(description='Bulk renaming of files made easy.', usage="renamerename [options]")
    parser.add_argument("--dir", type=str,
                        help="directory whose filenames are processed", required=False, default=".", metavar="directory")
    parser.add_argument("--only-output-results", "-o", action="store_true",
                        help="only show renaming results without execution", required=False)
    parser.add_argument("--filter", "-f", type=str,
                        help="filter the directory contents according to Unix patterns", required=False, default=None)
    parser.add_argument("--prefix", "-p", type=str,
                        help="add a prefix to filtered filenames", required=False, default=None)
    parser.add_argument("--suffix", "-s", type=str,
                        help="add a suffix to filtered filenames", required=False, default=None)
    parser.add_argument("--change-extension", "-e", type=str,
                        help="change the extension of the filtered filenames", required=False, default=None)
    parser.add_argument("--add-numbering", "-n", type=str,
                        help="change filtered filenames to same name suffixed with increasing numbers", required=False, default=None)
    parser.add_argument("--save-renaming", "-sr", action="store_true",
                        help="create JSON file containing all files renamed", required=False)
    from_file_group = parser.add_mutually_exclusive_group()
    from_file_group.add_argument("--from-json", type=str,
                                 help="rename set of files as described from JSON file", required=False, metavar="JSON file path")
    from_file_group.add_argument("--undo-from-json", type=str,
                                 help="undo renaming of set of files based on saved renaming specification",
                                 required=False, metavar="JSON file path")
    parser.add_argument("--version", action="version", version=f"RenameRename {__version__}")
    return parser.parse_args(*args, **kwargs)


def run(args=None):
    """Main entrypoint script"""

    if not args:
        args = parse_args()

    assert os.path.isdir(args.dir), "Given directory is not a valid directory."

    # Get all (non-hidden) files in a directory:
    names = [name for name in os.listdir(args.dir)
             if os.path.isfile(os.path.join(args.dir, name)) and not name.startswith(".")]

    executor = RenameExecutor(args.dir, save_renaming=args.save_renaming)

    # If actions are specified via file
    if args.from_json or args.undo_from_json:
        try:
            undo = True if args.undo_from_json else False
            filepath = args.undo_from_json if undo else args.from_json
            if undo:
                logging.info("Undo-ing renaming")
            else:
                logging.info("Renaming based on file specification")

            logging.info(f"Loading renaming specifications from the file {filepath}")
            executor.execute_from_file(names, filepath, undo=undo)
            logging.info(f"Renamed the following:\n{executor.actual_transformation}")
            n = len(executor.actual_transformation)
            logging.info(f"Successfully renamed {n}/{n} filtered files")
        except (FileExistsError, FileNotFoundError, DuplicateFilenamesError) as e:
            logging.warning(f"Renamed the following files:\n{executor.actual_transformation}")
            logging.error(e)
            return 2

        return 0

    file_list_handler = FileListHandler(names)
    file_list_handler.filter_names(filter=args.filter)

    logging.info(f"Filtered files ({len(file_list_handler.filenames)} matching):\n{file_list_handler.filenames}")

    # Only print out filtered files if no action is requested
    if not any([args.prefix, args.suffix, args.change_extension, args.add_numbering]):
        return 1

    if args.prefix:
        file_list_handler.add_prefix(args.prefix)
    if args.suffix:
        file_list_handler.add_suffix(args.suffix)
    if args.change_extension:
        file_list_handler.change_extension(args.change_extension)
    if args.add_numbering:
        file_list_handler.add_numbering(args.add_numbering)

    if args.only_output_results:
        # Display output of actions without actually renaming/executing
        executor.display_output(file_list_handler.names, file_list_handler.filetransformations)
    else:
        try:
            executor.execute(file_list_handler.names, file_list_handler.filetransformations)
            logging.info(f"Renamed the following:\n{executor.actual_transformation}")
            n = len(executor.actual_transformation)
            logging.info(f"Successfully renamed {n}/{n} filtered files")
        except (FileExistsError, FileNotFoundError) as e:
            logging.warning(f"{len(executor.actual_transformation)}/{len(file_list_handler.filetransformations)} were renamed")
            logging.warning(f"Renamed the following files:\n{executor.actual_transformation}")
            logging.error(e)
            return 2

    return 0
