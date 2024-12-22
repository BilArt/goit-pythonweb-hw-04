import asyncio
import logging
from pathlib import Path
import shutil
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def copy_file(file_path: Path, output_folder: Path):
    try:
        extension = file_path.suffix.lstrip(".").lower() or "unknown"
        target_folder = output_folder / extension

        target_folder.mkdir(parents=True, exist_ok=True)

        target_file_path = target_folder / file_path.name
        shutil.copy2(file_path, target_file_path)
        logger.info(f"Copied: {file_path} -> {target_file_path}")
    except Exception as e:
        logger.error(f"Error copying file {file_path}: {e}")

async def read_folder(source_folder: Path, output_folder: Path):
    try:
        tasks = []
        for item in source_folder.rglob("*"):
            if item.is_file():
                tasks.append(copy_file(item, output_folder))

        await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"Error reading folder {source_folder}: {e}")

if __name__ == "__main__":
    parser = ArgumentParser(description="Sort files by extension asynchronously.")
    parser.add_argument("source", type=str, help="Source folder path.")
    parser.add_argument("output", type=str, help="Output folder path.")

    args = parser.parse_args()

    source_folder = Path(args.source).resolve()
    output_folder = Path(args.output).resolve()

    if not source_folder.exists() or not source_folder.is_dir():
        logger.error(f"Source folder does not exist: {source_folder}")
        exit(1)

    output_folder.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting file sorting: {source_folder} -> {output_folder}")

    asyncio.run(read_folder(source_folder, output_folder))

    logger.info("File sorting completed.")
