import re

from typing import Tuple, List, Dict, Iterable, Union, Optional


def main():
    raw_orbits = load_raw_data()

    orbit_dict = build_orbital_dict(raw_orbits)

    total_orbits = sum([o["count"] for o in orbit_dict.values()])

    print("The total number of orbits in the system is: %d" % total_orbits)


def load_raw_data() -> Iterable[Tuple[str, str]]:
    regex = re.compile(r'(.*)\)(.*)')
    with open("input/input06.txt", "r") as f:
        for line in f.readlines():
            m = regex.match(line.strip())
            yield m.group(1), m.group(2)


def build_orbital_dict(orbits: Iterable[Tuple[str, str]]) -> Dict[str, dict]:
    orbit_dict = {o[1]: {"direct": o[0]} for o in orbits}

    for orbit in orbit_dict.keys():
        orbit_dict[orbit]["count"] = count_orbits(orbit, orbit_dict)

    return orbit_dict


def count_orbits(orbit: str, orbit_dict: Dict[str, dict]) -> int:
    if orbit not in orbit_dict:
        return 0
    if "count" not in orbit_dict[orbit]:
        orbit_dict[orbit]["count"] = count_orbits(orbit_dict[orbit]["direct"], orbit_dict) + 1
    return orbit_dict[orbit]["count"]


if __name__ == "__main__":
    main()
