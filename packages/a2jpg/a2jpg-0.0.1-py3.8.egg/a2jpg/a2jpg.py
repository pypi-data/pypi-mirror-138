import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from pathlib import Path
import subprocess


def command_run(cmd=None):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    proc.wait()


class job:
    def __init__(self, img_from=None, img_to=None):
        self.img_from = img_from
        self.img_to = img_to

        self.done = False

        assert self.img_from is not None
        assert self.img_to is not None

    def do(self):
        os.makedirs(os.path.dirname(self.img_to), exist_ok=True)
        command_run(cmd="sips -s format jpeg {} --out {}".format(self.img_from, self.img_to))
        self.done = True


def display(jobs):
    while sum([j_.done for j_ in jobs]) < len(jobs):
        if sum([j_.done for j_ in jobs]) == len(jobs) - 1:
            print(" ({}/{})".format(sum([j_.done for j_ in jobs]), len(jobs)))
        else:
            print(" ({}/{})".format(sum([j_.done for j_ in jobs]), len(jobs)), end="\r")
        time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help="input image or path.", type=str, required=True)
    parser.add_argument('-f', help="image format (Default: *.ARW)", type=str, default="*.ARW")
    parser.add_argument('-c', help="quality in % (Default: 100)", type=int, default=100)
    parser.add_argument('-w', help="number of worker (Default: 2)", type=int, default=2)

    try:
        args = parser.parse_args()
    except AttributeError:
        parser.print_help()
        exit(0)

    # search
    img_path = os.path.abspath(args.i)
    img_list = list(Path(img_path).glob(args.f))

    img_convert_list = [
        [str(i.absolute()), os.path.join(os.path.dirname(i), "jpg", i.name.replace(args.f.split(".")[-1], "jpg"))] for i
        in img_list]

    jobs = [job(img_from=v[0], img_to=v[1]) for v in img_convert_list]

    executor = ThreadPoolExecutor(max_workers=args.w)

    start_time = time.time()
    futures = [executor.submit(display, jobs)]
    for j in jobs:
        futures.append(executor.submit(j.do))

    for _ in as_completed(futures):
        pass

    print(" ({}/{}) finish in {} sec.".format(len(jobs), len(jobs), round(time.time() - start_time, 2)))


if __name__ == '__main__':
    main()
