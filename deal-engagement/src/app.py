"""
Streamlit frontend for the Deal Engagement Extractor.
Run with: streamlit run app.py
(or double-click start.command / start.bat)
"""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml
from dotenv import load_dotenv

import run as core

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

st.set_page_config(
    page_title="HubSpot Deal Engagement",
    page_icon="📊",
    layout="wide",
)

# ----------------------------------------------------------------------------
# Sidebar — configuration
# ----------------------------------------------------------------------------
with (ROOT / "config.yaml").open() as f:
    cfg = yaml.safe_load(f)

st.sidebar.title("⚙️ Configuration")

list_id = st.sidebar.number_input(
    "HubSpot List ID",
    value=int(cfg.get("list_id", 17603)),
    step=1,
    help="ID of the HubSpot deal segment to analyse.",
)

score_property = st.sidebar.selectbox(
    "Score property",
    options=["lead_score_contacts_total", "lead_score_contacts_engagement"],
    index=0,
    help="HubSpot property to use as lead score.",
)

threshold_choice = st.sidebar.selectbox(
    "Minimum score threshold",
    options=[
        "All scored (exclude only unscored)",
        "≥ 1 (exclude zero too)",
        "≥ 5 (Medium or above)",
        "≥ 10 (High)",
        "≥ 25",
        "≥ 50 (MQL)",
    ],
    index=0,
)
threshold_map = {
    "All scored (exclude only unscored)": None,
    "≥ 1 (exclude zero too)": 1,
    "≥ 5 (Medium or above)": 5,
    "≥ 10 (High)": 10,
    "≥ 25": 25,
    "≥ 50 (MQL)": 50,
}
threshold = threshold_map[threshold_choice]

# Token — pre-filled from .env if available
_env_token = os.getenv("HUBSPOT_TOKEN", "")
if _env_token:
    st.sidebar.text_input(
        "HubSpot Private App Token",
        value="••••••••••••••••••••",
        disabled=True,
        help="Token loaded from .env — no action needed.",
    )
    token = _env_token
else:
    token = st.sidebar.text_input(
        "HubSpot Private App Token",
        type="password",
        value="",
        help="Settings → Integrations → Private Apps. The token stays in memory only.",
    )

st.sidebar.markdown("---")
use_cache = st.sidebar.checkbox(
    "Use local cache (data/cache)",
    value=True,
    help="If enabled, reuses previously downloaded JSON files instead of calling HubSpot again.",
)

st.sidebar.markdown("---")
st.sidebar.caption("v1.0 · Doxee Marketing AI")

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
st.title("📊 HubSpot Deal Engagement Report")
st.markdown(
    "Pulls all **accounts / opportunities** from a HubSpot segment and lists contacts "
    "with a **valued lead score**. Output: downloadable Excel file."
)

run_btn = st.button("▶︎ Generate report", type="primary")

if run_btn:
    if not token:
        st.error("HubSpot token missing. Add it in the sidebar or set HUBSPOT_TOKEN in .env.")
        st.stop()

    progress = st.progress(0, text="Starting…")
    log_box = st.expander("📋 Detailed log", expanded=False)
    log_lines: list[str] = []

    def log(msg: str) -> None:
        log_lines.append(msg)
        log_box.code("\n".join(log_lines))

    try:
        force = not use_cache

        progress.progress(10, text="Step 1/6 — list memberships")
        mem = core.load_or_fetch(
            1, lambda: core.step1_list_memberships(token, list_id), force=force
        )
        deal_ids = [str(r["recordId"]) for r in mem["results"]]
        log(f"Step 1: {len(deal_ids)} deals in segment")

        progress.progress(25, text="Step 2/6 — deal detail")
        deals = core.load_or_fetch(
            2, lambda: core.step2_deals_detail(token, deal_ids), force=force
        )
        log(f"Step 2: details for {len(deals['results'])} deals")

        progress.progress(40, text="Step 3/6 — deal → company")
        d2c = core.load_or_fetch(
            3, lambda: core.step3_deal_to_companies(token, deal_ids), force=force
        )
        company_ids = list(
            {str(t["toObjectId"]) for r in d2c["results"] for t in r["to"]}
        )
        log(f"Step 3: {len(company_ids)} unique companies")

        progress.progress(55, text="Step 4/6 — company detail")
        companies = core.load_or_fetch(
            4,
            lambda: core.step4_companies_detail(token, company_ids),
            force=force,
        )
        log("Step 4: account names retrieved")

        progress.progress(70, text="Step 5/6 — company → contacts")
        c2c = core.load_or_fetch(
            5,
            lambda: core.step5_company_to_contacts(token, company_ids),
            force=force,
        )
        contact_ids = list(
            {str(t["toObjectId"]) for r in c2c["results"] for t in r["to"]}
        )
        log(f"Step 5: {len(contact_ids)} total contacts across companies")

        progress.progress(85, text="Step 6/6 — contact detail + score")
        contacts = core.load_or_fetch(
            6,
            lambda: core.step6_contacts_detail(token, contact_ids, score_property),
            force=force,
        )
        log("Step 6: contact info + scores")

        progress.progress(95, text="Aggregating and building Excel…")
        groups = core.aggregate(
            deals, d2c, companies, c2c, contacts, score_property, threshold
        )
        total_engaged = sum(len(g["contacts"]) for g in groups)
        log(f"Score filter (threshold={threshold}): {total_engaged} contacts")

        ts = datetime.now().strftime("%Y%m%d_%H%M")
        out_path = ROOT / "output" / f"hubspot_deal_report_{ts}.xlsx"
        core.write_xlsx(groups, out_path)
        progress.progress(100, text="Done ✓")

        st.success(f"Report ready: **{out_path.name}**")

        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Deals", len(groups))
        c2.metric("Accounts", len({g["account_name"] for g in groups}))
        c3.metric("Engaged contacts", total_engaged)
        c4.metric(
            "Total pipeline (€)",
            f"{sum((g['amount'] or 0) for g in groups):,.0f}",
        )

        # Download
        with out_path.open("rb") as f:
            st.download_button(
                "⬇︎ Download Excel",
                data=f.read(),
                file_name=out_path.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
            )

        # Preview
        st.subheader("Preview")
        rows = []
        for g in groups:
            if not g["contacts"]:
                rows.append(
                    {
                        "Account": g["account_name"],
                        "Opportunity": g["deal_name"],
                        "Amount (€)": g["amount"],
                        "SF Create Date": g["close_date"],
                        "Contact": "(no engaged contacts)",
                        "Job Title": "",
                        "Email": "",
                        "Score": "—",
                        "Analytics Source": "",
                        "Source Data 1": "",
                        "Source Data 2": "",
                        "First Touch Campaign": "",
                    }
                )
                continue
            for c in g["contacts"]:
                rows.append(
                    {
                        "Account": g["account_name"],
                        "Opportunity": g["deal_name"],
                        "Amount (€)": g["amount"],
                        "SF Create Date": g["close_date"],
                        "Contact": c["name"],
                        "Job Title": c["jobtitle"],
                        "Email": c["email"],
                        "Score": c["score"],
                        "Analytics Source": c["source"],
                        "Source Data 1": c["source_data_1"],
                        "Source Data 2": c["source_data_2"],
                        "First Touch Campaign": c["first_touch_campaign"],
                    }
                )
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.warning("No rows to display.")

    except Exception as e:
        progress.empty()
        st.error(f"Error during execution: {e}")
        st.exception(e)
else:
    st.info(
        "Set parameters in the sidebar and click **Generate report**. "
        "The first run makes ~6 HubSpot API calls (~30 sec). "
        "Subsequent runs with cache enabled are near-instant."
    )
