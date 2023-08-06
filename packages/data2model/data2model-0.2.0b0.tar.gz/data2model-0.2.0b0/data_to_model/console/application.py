"""
# Usage:

data2model -if data.csv -of data.py
"""
import asyncio  # noqa

from pathlib import Path

import asyncclick as click

from data_to_model import ModelGenerator


@click.command()
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
async def model_generator(input_file: str, output_file: str, csv_delimiter: str):
    input_path = Path(input_file)
    output_path = Path(output_file)

    mg = ModelGenerator(input_path, csv_delimiter=csv_delimiter)
    model = await mg.get_model()
    await model.save(output_path)


def main():
    model_generator(_anyio_backend="asyncio")


if __name__ == "__main__":
    main()
