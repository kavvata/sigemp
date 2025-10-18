#!/usr/bin/env python3
"""
Two-level sunburst for pytest-cov XML coverage reports.

Level 1: top-level package (first segment of path)
Level 2: file label, showing subpackage paths as "subpkg/file.py"
"""

import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
import plotly.express as px
import os
import pandas as pd


def parse_pytest_cov_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    data = []

    # Try both structures: <package><class> and <packages><classes> OR <sources><source> with <file>
    files = root.findall(".//class")
    if not files:
        files = root.findall(".//file")

    for f in files:
        filename = f.get("filename")
        if not filename:
            continue

        # Normalize package structure from path (strip extensions and convert / to .)
        parts = filename.replace("\\", "/").split("/")
        if len(parts) == 1:
            top = "root"
            remainder = parts[0]
        else:
            top = parts[0]
            remainder = "/".join(parts[1:])

        # Calculate coverage
        lines = f.findall(".//line")
        if not lines:
            continue

        total = len(lines)
        covered = sum(1 for l in lines if int(l.get("hits", "0")) > 0)
        coverage = (covered / total) * 100 if total else 0

        data.append({"package": top, "file": remainder, "coverage": coverage})

    return data


def build_sunburst(data):
    if not data:
        print("No coverage data found.")
        return

    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} entries.")
    print(df.head(10))

    fig = px.sunburst(
        df,
        path=["package", "file"],
        values="coverage",
        color="coverage",
        color_continuous_scale="RdYlGn",
        title="Cobertura de testes automatizados",
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Coverage: %{value:.1f}%<extra></extra>",
        branchvalues="total",
    )
    fig.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pytest_cov_sunburst.py coverage.xml")
        sys.exit(1)

    xml_path = sys.argv[1]
    data = parse_pytest_cov_xml(xml_path)
    build_sunburst(data)
