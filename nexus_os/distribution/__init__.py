from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DistributionPlan:
    channels: list[str]
    segments: list[str]
    campaigns: list[str]
    launch_sequence: list[str]
    feedback_loop: list[str]


def build_distribution(product_name: str) -> DistributionPlan:
    name = product_name.lower()

    channels = ["direct_sales", "content", "partnerships"]
    segments = ["smb", "mid_market", "enterprise"]

    if "enterprise" in name:
        channels.append("account_based_sales")
        segments = ["enterprise"]

    campaigns = [
        f"launch_{product_name}",
        "customer_case_studies",
        "demo_campaign",
    ]

    launch_sequence = [
        "internal_validation",
        "beta_release",
        "public_launch",
        "scale_distribution",
    ]

    feedback_loop = [
        "collect_usage",
        "analyze_feedback",
        "prioritize_updates",
    ]

    return DistributionPlan(channels, segments, campaigns, launch_sequence, feedback_loop)


__all__ = ["DistributionPlan", "build_distribution"]
