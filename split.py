#!/usr/bin/env python



"""these routines read and shuffle in a list of sentences for training, dev and
test data."""

import argparse
from typing import Iterator, List
import random
import logging





# create logger
logger = logging.getLogger('split_data.log')










def write_tags(file_path: str, data: str) -> str:
#def write_tags(file_path,data: strstr) -> str:
    with open(file_path, "w") as file:
        for sent in data:
            for line in sent:
                data = " ".join(line)
                file.write(f"{data}\n")
        logger.info('writing data to training, dev and test')


def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
        logger.info('reading data from conll2000')


def main(args: argparse.Namespace) -> None:
    random.seed(args.seed)  # seed data

    #logging.info("Started")
    corpus = list(read_tags("conll2000.tag"))
    # random.seed(args.seed) #seed data
    random.shuffle(corpus)  # shuffle the data

    split_1 = int(0.8 * len(corpus))
    split_2 = int(0.9 * len(corpus))
    training_data = corpus[:split_1]
    dev_data = corpus[split_1:split_2]
    test_data = corpus[split_2:]
    write_tags(args.train, training_data)
    write_tags(args.dev, dev_data)
    write_tags(args.test, test_data)

    corpus = list(read_tags("conll2000.tag"))
    #num_of_prepositions = count_prepositions(corpus)
    #logging.info(f"Found {num_of_prepositions} prepositions.")

    #logging.basicConfig(filename="split.log",level=logging.INFO,
    #format="%(levelname)s:%(message)s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to file for input data", type=str)
    parser.add_argument("train", help="path to file for train data", type=str)
    parser.add_argument("dev", help="path to file for dev data", type=str)
    parser.add_argument("test", help="path to file for test data", type=str)
    parser.add_argument(
        "--seed", help="seeds number generator", type=int, required=True
    )

    logging.basicConfig(filename="split_output.log", level=logging.INFO)

    main(parser.parse_args())


"""
(base) ➜  hw2-reubenraff git:(hw2) ✗ wc -l train.tag dev.tag test.tag
207187 train.tag
26224 dev.tag
25665 test.tag
259076 total

207187. / 259076.
0.7997151415028795
26224. / 259076.
0.10122126325865768
25665. / 259076.
0.09906359523846285
"""





"""
(base) ➜  hw2-reubenraff git:(hw2) ✗ ./split.py conll2000.tag train.tag dev.tag test.tag --seed 250
(base) ➜  hw2-reubenraff git:(hw2) ✗ shasum -a256 train.tag dev.tag test.tag
52075be05277dc52a500e59217007de860aacdb8d99cf0d882b679e46e2f7fb6  train.tag
20c63d10ecc46cd4ddfe4c984cfc485d7f5e71b3a9cf436d7f0e121562f984ff  dev.tag
b8a7ab00cc19d38c86ac99339dd7cfcfe5fd08226acbcdde7e4f99af788398c5  test.tag
(base) ➜  hw2-reubenraff git:(hw2) ✗ ./split.py conll2000.tag train.tag dev.tag test.tag --seed 250
(base) ➜  hw2-reubenraff git:(hw2) ✗ shasum -a256 train.tag dev.tag test.tag
52075be05277dc52a500e59217007de860aacdb8d99cf0d882b679e46e2f7fb6  train.tag
20c63d10ecc46cd4ddfe4c984cfc485d7f5e71b3a9cf436d7f0e121562f984ff  dev.tag
b8a7ab00cc19d38c86ac99339dd7cfcfe5fd08226acbcdde7e4f99af788398c5  test.tag
(base) ➜  hw2-reubenraff git:(hw2) ✗
"""
