import re

from typing import Tuple, List, Dict, Iterable, Union, Optional


def main():
    raw_orbits = load_raw_data()

    orbit_dict = build_orbital_dict(raw_orbits)

    path = transfer("YOU", "SAN", orbit_dict)

    print("Orbital transfers from you to Santa: %d" % (len(path) - 3))
    print("Path: %s" % ", ".join(path))


def load_raw_data() -> Iterable[Tuple[str, str]]:
    regex = re.compile(r'(.*)\)(.*)')
    with open("input/input06.txt", "r") as f:
        for line in f.readlines():
            m = regex.match(line.strip())
            yield m.group(1), m.group(2)


def build_orbital_dict(orbits: Iterable[Tuple[str, str]]) -> Dict[str, dict]:
    orbit_dict = {o[1]: {"direct": o[0], "orbits": [], "orbited_by": set(), "directly_orbited_by": set()}
                  for o in orbits}

    for orbit in orbit_dict.keys():
        orbit_dict[orbit]["orbits"] = fill_orbital_hierarchy(orbit, orbit_dict, orbit)

    return orbit_dict


def fill_orbital_hierarchy(orbit: str, orbit_dict: Dict[str, dict], by: str, directly_by: str = None) -> List[str]:
    path = [orbit]
    if orbit not in orbit_dict:
        return path
    if orbit != by:
        orbit_dict[orbit]["orbited_by"].add(by)
    if directly_by:
        orbit_dict[orbit]["directly_orbited_by"].add(directly_by)
    return path + fill_orbital_hierarchy(orbit_dict[orbit]["direct"], orbit_dict, by, orbit)


def transfer(from_orbit: str, to_orbit: str, orbit_map: Dict[str, dict]) -> List[str]:
    orbit = from_orbit
    path = [orbit]
    while orbit != to_orbit:
        if to_orbit in orbit_map[orbit]["orbited_by"]:
            for o in orbit_map[orbit]["directly_orbited_by"]:
                if to_orbit in orbit_map[o]["orbited_by"] or to_orbit == o:
                    orbit = o
                    break
        else:
            orbit = orbit_map[orbit]["direct"]
        path.append(orbit)
    return path


if __name__ == "__main__":
    main()
