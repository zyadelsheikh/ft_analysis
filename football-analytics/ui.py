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


def section(title: str):
    st.markdown(f'<div class="app-section">{title}</div>', unsafe_allow_html=True)
