from pathlib import Path

import pandas as pd

from app.ai.parsers.base import BaseParser


class TabularParser(BaseParser):
    """Parser for CSV and XLSX files."""

    def parse(self, file_path: Path) -> str:
        """Extract tabular data and return it as text."""

        suffix = file_path.suffix.lower()

        if suffix == ".csv":
            dataframe = pd.read_csv(file_path)

        elif suffix == ".xlsx":
            dataframe = pd.read_excel(file_path)

        else:
            raise ValueError(
                f"Unsupported tabular file type: {suffix}"
            )

        return dataframe.to_csv(
            index=False
        )