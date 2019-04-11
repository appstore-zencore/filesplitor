import os
import math
import glob
from io import open
import click

K=1024
M=1024*1024
G=1024*1024*1024
T=1024*1024*1024*1024
DEFAULT_SIZE = 1 * G
CHUNK_SIZE = 4 * M
verbose = False


def get_slice_size(size):
    size = str(size)
    if not size:
        return DEFAULT_SIZE
    if size[-1].lower() == 'b':
        return int(size[:-1])
    if size[-1].lower() == 'k':
        return int(size[:-1]) * K
    if size[-1].lower() == 'm':
        return int(size[:-1]) * M
    if size[-1].lower() == 'g':
        return int(size[:-1]) * G
    if size[-1].lower() == 't':
        return int(size[:-1]) * T
    return int(size)

def human_readable_size(size):
    if size >= T:
        return "{:.2f}T".format(size/T)
    if size >= G:
        return "{:.2f}G".format(size/G)
    if size >= M:
        return "{:.2f}M".format(size/M)
    if size >= K:
        return "{:.2f}K".format(size/K)
    return str(size) + "B"

def write(src_stream, dst_file_prefix, size, index):
    read_size = CHUNK_SIZE
    index_length = len(str(index))
    dst_file_name_template = "{}.{:0%dd}"%(index_length)
    dst_file_name = dst_file_name_template.format(dst_file_prefix, index)
    with open(dst_file_name, "wb") as fobj:
        while True:
            read_size = min(CHUNK_SIZE, size)
            buffer = src_stream.read(read_size)
            fobj.write(buffer)
            size -= CHUNK_SIZE
            if size < 0:
                break
            if not buffer:
                break
    return dst_file_name

def get_max_index(src_stream, size):
    src_stream.seek(0, 2)
    file_size = src_stream.tell()
    src_stream.seek(0)
    return int(math.ceil(file_size * 1.0/size))


def do_split(src, dst, size, verbose=False):
    if not dst:
        dst = src.name
    size = get_slice_size(size)
    max_index = get_max_index(src, size)
    dst_file_names = []
    if verbose:
        click.echo("Split file [{0}] into {1} sized files...".format(src.name, human_readable_size(size)))
    for index in range(1, max_index + 1):
        dst_file_name = write(src, dst, size, index)
        if verbose:
            click.echo(dst_file_name)
        dst_file_names.append(dst_file_name)
    if verbose:
        print("Done!")

def filecopy(src, dst):
    while True:
        buffer = src.read(CHUNK_SIZE)
        if not buffer:
            break
        dst.write(buffer)

def get_filenames(filenames):
    names = []
    for filename in filenames:
        names += glob.glob(filename)
    return names


def do_merge(dst, filenames):
    filenames = get_filenames(filenames)
    if verbose:
        click.echo("Merge files {0} into one file [{1}]...".format(filenames, dst))
    with open(dst, 'wb') as fobj_output:
        for filename in filenames:
            with open(filename, 'rb') as fobj_input:
                filecopy(fobj_input, fobj_output)
    if verbose:
        print("Done!")

@click.group()
def splitor():
    pass


@splitor.command()
@click.option("-s", "--size", help="File slice size, default to 1G. Accepted units are B, K, M, G, T.")
@click.argument("src", type=click.File('rb'), nargs=1, required=True)
@click.argument("dst", nargs=1, required=False)
def split(size, src, dst):
    do_split(src, dst, size, verbose)


@splitor.command()
@click.argument("dst", nargs=1, required=True)
@click.argument("filenames", nargs=-1, required=True)
def merge(dst, filenames):
    do_merge(dst, filenames)

def main():
    global verbose
    verbose = True 
    splitor()
    
if __name__ == "__main__":
    main()
