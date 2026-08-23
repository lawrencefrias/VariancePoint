from __future__ import annotations

from datetime import date, timedelta

from .models import CommunityInsight, LifecycleEvent, Technology

TECHNOLOGIES = [
    Technology(id="adfs", name="ADFS", vendor="Microsoft", category="Identity"),
    Technology(id="citrix-virtual-apps", name="Citrix Virtual Apps", vendor="Citrix", category="Virtualization"),
    Technology(id="exchange-onprem", name="Exchange On-Prem", vendor="Microsoft", category="Messaging"),
    Technology(id="vmware-legacy", name="Legacy VMware Estate", vendor="Broadcom", category="Virtualization"),
    Technology(id="sccm-legacy", name="Legacy SCCM", vendor="Microsoft", category="Endpoint Management"),
]

LIFECYCLE_EVENTS = [
    LifecycleEvent(technology_id="exchange-onprem", event_type="end_of_support", event_date=date.today() + timedelta(days=620)),
    LifecycleEvent(technology_id="vmware-legacy", event_type="vendor_retirement_signal", event_date=date.today() + timedelta(days=240)),
    LifecycleEvent(technology_id="sccm-legacy", event_type="extended_support", event_date=date.today() + timedelta(days=420)),
]

COMMUNITY_INSIGHTS: list[CommunityInsight] = []
