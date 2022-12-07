from dataclasses import dataclass
from typing import Union, Iterator

@dataclass
class File:
    name: str
    size: int

@dataclass
class Directory:
    path: list[str]
    files: dict[str, Union[File, 'Directory']]
    parent: Union[None, 'Directory'] = None
    size: int = -1


def compute_sizes(dir: Directory) -> int:
    dir_size = 0
    for file in dir.files.values():
        match file:
            case File(_, size):
                dir_size += size
            case Directory():
                dir_size += compute_sizes(file)
    dir.size = dir_size

    return dir_size

def learn_filesystem(raw: str) -> Directory:
    """Parse the filesystem from the raw string and return the root directory"""
    root = Directory([], {})
    pwd: Directory = root

    commands = [x.strip() for x in raw.split("$ ") if x.strip()]

    for command in commands:
        lines = command.split("\n")

        match lines:
            case ["ls", *rest]:
                for listing in rest:
                    match listing.split():
                        case ["dir", dirname]:
                            if "dirname" not in pwd.files:
                                pwd.files[dirname] = Directory(pwd.path + [dirname], {}, pwd)
                        case [size, filename]:
                            pwd.files[filename] = File(filename, int(size))
            case [cd]:
                match cd.split():
                    case ["cd", "/"]:
                        pwd = root
                    case ["cd", ".."]:
                        pwd = pwd.parent if pwd.parent else pwd
                    case ["cd", dirname]:
                        if dirname in pwd.files:
                            newdir = pwd.files[dirname]
                            assert isinstance(newdir, Directory)
                            pwd = newdir
                        else:
                            pwd.files[dirname] = Directory(pwd.path + [dirname], {}, pwd)

    compute_sizes(root)
    return root

RAW = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

FS = learn_filesystem(RAW)


def all_directories_below(root: Directory, size: int = 100_000) -> Iterator[Directory]:
    if root.size <= size:
        yield root
    for file in root.files.values():
        match file:
            case Directory():
                yield from all_directories_below(file, size)
            case _:
                pass

assert sum(dir.size for dir in all_directories_below(FS)) == 95437

with open('day07.txt') as f:
    fs = learn_filesystem(f.read())

print(sum(dir.size for dir in all_directories_below(fs)))

TOTAL_DISK_SIZE = 70_000_000
NEED_UNUSED_SIZE = 30_000_000
MAX_SIZE = TOTAL_DISK_SIZE - NEED_UNUSED_SIZE  # 40_000_000

USED_SIZE = FS.size 
NEED_TO_FREE = USED_SIZE - MAX_SIZE
assert NEED_TO_FREE == 8_381_165

def candidate_directories(root: Directory, need_to_free: int) -> Iterator[Directory]:
    for file in root.files.values():
        match file:
            case Directory(_, _, _, size):
                if size >= need_to_free:
                    yield file
                yield from candidate_directories(file, need_to_free)
            case _:
                pass

assert min(dir.size for dir in candidate_directories(FS, NEED_TO_FREE)) == 24_933_642

used_size = fs.size 
need_to_free = used_size - MAX_SIZE

print(min(dir.size for dir in candidate_directories(fs, need_to_free)))