"""
admin_config.py - Aesthetic Physique Admin Operations Console Configuration
Architectural Role: Central configuration, permission matrix, KPI schemas, badge constraint
definitions, and system constants for the Aesthetic Physique Admin Console.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class AdminRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    COACH_MANAGER = "COACH_MANAGER"


class ConstraintType(str, Enum):
    STREAK_DAYS = "STREAK_DAYS"
    TOTAL_FAILURE_REPS = "TOTAL_FAILURE_REPS"
    HYDRATION_STREAK = "HYDRATION_STREAK"
    SLEEP_CONSISTENCY = "SLEEP_CONSISTENCY"
    MANUAL_AWARD = "MANUAL_AWARD"


class BadgeTier(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


class TicketStatus(str, Enum):
    UNREAD = "UNREAD"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class AuditLogAction(str, Enum):
    USER_EDIT = "USER_EDIT"
    BADGE_CREATE = "BADGE_CREATE"
    BADGE_ASSIGN = "BADGE_ASSIGN"
    BADGE_REVOKE = "BADGE_REVOKE"
    SYSTEM_CONFIG = "SYSTEM_CONFIG"
    TICKET_REPLY = "TICKET_REPLY"


# Visual styling tokens for Badge Tiers in Web Admin & Portals
TIER_STYLING: Dict[str, Dict[str, str]] = {
    BadgeTier.BRONZE.value: {
        "label": "Bronze",
        "primary_color": "#CD7F32",
        "secondary_color": "#8C5523",
        "bg_gradient_start": "#2A1808",
        "bg_gradient_end": "#170E05",
        "border_color": "#D78E44",
        "glow_color": "#CD7F3244",
    },
    BadgeTier.SILVER.value: {
        "label": "Silver",
        "primary_color": "#C0C0C0",
        "secondary_color": "#7F8C8D",
        "bg_gradient_start": "#1C2329",
        "bg_gradient_end": "#0E1317",
        "border_color": "#E0E0E0",
        "glow_color": "#C0C0C044",
    },
    BadgeTier.GOLD.value: {
        "label": "Gold",
        "primary_color": "#FFD700",
        "secondary_color": "#D4AC0D",
        "bg_gradient_start": "#2A2300",
        "bg_gradient_end": "#161200",
        "border_color": "#F4D03F",
        "glow_color": "#FFD70055",
    },
    BadgeTier.PLATINUM.value: {
        "label": "Platinum",
        "primary_color": "#00F2FE",
        "secondary_color": "#4FACFE",
        "bg_gradient_start": "#031B2A",
        "bg_gradient_end": "#010C14",
        "border_color": "#00F2FE",
        "glow_color": "#00F2FE66",
    },
}

# Navigation Tabs configuration for the Admin Console sidebar / topbar
ADMIN_NAV_TABS = [
    {
        "key": "dashboard",
        "label": "Dashboard Analytics",
        "icon": "analytics_outlined",
        "active_icon": "analytics_rounded",
        "min_role": AdminRole.SUPPORT_AGENT,
    },
    {
        "key": "users",
        "label": "Athletes Ledger",
        "icon": "people_outline_rounded",
        "active_icon": "people_rounded",
        "min_role": AdminRole.SUPPORT_AGENT,
    },
    {
        "key": "badge_studio",
        "label": "Badge Studio",
        "icon": "workspace_premium_outlined",
        "active_icon": "workspace_premium_rounded",
        "min_role": AdminRole.COACH_MANAGER,
    },
    {
        "key": "badge_manager",
        "label": "Direct Assignment",
        "icon": "assignment_ind_outlined",
        "active_icon": "assignment_ind_rounded",
        "min_role": AdminRole.SUPER_ADMIN,
    },
    {
        "key": "inbox",
        "label": "Support Inbox",
        "icon": "mark_email_unread_outlined",
        "active_icon": "mark_email_unread_rounded",
        "min_role": AdminRole.SUPPORT_AGENT,
    },
    {
        "key": "version_manager",
        "label": "Documentation & Version",
        "icon": "phonelink_setup_rounded",
        "active_icon": "phonelink_setup_rounded",
        "min_role": AdminRole.SUPER_ADMIN,
    },
]

# Support Inbox Icons
INBOX_ICON_DEFAULT = "✉️"
INBOX_ICON_ACTIVE = "📩"

# Default Server & Mobile Client Version Registry
DEFAULT_VERSION_CONFIG = {
    "latest_mobile_version": "1.2.0",
    "min_required_mobile_version": "1.0.0",
    "apk_download_url": "https://cdn.aestheticphysique.com/builds/AestheticPhysique-v1.2.0.apk",
    "documentation_url": "https://docs.aestheticphysique.com/athlete-guide",
    "release_notes": "Added 52 unilateral routines, real-time rest audio coordinator, and Supabase cloud sync.",
    "force_update_flag": False,
}

# Operations Metrics Thresholds & Defaults
DEFAULT_OPS_METRICS = {
    "total_athletes": 1284,
    "active_today": 342,
    "total_sets_completed": 18920,
    "failure_sets_logged": 4821,
    "server_status": "OPERATIONAL",
    "uptime_percentage": "99.98%",
    "avg_rest_compliance": "94.6%",
    "active_tickets_count": 5,
}
