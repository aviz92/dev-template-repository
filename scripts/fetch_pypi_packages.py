"""
This script fetches all packages owned by the specified PyPI user and their latest versions.
It then prints the results in a format suitable for inclusion in a pyproject.toml dependencies list.
"""

import json
import sys
import urllib.request
import xmlrpc.client

PYPI_USER = "aviz"


def get_user_packages(user: str) -> list[str]:
    client = xmlrpc.client.ServerProxy("https://pypi.org/pypi")
    roles = client.user_packages(user)  # returns [["Owner", "pkg-name"], ...]
    return sorted({pkg for _, pkg in roles})


def get_latest_version(package: str) -> str:
    url = f"https://pypi.org/pypi/{package}/json"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    return data["info"]["version"]


def main() -> None:
    print(f"Fetching packages for PyPI user: {PYPI_USER}\n")

    if not (packages := get_user_packages(PYPI_USER)):
        print("No packages found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(packages)} packages\n")

    results = []
    for pkg in packages:
        try:
            version = get_latest_version(pkg)
            results.append((pkg, version))
            print(f"  ✓ {pkg} = {version}")
        except Exception as e:
            print(f"  ✗ {pkg} — error: {e}")

    # pyproject.toml output
    print("\ndependencies = [")
    for pkg, version in results:
        print(f'    "{pkg}>={version}",')
    print("]")


if __name__ == "__main__":
    main()
