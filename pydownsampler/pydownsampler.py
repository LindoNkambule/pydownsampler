"""
pydownsampler

Usage:
  pydownsampler (<file>) [-d <dcov>]
  pydownsampler (<file>) [-d <dcov>] [-o <output>]
  pydownsampler (<file>) [-c]
  pydownsampler [-h] | [--help]
  pydownsampler [-v] [--version]

Arguments:
  file                   BAM/SAM/CRAM file to be downsampled (Required argument)

Options:
  -h --help             Show this screen.
  -v --version          Show version.
  -d --downcoverage     The coverage you want to downsample to (Required argument)
  -o --output           Output filename prefix (Optional)
  -c --coverage         Print out average coverage for file
"""

import warnings
import os
import sys
import ntpath
import pysam
from docopt import docopt


def lengths(readinf):
    reads = []
    for read in readinf.fetch():
        if len(reads) > 1000:
            break
        else:
            if read.infer_read_length() is not None:
                # if CIGAR alignment is not present, infer_read_length will return None
                reads.append(read.infer_read_length())

    return reads


def averagerl(readlist):
    readlist.sort()

    # work out difference between second shortest and longest read lengths
    long = readlist[1000]
    short = readlist[1]
    num = long - short
    denom = (long + short) / 2
    percdiff = (num / denom) * 100

    if percdiff > 5:
        warnings.warn("The second longest read of 1002 reads and second shorted read differ by more than 5%")

    pruned = readlist[1:1001]
    rlave = sum(pruned) / 1000

    return rlave


def getversion():
    import pkg_resources
    version = pkg_resources.require("pydownsampler")[0].version
    print("pydownsampler {}".format(version))
    print("using pysam {}".format(pysam.__version__))
    sys.exit(0)


def main():
    # arguments ----------------------------------------------------------------
    args = docopt(__doc__)

    if args['--version']:
        getversion()

    # error handling -----------------------------------------------------------
    if not args['<file>']:
        raise Exception("No input BAM/SAM/CRAM file selected")

    if args['<file>']:
        if not os.path.exists(args['<file>']):
            raise Exception("Failed to open '{}': No such file or directory.".format(args['<file>']))

        # variables ----------------------------------------------------------------
        file = args['<file>']
        downcov = args['<dcov>']

        readnum = 0
        genomelen = 0

        filext = os.path.splitext(file)[-1].lower()

        if not args['<output>']:
            outfile = "Downsampled{}X_{}".format(downcov, ntpath.basename(file))
        else:
            outfile = "{}{}".format(args['<output>'], filext)

        if filext == '.bam':
            bamind1 = "{}.bai".format(file)
            bamind2 = "{}.bai".format(os.path.splitext(file)[0])

            # more error handling ------------------------------------------------------
            if os.path.exists(bamind1) & (not os.path.exists(bamind2)):
                bamind = bamind1
            elif os.path.exists(bamind2) & (not os.path.exists(bamind1)):
                bamind = bamind2
            elif os.path.exists(bamind1) & os.path.exists(bamind2):
                warnings.warn("Input BAM file has two index files. Index file {} will be used".format(bamind1))
                bamind = bamind1
            else:
                raise Exception("Input BAM file {} is not indexed. Please index it and try again.".format(file))

            # file stats ------------------------------------------------------------
            file_stats = pysam.idxstats(file, index_filename=bamind)
            readinfo = pysam.AlignmentFile(file, index_filename=bamind)

        if filext == '.cram':
            # file stats ------------------------------------------------------------
            cramind = "{}.crai".format(os.path.splitext(file)[0])

            if not os.path.exists(cramind):
                raise Exception("Input CRAM file {} is not indexed. Please index it and try again.".format(file))

            file_stats = pysam.idxstats(file, index_filename=cramind)
            readinfo = pysam.AlignmentFile(file, index_filename=cramind)

        if filext == '.sam':
            # file stats ------------------------------------------------------------
            file_stats = pysam.idxstats(file, index_filename=None)
            readinfo = pysam.AlignmentFile(file, index_filename=None)

        # read length --------------------------------------------------------------
        readlens = lengths(readinfo)
        avereadlen = averagerl(readlens)

        for line in file_stats.split("\n"):
            chroms_inf = line.split("\t")
            if len(chroms_inf) > 1 and chroms_inf[0] != '*':
                readnum += int(chroms_inf[2])
                genomelen += int(chroms_inf[1])

        # average coverage ---------------------------------------------------------
        if avereadlen < 100:
            warnings.warn('Your file has reads shorter than 100bp')
            averagecov = (readnum * avereadlen) / genomelen

        elif avereadlen > 160:
            warnings.warn('Your file has reads longer than 160bp')
            averagecov = (readnum * avereadlen) / genomelen

        else:
            averagecov = (readnum * avereadlen) / genomelen

        if args['--coverage']:
            print("Average coverage for {}: {}".format(file, averagecov))
            sys.exit(0)

        else:
            if not args['<dcov>']:
                raise Exception("Please specify the coverage you'd like to downsample to using -d or --downcoverage")

            # downsampling fraction ----------------------------------------------------
            downsamplefrac = int(downcov) / averagecov

            # error handling -----------------------------------------------------------
            if int(downcov) > averagecov:
                raise Exception("The desired coverage is higher than the average coverage")

            if (averagecov - int(downcov)) <= 5:
                raise Exception("The difference between the average coverage and desired coverage is too small (<= 5)")

            # print out some stats -----------------------------------------------------
            print("The average coverage is", averagecov)
            fromcov = str(round(averagecov)) + "X"
            tocov = str(downcov) + "X"
            print("Downsampling {} from {} to {}".format(file, fromcov, tocov))
            print("The downsampling fraction is", downsamplefrac)

            # downsample ---------------------------------------------------------------
            # first 'touch' the output file, so that the `c_open` function can open it
            # https://github.com/pysam-developers/pysam/issues/677
            fh = open(outfile, 'w')
            fh.close()

            # pysam requires arguments to be strings
            pysam.view("-s", str(downsamplefrac), "-b", str(file), "-o", str(outfile), save_stdout=outfile)


if __name__ == '__main__':
    main()
