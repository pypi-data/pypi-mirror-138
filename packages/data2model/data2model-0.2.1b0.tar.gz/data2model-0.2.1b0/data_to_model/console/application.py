"""
# Usage:

data2model -if data.csv -of data.py
"""
import asyncio  # noqa

from functools import wraps
from pathlib import Path

import click

from data_to_model import ModelGenerator


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group(help="Generate models from data files")
def cli():
    pass


@click.command("file", short_help="Generate model from a single file")
@click.option(
    "-if", "--input-file", type=str, required=True, help="Input file, e.g. data.csv"
)
@click.option(
    "-of", "--output-file", type=str, required=True, help="Output file, e.g. data.py"
)
@click.option(
    "--csv-delimiter",
    type=str,
    required=False,
    help="Delimiter in CSV files, default coma(',')",
    default=",",
)
@coro
async def from_file(input_file: str, output_file: str, csv_delimiter: str):
    input_path = Path(input_file)
    output_path = Path(output_file)
    await model_generator(input_path, output_path, csv_delimiter)


@click.command("folder", short_help="Generate models from files from a folder")
@click.option(
    "-if", "--input-folder", type=str, required=True, help="Folder with data files"
)
@click.option("-of", "--output-folder", type=str, required=True, help="Output folder")
@click.option(
    "--csv-delimiter",
    type=str,
    required=False,
    help="Delimiter in CSV files, default coma(',')",
    default=",",
)
@coro
async def from_folder(input_folder: str, output_folder: str, csv_delimiter: str):
    allowed_file_formats = {".csv", ".tsv", ".txt"}
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    input_files = [
        i
        for i in input_path.iterdir()
        if i.is_file() and i.suffix in allowed_file_formats
    ]
    output_files = [output_path.joinpath(f"{i.stem}.py") for i in input_files]

    output_path.mkdir(exist_ok=True, parents=True)

    tasks = [
        model_generator(i, o, csv_delimiter=csv_delimiter)
        for i, o in zip(input_files, output_files)
    ]
    await asyncio.gather(*tasks)


async def model_generator(
    input_path: Path, output_path: Path, csv_delimiter: str = ","
):
    mg = ModelGenerator(input_path, csv_delimiter=csv_delimiter)
    model = await mg.get_model()
    await model.save(output_path)


def main():
    cli.add_command(from_file)
    cli.add_command(from_folder)
    cli()


if __name__ == "__main__":
    main()
