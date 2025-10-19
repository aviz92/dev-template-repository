import argparse
import os

from custom_python_logger import build_logger
from python_github_plus import GitHubClient

logger = build_logger(__name__)


def run_pytest_marker_workflow(
    marker: str,
    repo_full_name: str = "aviz92/dev-template-repository",
    branch: str | None = None,
    workflow_name: str = "Pytest by Marker",
) -> None:
    github_client = GitHubClient(access_token=os.environ.get("GITHUB_TOKEN"), repo_full_name=repo_full_name)

    if branch is None:
        branch = github_client.branch.get_current_branch()
        logger.debug(f"Detected current branch: {branch}")

    logger.debug("Running Pytest workflow with:" f"Marker: {marker}" f"Branch: {branch}" f"Repo: {repo_full_name}")

    response = github_client.workflow.trigger(
        workflow_name=workflow_name, branch_name=branch, inputs={"marker": marker}
    )
    if response.state:
        logger.info("Workflow triggered successfully!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Trigger Pytest workflow on GitHub with a marker.")
    parser.add_argument("marker", help="The marker to run (e.g., unit1)", nargs="?", default=None)
    parser.add_argument(
        "branch", nargs="?", default=None, help="Branch to run workflow on (defaults to current branch)"
    )
    marker = parser.parse_args().marker or "unit2"
    branch = parser.parse_args().branch or "test-ci2"

    run_pytest_marker_workflow(
        marker=marker,
        branch=branch,
    )


if __name__ == "__main__":
    main()
