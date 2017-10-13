import nanoget
from os import path
from argparse import ArgumentParser
from nanoplot import utils
import nanoplotter
import pandas as pd
import numpy as np
import logging
from .version import __version__


def main():
    '''
    Organization function
    -setups logging
    -gets inputdata
    -calls plotting function
    '''
    args = get_args()
    try:
        utils.make_output_dir(args.outdir)
        utils.init_logs(args)
        args.format = nanoplotter.check_valid_format(args.format)
        datadf = get_input(args)
        make_plots(datadf, path.join(args.outdir, args.prefix), args)
        logging.info("Succesfully processed all input.")
    except Exception as e:
        logging.error(e, exc_info=True)
        raise


def get_args():
    parser = ArgumentParser(description="Compares Oxford Nanopore Sequencing datasets.")
    parser.add_argument("-v", "--version",
                        help="Print version and exit.",
                        action="version",
                        version='NanoComp {}'.format(__version__))
    parser.add_argument("-t", "--threads",
                        help="Set the allowed number of threads to be used by the script",
                        default=4,
                        type=int)
    parser.add_argument("--readtype",
                        help="Which read type to extract information about from summary. \
                             Options are 1D, 2D, 1D2",
                        default="1D",
                        choices=['1D', '2D', '1D2'])
    parser.add_argument("-o", "--outdir",
                        help="Specify directory in which output has to be created.",
                        default=".")
    parser.add_argument("-p", "--prefix",
                        help="Specify an optional prefix to be used for the output files.",
                        default="",
                        type=str)
    parser.add_argument("-f", "--format",
                        help="Specify the output format of the plots.",
                        default="png",
                        type=str,
                        choices=['eps', 'jpeg', 'jpg', 'pdf', 'pgf', 'png', 'ps',
                                 'raw', 'rgba', 'svg', 'svgz', 'tif', 'tiff'])
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--fastq",
                        help="Data is in default fastq format.",
                        nargs='*')
    target.add_argument("--summary",
                        help="Data is a summary file generated by albacore.",
                        nargs='*')
    target.add_argument("--bam",
                        help="Data as a sorted bam file.",
                        nargs='*')
    return parser.parse_args()


def get_input(args):
    '''
    Get input and process accordingly.
    Data can be:
    - a uncompressed, bgzip, bzip2 or gzip compressed fastq file
    - a sorted bam file
    - a sequencing_summary.txt file generated by albacore
    Handle is passed to the proper functions to get DataFrame with metrics
    Multiple files of the same type can be used to extract info from
    The resulting output DataFrames are concatenated
    '''
    if args.fastq:
        datadf = combine_dfs(
            dfs=[nanoget.process_fastq_plain(inp, args.threads) for inp in args.fastq],
            names=[args.fastq])
    elif args.bam:
        datadf = combine_dfs(
            dfs=[nanoget.process_bam(inp, args.threads) for inp in args.bam],
            names=[args.bam])
    elif args.summary:
        datadf = combine_dfs(
            dfs=[nanoget.process_summary(inp, args.readtype) for inp in args.summary],
            names=args.summary)
    logging.info("Gathered metrics for plotting")
    return datadf


def combine_dfs(dfs, names):
    res = []
    for df, identifier in zip(dfs, names):
        df["dataset"] = identifier
        res.append(df)
    return pd.concat(res, ignore_index=True)


def make_plots(df, path, args):
    df["log length"] = np.log10(df["lengths"])
    nanoplotter.violinplots(
        df=df,
        y="lengths",
        figformat=args.format,
        path=path)
    nanoplotter.violinplots(
        df=df,
        y="log length",
        figformat=args.format,
        path=path,
        logBool=True
    )
    nanoplotter.violinplots(
        df=df,
        y="quals",
        figformat=args.format,
        path=path
    )
    if args.bam:
        nanoplotter.violinplots(
            df=df,
            y="percentIdentity",
            figformat=args.format,
            path=path,
        )


if __name__ == '__main__':
    main()
