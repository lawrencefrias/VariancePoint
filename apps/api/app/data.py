from __future__ import annotations

import json
import os
import tempfile
import threading
from datetime import date
from pathlib import Path

from .models import CommunityInsight, LifecycleEvent, MortalityInput, Technology

TECHNOLOGIES = [
    Technology(id="adfs", name="ADFS", vendor="Microsoft", category="Identity"),
    Technology(id="citrix-virtual-apps", name="Citrix Virtual Apps", vendor="Citrix", category="Virtualization"),
    Technology(id="exchange-onprem", name="Exchange On-Prem", vendor="Microsoft", category="Messaging"),
    Technology(id="vmware-legacy", name="Legacy VMware Estate", vendor="Broadcom", category="Virtualization"),
    Technology(id="sccm-legacy", name="Legacy SCCM", vendor="Microsoft", category="Endpoint Management"),
    Technology(id="windows-server-2016", name="Windows Server 2016", vendor="Microsoft", category="Server"),
]

_TECHNOLOGY_NAME_TO_ID: dict[str, str] = {t.name: t.id for t in TECHNOLOGIES}

_LIFECYCLE_SEED_FILE = Path(
    os.environ.get(
        "LIFECYCLE_SEED_FILE",
        str(Path(__file__).parents[3] / "datasets" / "lifecycle" / "sample_lifecycle_events.json"),
    )
)


def _load_lifecycle_events() -> list[LifecycleEvent]:
    raw: list[dict] = json.loads(_LIFECYCLE_SEED_FILE.read_text())
    events: list[LifecycleEvent] = []
    for entry in raw:
        technology_id = _TECHNOLOGY_NAME_TO_ID.get(entry["technology"])
        if technology_id is None:
            continue
        events.append(
            LifecycleEvent(
                technology_id=technology_id,
                event_type=entry["event"],
                event_date=date.fromisoformat(entry["date"]),
            )
        )
    return events


LIFECYCLE_EVENTS: list[LifecycleEvent] = _load_lifecycle_events()

MORTALITY_INPUTS: list[MortalityInput] = [
    MortalityInput(
        technology_id="adfs",
        adoption_score=20.0,
        community_momentum_score=15.0,
        vendor_investment_score=10.0,
        talent_availability_score=25.0,
        migration_urgency_score=80.0,
    ),
    MortalityInput(
        technology_id="citrix-virtual-apps",
        adoption_score=35.0,
        community_momentum_score=30.0,
        vendor_investment_score=25.0,
        talent_availability_score=40.0,
        migration_urgency_score=60.0,
    ),
    MortalityInput(
        technology_id="exchange-onprem",
        adoption_score=25.0,
        community_momentum_score=20.0,
        vendor_investment_score=15.0,
        talent_availability_score=30.0,
        migration_urgency_score=70.0,
    ),
    MortalityInput(
        technology_id="vmware-legacy",
        adoption_score=30.0,
        community_momentum_score=20.0,
        vendor_investment_score=10.0,
        talent_availability_score=35.0,
        migration_urgency_score=85.0,
    ),
    MortalityInput(
        technology_id="sccm-legacy",
        adoption_score=40.0,
        community_momentum_score=35.0,
        vendor_investment_score=30.0,
        talent_availability_score=45.0,
        migration_urgency_score=55.0,
    ),
]

_INSIGHTS_FILE = Path(os.environ.get("INSIGHTS_FILE", Path(__file__).parent.parent / "community_insights.json"))
_INSIGHTS_LOCK = threading.Lock()


def _load_insights() -> list[CommunityInsight]:
    if _INSIGHTS_FILE.exists():
        raw = json.loads(_INSIGHTS_FILE.read_text())
        return [CommunityInsight(**item) for item in raw]
    return []


def _save_insights(insights: list[CommunityInsight]) -> None:
    _INSIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps([item.model_dump() for item in insights], default=str)
    fd, tmp_path = tempfile.mkstemp(dir=_INSIGHTS_FILE.parent)
    try:
        os.write(fd, payload.encode())
        os.close(fd)
        os.replace(tmp_path, _INSIGHTS_FILE)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


COMMUNITY_INSIGHTS: list[CommunityInsight] = _load_insights()
