#!/usr/bin/env python3
"""
Fetch GitHub release download statistics and generate a graph.

This script fetches download counts from GitHub API, stores historical data,
and generates a graph showing download trends over time.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import requests


def fetch_download_stats(owner: str, repo: str) -> dict:
    """
    Fetch download statistics from GitHub API.

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        dict: Dictionary containing total downloads and timestamp
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {}

    # Fetch all releases with pagination
    all_releases = []
    page = 1
    per_page = 100  # Maximum per page allowed by GitHub API

    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        releases = response.json()
        if not releases:
            break

        all_releases.extend(releases)
        page += 1

        # Check if there are more pages
        if len(releases) < per_page:
            break

    print(f"Fetched {len(all_releases)} releases")

    total_downloads = 0
    release_data = []

    for release in all_releases:
        release_downloads = 0
        for asset in release.get("assets", []):
            release_downloads += asset.get("download_count", 0)

        total_downloads += release_downloads
        release_data.append(
            {
                "tag": release["tag_name"],
                "name": release["name"],
                "downloads": release_downloads,
                "created_at": release["created_at"],
            }
        )

    return {
        "total_downloads": total_downloads,
        "releases": release_data,
    }


def load_history(filepath: Path) -> list:
    """
    Load historical download statistics from JSON file.

    Args:
        filepath: Path to the history JSON file

    Returns:
        list: List of historical data points
    """
    if not filepath.exists():
        return []

    with open(filepath, "r") as f:
        return json.load(f)


def save_history(filepath: Path, history: list) -> None:
    """
    Save historical download statistics to JSON file.

    Args:
        filepath: Path to the history JSON file
        history: List of historical data points
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(history, f, indent=2)


def generate_graph(history: list, output_path: Path, label: str = "") -> None:
    """
    Generate a download statistics graph in Star History (XKCD) style.
    """
    if len(history) < 2:
        print("Not enough data to generate a graph (need at least 2 data points)")
        return

    dates = [datetime.fromisoformat(entry["timestamp"]) for entry in history]
    downloads = [entry["total_downloads"] for entry in history]

    # --- XKCD Style Context ---
    # これにより手書き風のエフェクト（歪んだ線、手書きフォント）が適用されます
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(8, 6))

        # Star History風の色（オレンジ/赤系）
        line_color = "#f05133"

        # プロット
        ax.plot(
            dates,
            downloads,
            color=line_color,
            linewidth=3,
            label=label if label else "Downloads",
        )

        if label:
            legend = ax.legend(loc="upper left", frameon=True, fontsize=10)
            legend.get_frame().set_edgecolor("black")
            legend.get_frame().set_linewidth(1.5)

        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")

        ax.spines["bottom"].set_linewidth(1.5)
        ax.spines["left"].set_linewidth(1.5)

        plt.title("Download History", fontsize=16, y=1.05)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Total Downloads", fontsize=12)

        ax.set_ylim(bottom=0)

        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{int(x):,}"))

        fig.autofmt_xdate(rotation=0, ha="center")

        plt.tight_layout()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
        print(f"Graph saved to {output_path}")


def main():
    """Main function to update download statistics and generate graph."""
    owner = "mjun0812"
    repo = "flash-attention-prebuild-wheels"
    history_file = Path("docs/data/download_history.json")
    graph_output = Path("docs/data/download_graph.png")

    # Fetch current stats
    print("Fetching download statistics from GitHub API...")
    current_stats = fetch_download_stats(owner, repo)
    print(f"Total downloads: {current_stats['total_downloads']}")

    # Load and update history
    history = load_history(history_file)
    history.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_downloads": current_stats["total_downloads"],
        }
    )

    # Save updated history
    save_history(history_file, history)
    print(f"History saved to {history_file}")

    generate_graph(history, graph_output, f"{owner}/{repo}")


if __name__ == "__main__":
    main()
