# smgantt

Snakemake Gantt

## Install

```
pip install smgantt==0.0.3
```

## Usage

```
$ smgantt --help
usage: smgantt [-h] [-V] [-m METADATA] [-o OUTPUT] [-s MIN_SECONDS] [-n]

Snakemake Gantt 0.0.3

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -m METADATA, --metadata METADATA
                        Snakemake metadata directory, default: .snakemake/metadata
  -o OUTPUT, --output OUTPUT
                        Output image, default: gantt.png
  -s MIN_SECONDS, --min-seconds MIN_SECONDS
                        Minimum runtime in seconds, default: None, means all
  -n, --sort-by-name    Sort by rule name, default: False
```

## Example

```
smgantt -s 10
```

![image-20220210101227142](https://vs-picgo.oss-cn-zhangjiakou.aliyuncs.com/image-20220210101227142.png)
