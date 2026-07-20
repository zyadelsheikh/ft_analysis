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


def section(title, icon="chart"):
    icons = {
        "trophy": """
        <svg viewBox="0 0 24 24" width="21" height="21"
             fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="M8 21h8"/>
            <path d="M12 17v4"/>
            <path d="M7 4h10v5a5 5 0 0 1-10 0V4Z"/>
            <path d="M7 7H4a3 3 0 0 0 3 3"/>
            <path d="M17 7h3a3 3 0 0 1-3 3"/>
        </svg>
        """,

        "target": """
        <svg viewBox="0 0 24 24" width="21" height="21"
             fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="9"/>
            <circle cx="12" cy="12" r="5"/>
            <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
        </svg>
        """,

        "chart": """
        <svg viewBox="0 0 24 24" width="21" height="21"
             fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19V5"/>
            <path d="M4 19h16"/>
            <path d="m7 15 3-4 3 2 5-6"/>
        </svg>
        """,

        "users": """
        <svg viewBox="0 0 24 24" width="21" height="21"
             fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        """,

        "team": """
        <svg viewBox="0 0 24 24" width="21" height="21"
             fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 21h18"/>
            <path d="M5 21V8l7-5 7 5v13"/>
            <path d="M9 21v-5h6v5"/>
            <path d="M9 10h.01M15 10h.01"/>
        </svg>
        """,
    }

    icon_html = icons.get(icon, icons["chart"])

    st.markdown(
        f"""
        <div class="app-section" style="
            display:flex;
            align-items:center;
            gap:11px;
            margin:18px 0 14px;
        ">
            <span style="
                display:flex;
                align-items:center;
                justify-content:center;
                width:36px;
                height:36px;
                border-radius:11px;
                background:linear-gradient(135deg,#193c38,#122323);
                border:1px solid #2d6258;
                color:#62e6b5;
            ">
                {icon_html}
            </span>

            <span style="
                color:#e7f5f1;
                font-size:19px;
                font-weight:750;
            ">
                {title}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
