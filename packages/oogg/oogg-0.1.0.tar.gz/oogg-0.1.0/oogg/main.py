import argparse
import re
import subprocess

GITHUB_URL: str = "https://github.com/{user}/{repository}/blob/{branch}/{file}"
GITLAB_URL: str = (
    "https://gitlab.com/{user}/{repository}/-/blob/{branch}/{file}"
)


def get_current_branch() -> str:
    out = subprocess.run(
        ("git", "branch", "--show-current"),
        capture_output=True,
    )
    return out.stdout.strip().decode("utf-8")


def get_current_repository() -> str:
    out = subprocess.run(
        ("git", "config", "--get", "remote.origin.url"),
        capture_output=True,
    )
    return re.split("/|.git", out.stdout.strip().decode("utf-8"))[-2]


def get_current_user() -> str:
    out = subprocess.run(
        ("git", "config", "--get", "remote.origin.url"),
        capture_output=True,
    )
    return re.split(":|/", out.stdout.strip().decode("utf-8"))[-2]


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        help="Specify the file path to open.",
        required=True,
    )
    parser.add_argument(
        "--line",
        help="The line in the file that will be opened.",
    )

    parser.add_argument(
        "--user",
        help="Username in GitHub/GitLab.",
        default=get_current_user(),
    )
    parser.add_argument(
        "--repository",
        help="Repository in GitHub/GitLab.",
        default=get_current_repository(),
    )
    parser.add_argument(
        "--branch",
        help="Repository branch",
        default=get_current_branch(),
    )
    parser.add_argument(
        "--gitlab",
        action="store_false",
        help="Open on GitLab",
        default=False,
    )

    return parser.parse_args()


def main() -> int:
    args = create_parser()

    url = GITHUB_URL if not args.gitlab else GITLAB_URL
    url = url.format(
        user=args.user,
        repository=args.repository,
        branch=args.branch,
        file=args.path,
    )

    url += f"#L{args.line}" if args.line else ""

    out = subprocess.run(
        ("xdg-open", url),
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    print("Opened your file in your prefered browser.")
    return out.returncode
