import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px

__version__ = "0.0.1"


class Runtime:
    def __init__(self, rule: str, stime: datetime, etime: datetime):
        self.rule = rule
        self.stime = stime
        self.etime = etime
        self.cost = (etime - stime).total_seconds()

    def to_dict(self):
        return {"rule": self.rule, "stime": self.stime, "etime": self.etime, "cost": self.cost}


def get_runtimes(metadata: str) -> pd.DataFrame:
    metadata = Path(metadata)
    counter = defaultdict(int)
    runtimes = []
    for p in metadata.iterdir():
        with p.open() as f:
            data = json.load(f)
            rule = data["rule"]
            stime = datetime.fromtimestamp(data["starttime"])
            etime = datetime.fromtimestamp(data["endtime"])
            counter[rule] += 1
            runtime = Runtime(rule, stime, etime)
            runtimes.append(runtime)
    buckets = defaultdict(int)
    for runtime in runtimes:
        if counter[runtime.rule] > 1:
            buckets[runtime.rule] += 1
            runtime.rule = runtime.rule + "#" + str(buckets[runtime.rule])
    runtimes = sorted(runtimes, key=lambda x: x.stime)
    runtimes = pd.DataFrame([runtime.to_dict() for runtime in runtimes])
    return runtimes


def plot_gantt(runtimes: pd.DataFrame, output: str):
    fig = px.timeline(runtimes, x_start="stime", x_end="etime", y="rule")
    fig.update_yaxes(autorange="reversed")
    height = runtimes.shape[0] * 25
    width = height / 0.618
    fig.write_image(output, engine="kaleido", width=width, height=height)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Snakemake Gantt {}".format(__version__))
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument("-m",
                        "--metadata",
                        type=str,
                        default=".snakemake/metadata",
                        help="Snakemake metadata directory, default: .snakemake/metadata")
    parser.add_argument("-o", "--output", type=str, default="gantt.png", help="Output image, default: gantt.png")
    args = parser.parse_args()
    runtimes = get_runtimes(args.metadata)
    plot_gantt(runtimes, args.output)


if __name__ == "__main__":
    main()
