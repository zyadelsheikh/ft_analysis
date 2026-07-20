import streamlit as st


def inject_styles():
    st.markdown(
        """
        <style>
        .app-hero { background: linear-gradient(135deg,#172b2b 0%,#102020 55%,#0c1515 100%); border:1px solid #274444; border-radius:20px; padding:26px 28px 22px; margin:4px 0 22px; box-shadow:0 14px 36px rgba(0,0,0,.18); }
        .app-kicker { color:#62e6b5; font-size:12px; font-weight:700; letter-spacing:1.6px; text-transform:uppercase; margin-bottom:7px; }
        .app-title { color:#f8fafc; font-size:34px; font-weight:800; line-height:1.1; margin:0; }
        .app-subtitle { color:#b3c6c3; font-size:14px; margin-top:8px; }
        .app-section { color:#e7f5f1; font-size:19px; font-weight:750; margin:18px 0 14px; }
        .app-card { background:#122323; border:1px solid #274141; border-radius:14px; padding:14px 15px; margin-bottom:10px; }
        div[data-testid="stMetric"] { background:rgba(255,255,255,.055); border:1px solid rgba(130,239,203,.18); border-radius:13px; padding:13px 14px; }
        div[data-testid="stPlotlyChart"] { background:#122323; border:1px solid #274141; border-radius:16px; padding:8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(kicker: str, title: str, subtitle: str):
    st.markdown(
        f'<div class="app-hero"><div class="app-kicker">{kicker}</div>'
        f'<div class="app-title">{title}</div>'
        f'<div class="app-subtitle">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


def section(title, icon=""):
    icons = {
        "scorers": """
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
                 stroke="#fbbf24" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M8 21h8"/>
                <path d="M12 17v4"/>
                <path d="M7 4h10v5a5 5 0 0 1-10 0V4Z"/>
                <path d="M7 7H4a3 3 0 0 0 3 3"/>
                <path d="M17 7h3a3 3 0 0 1-3 3"/>
            </svg>
        """,
        "assisters": """
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
                 stroke="#38bdf8" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <circle cx="12" cy="12" r="9"/>
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 3v6"/>
                <path d="M21 12h-6"/>
                <path d="M12 21v-6"/>
                <path d="M3 12h6"/>
            </svg>
        """,
    }

    st.markdown(
        f"""
        <div class="app-section" style="
            display:flex;
            align-items:center;
            gap:10px;
        ">
            <span style="
                display:flex;
                align-items:center;
                justify-content:center;
                width:34px;
                height:34px;
                border-radius:10px;
                background:rgba(255,255,255,.07);
                border:1px solid rgba(255,255,255,.12);
            ">
                {icons.get(icon, "")}
            </span>
            <span>{title}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
