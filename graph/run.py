import weight
from linking import Linker


if __name__ == "__main__":
    weight.make_graph()
    linker = Linker('./data/seoul_j.json',
                    './data/seoul_link_j.json', 0)
    linker.processing()
