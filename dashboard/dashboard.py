import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Obesity Risk Dashboard", layout="wide")

# ── Google Fonts ───────────────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

# ── Dark mode toggle (session state) ──────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True

# ── Theme tokens ───────────────────────────────────────────────────────────────
def get_theme(dark: bool) -> dict:
    if dark:
        return {
            # backgrounds
            "bg_app":       "#0f172a",
            "bg_sidebar":   "#1e293b",
            "bg_card":      "#1e293b",
            "bg_kpi":       "#1e293b",
            "bg_tab_bar":   "#0f172a",
            "bg_tab_sel":   "#1e293b",
            # borders
            "border":       "#334155",
            "border_sb":    "#334155",
            # text
            "text_primary":   "#f1f5f9",
            "text_secondary": "#94a3b8",
            "text_muted":     "#64748b",
            "text_title":     "#f8fafc",
            # hr
            "hr":           "#334155",
            # panel footer
            "footer_border": "#334155",
            # plotly
            "plot_bg":      "#1e293b",
            "paper_bg":     "#1e293b",
            "grid_color":   "#334155",
            "line_color":   "#475569",
            "tick_color":   "#64748b",
            "axis_title":   "#94a3b8",
            # disclaimer dark
            "disc_bg":      "#1c1a09",
            "disc_border":  "#78350f",
            "disc_left":    "#f59e0b",
            "disc_text":    "#fcd34d",
        }
    else:
        return {
            "bg_app":       "#f8fafc",
            "bg_sidebar":   "#ffffff",
            "bg_card":      "#ffffff",
            "bg_kpi":       "#ffffff",
            "bg_tab_bar":   "#f1f5f9",
            "bg_tab_sel":   "#ffffff",
            "border":       "#e2e8f0",
            "border_sb":    "#e2e8f0",
            "text_primary":   "#1e293b",
            "text_secondary": "#64748b",
            "text_muted":     "#94a3b8",
            "text_title":     "#0f172a",
            "hr":           "#e2e8f0",
            "footer_border": "#f1f5f9",
            "plot_bg":      "#ffffff",
            "paper_bg":     "#ffffff",
            "grid_color":   "#f1f5f9",
            "line_color":   "#e2e8f0",
            "tick_color":   "#94a3b8",
            "axis_title":   "#64748b",
            "disc_bg":      "#fffbeb",
            "disc_border":  "#fde68a",
            "disc_left":    "#f59e0b",
            "disc_text":    "#78350f",
        }

dark = st.session_state["dark_mode"]
T    = get_theme(dark)

# ── Dynamic CSS injection ──────────────────────────────────────────────────────
st.markdown(f"""
<style>
html, body, [class*="css"], .stApp {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: {T['bg_app']} !important;
    color: {T['text_primary']};
}}
.block-container {{
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 100% !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}
[data-testid="collapsedControl"] {{
    display: none !important;
}}
section[data-testid="stSidebar"][aria-expanded="false"] {{
    display: block !important;
    width: 270px !important;
}}
/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {T['bg_sidebar']} !important;
    border-right: 1px solid {T['border_sb']} !important;
    min-width: 270px !important;
    max-width: 270px !important;
}}
[data-testid="stSidebar"] * {{
    color: {T['text_primary']} !important;
}}
[data-testid="stSidebar"] .stCaption {{
    color: {T['text_muted']} !important;
}}

/* Multiselect tags coral */
[data-testid="stSidebar"] span[data-baseweb="tag"] {{
    background-color: #f87171 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
}}
/* Multiselect dropdown bg */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: {T['bg_card']} !important;
    border-color: {T['border']} !important;
}}

/* Slider coral */
[data-testid="stSidebar"] div[data-testid="stSlider"] div div div {{
    background-color: #f87171 !important;
}}
[data-testid="stSidebar"] div[data-testid="stSlider"] div[role="slider"] {{
    background-color: #f87171 !important;
    border-color: #f87171 !important;
}}

/* Sidebar toggle button */
[data-testid="stSidebar"] .stButton button {{
    background-color: {'#334155' if dark else '#f1f5f9'} !important;
    color: {T['text_primary']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}}
[data-testid="stSidebar"] .stButton button:hover {{
    background-color: {'#475569' if dark else '#e2e8f0'} !important;
}}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    gap: 4px;
    background: {T['bg_tab_bar']};
    border-radius: 10px;
    padding: 4px;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    color: {T['text_secondary']};
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    background: {T['bg_tab_sel']} !important;
    color: {T['text_title']} !important;
    box-shadow: 0 1px 3px rgba(0,0,0,{'0.25' if dark else '0.08'});
}}

/* ── HR ── */
hr {{ border-color: {T['hr']} !important; margin: 1rem 0 !important; }}

/* ── Streamlit warnings/info in dark ── */
[data-testid="stAlert"] {{
    background-color: {T['bg_card']} !important;
    border-color: {T['border']} !important;
    color: {T['text_primary']} !important;
}}

/* ── Selectbox & checkbox in main area dark ── */
div[data-baseweb="select"] > div {{
    background-color: {T['bg_card']} !important;
    border-color: {T['border']} !important;
    color: {T['text_primary']} !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
CAT_ORDER = [
    "Insufficient_Weight", "Normal_Weight", "Overweight_Level_I",
    "Overweight_Level_II", "Obesity_Type_I", "Obesity_Type_II", "Obesity_Type_III",
]
CAT_LABEL = {
    "Insufficient_Weight": "Insuf. Weight",
    "Normal_Weight":       "Normal Weight",
    "Overweight_Level_I":  "Overweight I",
    "Overweight_Level_II": "Overweight II",
    "Obesity_Type_I":      "Obesity I",
    "Obesity_Type_II":     "Obesity II",
    "Obesity_Type_III":    "Obesity III",
}
CAT_COLOR = {
    "Insufficient_Weight": "#60a5fa",
    "Normal_Weight":       "#34d399",
    "Overweight_Level_I":  "#86efac",
    "Overweight_Level_II": "#fbbf24",
    "Obesity_Type_I":      "#fb923c",
    "Obesity_Type_II":     "#f87171",
    "Obesity_Type_III":    "#ef4444",
}
OBESE_CATS = ["Obesity_Type_I", "Obesity_Type_II", "Obesity_Type_III"]

VAR_LABEL = {
    "FAF":    "Physical Activity Frequency",
    "CH2O":   "Daily Water Intake",
    "FCVC":   "Vegetable Consumption",
    "NCP":    "Number of Main Meals",
    "TUE":    "Technology Usage Time",
    "BMI":    "BMI",
    "Age":    "Age",
    "Weight": "Weight",
    "FAVC":   "High Caloric Food Consumption",
    "CAEC":   "Eating Between Meals",
    "CALC":   "Alcohol Consumption Frequency",
    "SMOKE":  "Smoking Status",
    "SCC":    "Calorie Monitoring",
    "MTRANS": "Transportation Mode",
}

# ── Plotly base & axis helper (theme-aware) ────────────────────────────────────
def chart_base():
    return dict(
        font_family="Plus Jakarta Sans",
        font_color=T["text_primary"],
        plot_bgcolor=T["plot_bg"],
        paper_bgcolor=T["paper_bg"],
        hoverlabel=dict(
            bgcolor=T["bg_card"],
            bordercolor=T["border"],
            font_size=12,
            font_color=T["text_primary"],
        ),
    )

def ax_style(grid=True):
    return dict(
        showgrid=grid,
        gridcolor=T["grid_color"],
        linecolor=T["line_color"],
        zeroline=False,
        tickfont=dict(size=11, color=T["tick_color"]),
        title_font=dict(size=11, color=T["axis_title"]),
    )

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("obesity_processed.csv")
    df["NObeyesdad"] = pd.Categorical(df["NObeyesdad"], categories=CAT_ORDER, ordered=True)
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 18, 24, 34, 44, 54, 64, 200],
        labels=["< 18", "18–24", "25–34", "35–44", "45–54", "55–64", "65+"],
    )
    return df

df_raw = load_data()
age_min, age_max = int(df_raw["Age"].min()), int(df_raw["Age"].max())

# ── Session state defaults ─────────────────────────────────────────────────────
FILTER_DEFAULTS = {
    "sel_cat": CAT_ORDER,
    "sel_age": (age_min, age_max),
    "sel_fam": ["yes", "no"],
}
for k, v in FILTER_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand header
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:1.2rem 1rem 1rem 1rem;
                border-bottom:1px solid {T['border_sb']};margin-bottom:0.8rem;">
        <div style="font-size:1rem;font-weight:700;color:{T['text_title']};line-height:1.3;">
            Obesity Risk<br>Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dark mode toggle
    toggle_label = "Light Mode" if dark else "Dark Mode"
    if st.button(toggle_label, use_container_width=True, key="toggle_dark"):
        st.session_state["dark_mode"] = not dark
        st.rerun()

    st.divider()

    # Filters
    st.markdown(f'<p style="font-size:0.7rem;font-weight:700;color:{T["text_muted"]};text-transform:uppercase;letter-spacing:0.08em;margin:0 0 0.5rem 0.2rem;">Filter Global</p>', unsafe_allow_html=True)

    if st.button("Reset semua filter", use_container_width=True, key="btn_reset"):
        for k, v in FILTER_DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()

    sel_cat = st.multiselect(
        "Kategori", options=CAT_ORDER, key="sel_cat",
        format_func=lambda x: CAT_LABEL[x],
    )
    sel_age = st.slider("Rentang Usia", age_min, age_max, key="sel_age")
    sel_fam = st.multiselect(
        "Riwayat Keluarga", options=["yes", "no"], key="sel_fam",
        format_func=lambda x: "Ada riwayat" if x == "yes" else "Tidak ada",
    )
    st.caption("Filter berlaku untuk semua panel.")

# ── Apply filters ──────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["NObeyesdad"].isin(sel_cat) &
    df_raw["Age"].between(sel_age[0], sel_age[1]) &
    df_raw["family_history_with_overweight"].isin(sel_fam)
].copy()

SMALL_TOTAL = 30
SMALL_CAT   = 10

if len(df) == 0:
    st.error("❌ Tidak ada data yang sesuai filter. Ubah filter untuk melanjutkan.")
    st.stop()
elif len(df) < SMALL_TOTAL:
    st.error(f"❌ Filter terlalu ketat — hanya tersisa **{len(df)} baris**. Perlonggar filter.")
    st.stop()
else:
    cat_counts = df["NObeyesdad"].value_counts()
    small_cats = cat_counts[cat_counts < SMALL_CAT]
    if not small_cats.empty:
        names = ", ".join([CAT_LABEL.get(c, c) for c in small_cats.index])
        st.warning(f"⚠️ Kategori sampel kecil (< {SMALL_CAT}): **{names}**. Interpretasi perlu hati-hati.")

# ── Computed KPI values ────────────────────────────────────────────────────────
n       = len(df)
n_high  = int(df["NObeyesdad"].isin(OBESE_CATS).sum())
n_low   = n - n_high
pct_h   = (n_high / n) * 100
pct_l   = (n_low  / n) * 100
avg_age = df["Age"].mean()
avg_bmi = df["BMI"].mean()
now_str = datetime.now().strftime("%b %d, %Y  •  %H:%M")

# ── Welcome header ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.2rem;">
  <div>
    <div style="font-size:1.85rem;font-weight:800;color:{T['text_title']};margin:0 0 4px 0;">
      Obesity Risk Dashboard
    </div>
  </div>
  <div style="font-size:0.75rem;color:{T['text_muted']};text-align:right;">
    Last updated<br><strong>{now_str}</strong>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:{T['disc_bg']};border:1px solid {T['disc_border']};
            border-left:4px solid {T['disc_left']};border-radius:8px;
            padding:0.65rem 1rem;font-size:0.76rem;color:{T['disc_text']};margin-bottom:1.4rem;">
  ⚠️ <strong>Catatan Dataset:</strong> Sebagian besar data di-<em>generate</em> secara sintetis
  dan berasal dari populasi di Mexico, Peru &amp; Kolombia.
</div>
""", unsafe_allow_html=True)

# ── KPI cards ─────────────────────────────────────────────────────────────────
card_shadow = "0 1px 8px rgba(0,0,0,0.25)" if dark else "0 1px 3px rgba(0,0,0,0.04)"
st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:1.6rem;">
  <div style="background:{T['bg_kpi']};border:1px solid {T['border']};border-radius:12px;
              padding:1.1rem 1.2rem;box-shadow:{card_shadow};">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.55rem;">
      <div style="width:36px;height:36px;border-radius:8px;background:#eff6ff;
                  display:flex;align-items:center;justify-content:center;font-size:1.1rem;">🗄️</div>
      <div style="font-size:0.72rem;font-weight:600;color:{T['text_secondary']};">Jumlah Data</div>
    </div>
    <div style="font-size:1.75rem;font-weight:800;color:{T['text_title']};margin-bottom:4px;">{n:,}</div>
    <div style="font-size:0.72rem;font-weight:600;color:#2563eb;">data</div>
  </div>
  <div style="background:{T['bg_kpi']};border:1px solid {T['border']};border-radius:12px;
              padding:1.1rem 1.2rem;box-shadow:{card_shadow};">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.55rem;">
      <div style="width:36px;height:36px;border-radius:8px;background:#fef2f2;
                  display:flex;align-items:center;justify-content:center;font-size:1.1rem;">⚠️</div>
      <div style="font-size:0.72rem;font-weight:600;color:{T['text_secondary']};">Risiko Obesitas (High)</div>
    </div>
    <div style="font-size:1.75rem;font-weight:800;color:{T['text_title']};margin-bottom:4px;">{n_high:,}</div>
    <div style="font-size:0.72rem;font-weight:600;color:#ef4444;">{pct_h:.1f}% dari total</div>
  </div>
  <div style="background:{T['bg_kpi']};border:1px solid {T['border']};border-radius:12px;
              padding:1.1rem 1.2rem;box-shadow:{card_shadow};">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.55rem;">
      <div style="width:36px;height:36px;border-radius:8px;background:#f0fdf4;
                  display:flex;align-items:center;justify-content:center;font-size:1.1rem;">🛡️</div>
      <div style="font-size:0.72rem;font-weight:600;color:{T['text_secondary']};">Risiko Obesitas (Low)</div>
    </div>
    <div style="font-size:1.75rem;font-weight:800;color:{T['text_title']};margin-bottom:4px;">{n_low:,}</div>
    <div style="font-size:0.72rem;font-weight:600;color:#16a34a;">{pct_l:.1f}%  dari total</div>
  </div>
  <div style="background:{T['bg_kpi']};border:1px solid {T['border']};border-radius:12px;
              padding:1.1rem 1.2rem;box-shadow:{card_shadow};">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.55rem;">
      <div style="width:36px;height:36px;border-radius:8px;background:#faf5ff;
                  display:flex;align-items:center;justify-content:center;font-size:1.1rem;">👤</div>
      <div style="font-size:0.72rem;font-weight:600;color:{T['text_secondary']};">Rata-rata Usia</div>
    </div>
    <div style="font-size:1.75rem;font-weight:800;color:{T['text_title']};margin-bottom:4px;">{avg_age:.1f}</div>
    <div style="font-size:0.72rem;font-weight:600;color:#7c3aed;">Tahun</div>
  </div>
  <div style="background:{T['bg_kpi']};border:1px solid {T['border']};border-radius:12px;
              padding:1.1rem 1.2rem;box-shadow:{card_shadow};">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.55rem;">
      <div style="width:36px;height:36px;border-radius:8px;background:#fffbeb;
                  display:flex;align-items:center;justify-content:center;font-size:1.1rem;">📋</div>
      <div style="font-size:0.72rem;font-weight:600;color:{T['text_secondary']};">Rata-rata BMI</div>
    </div>
    <div style="font-size:1.75rem;font-weight:800;color:{T['text_title']};margin-bottom:4px;">{avg_bmi:.1f}</div>
    <div style="font-size:0.72rem;font-weight:600;color:#d97706;">kg/m²</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Helper ─────────────────────────────────────────────────────────────────────
def cat_labels_ordered():
    return [CAT_LABEL[c] for c in CAT_ORDER if c in df["NObeyesdad"].unique()]

def card_open(title, subtitle=""):
    sub_html = f'<div style="font-size:0.78rem;color:{T["text_muted"]};margin-bottom:0.6rem;">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="background:{T['bg_card']};border:1px solid {T['border']};border-radius:14px;
                padding:1.3rem 1.4rem 1rem 1.4rem;box-shadow:{card_shadow};margin-bottom:1.2rem;">
      <div style="font-size:0.95rem;font-weight:700;color:{T['text_title']};margin-bottom:2px;">{title}</div>
      {sub_html}
    """

def card_close(note=""):
    note_html = f'<div style="font-size:11px;color:{T["text_muted"]};margin-top:6px;border-top:1px solid {T["border"]};padding-top:5px;">{note}</div>' if note else ""
    return note_html + "</div>"

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_a, tab_b, tab_c = st.tabs([
    "|      Panel 1 : Distribusi Populasi",
    "|      Panel 2 : Profil Perilaku",
    "|      Panel 3 : Pola Hubungan Variabel",
])

# ══════════════════════════════════════════════════════════════════════════════
# PANEL A
# ══════════════════════════════════════════════════════════════════════════════
with tab_a:

    # ── Row 1: Bar distribusi + stacked riwayat keluarga ─────────────────────
    col_a1, col_a2 = st.columns([2, 1])

    with col_a1:
        st.markdown(card_open("Distribusi Kategori Berat Badan",
                              "Horizontal bar chart kategori berat badan."),
                    unsafe_allow_html=True)
        counts = (
            df.groupby("NObeyesdad", observed=True).size()
            .reset_index(name="count").sort_values("NObeyesdad")
        )
        counts["label"] = counts["NObeyesdad"].map(CAT_LABEL)
        counts["color"] = counts["NObeyesdad"].map(CAT_COLOR)

        fig_a1 = go.Figure(go.Bar(
            y=counts["label"], x=counts["count"], orientation="h",
            marker_color=counts["color"],
            text=counts["count"], textposition="outside",
            textfont=dict(color=T["text_primary"]),
            hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
        ))
        fig_a1.update_layout(
            **chart_base(),
            xaxis=dict(title="Jumlah Individu", **ax_style()),
            yaxis=dict(categoryorder="array", categoryarray=counts["label"].tolist(), **ax_style(False)),
            height=360, margin=dict(l=10, r=60, t=10, b=40),
        )
        st.plotly_chart(fig_a1, use_container_width=True, config={"displayModeBar": False})
        st.markdown(card_close("insight : Distribusi relatif seimbang, tidak terdapat kategori yang sangat dominan"),
                    unsafe_allow_html=True)

    with col_a2:
        st.markdown(card_open("Riwayat Keluarga per Kategori",
                              "Proporsi ada/tidak riwayat keluarga overweight per kategori."),
                    unsafe_allow_html=True)
        fam = (
            df.groupby(["NObeyesdad", "family_history_with_overweight"], observed=True)
            .size().reset_index(name="count")
        )
        totals = fam.groupby("NObeyesdad", observed=True)["count"].transform("sum")
        fam["pct"]   = fam["count"] / totals * 100
        fam["label"] = fam["NObeyesdad"].map(CAT_LABEL)
        fam = fam.sort_values("NObeyesdad")

        fig_a2 = go.Figure()
        for val, color, name in [("yes", "#3b82f6", "Ada riwayat"), ("no", "#bfdbfe", "Tidak ada")]:
            sub = fam[fam["family_history_with_overweight"] == val]
            fig_a2.add_trace(go.Bar(
                name=name, x=sub["label"], y=sub["pct"], marker_color=color,
                hovertemplate=f"<b>%{{x}}</b><br>{name}: %{{y:.1f}}%<extra></extra>",
            ))
        fig_a2.update_layout(
            **chart_base(),
            barmode="stack",
            xaxis=dict(categoryorder="array", categoryarray=cat_labels_ordered(), tickangle=-30, **ax_style(False)),
            yaxis=dict(title="Proporsi (%)", **ax_style()),
            height=360, margin=dict(l=10, r=10, t=10, b=60),
            legend=dict(orientation="h", y=-0.28, font=dict(color=T["text_primary"])),
        )
        st.plotly_chart(fig_a2, use_container_width=True, config={"displayModeBar": False})
        st.markdown(card_close("insight : Kategori berat badan lebih tinggi cenderung memiliki proporsi riwayat keluarga overweight yang lebih besar"),
                    unsafe_allow_html=True)

    st.divider()


    col_a3, col_a4 = st.columns([1, 1.6])

    with col_a3:
        st.markdown(card_open("Distribusi Risiko Obesitas",
                              "High Risk = Obesity I / II / III · Low Risk = sisanya"),
                    unsafe_allow_html=True)
        fig_donut = go.Figure(go.Pie(
            values=[n_high, n_low], labels=["High Risk", "Low Risk"], hole=0.62,
            marker=dict(colors=["#f87171", "#4ade80"], line=dict(color=T["bg_card"], width=2)),
            textinfo="none",
        ))
        fig_donut.update_layout(
            **chart_base(),
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(orientation="h", y=-0.12, font=dict(color=T["text_primary"])),
            annotations=[dict(
                text=f"<b>{n:,}</b><br>Total",
                x=0.5, y=0.5, font_size=15, showarrow=False,
                font=dict(color=T["text_title"]),
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
        st.markdown(card_close(f"insight : {pct_h:.1f}% populasi termasuk kategori risiko tinggi obesitas"),
                    unsafe_allow_html=True)

    with col_a4:
        st.markdown(card_open("Distribusi Risiko Obesitas per Kelompok Usia",
                              "Komposisi High/Low Risk per kelompok usia."),
                    unsafe_allow_html=True)
        age_risk = df.copy()
        age_risk["Risk"] = np.where(age_risk["NObeyesdad"].isin(OBESE_CATS), "High Risk", "Low Risk")
        age_grp = age_risk.groupby(["AgeGroup", "Risk"], observed=True).size().reset_index(name="count")

        fig_age_grp = go.Figure()
        for risk, color in [("High Risk", "#f87171"), ("Low Risk", "#4ade80")]:
            sub = age_grp[age_grp["Risk"] == risk]
            fig_age_grp.add_trace(go.Bar(
                name=risk, x=sub["AgeGroup"].astype(str), y=sub["count"],
                marker_color=color,
                hovertemplate=f"<b>%{{x}}</b><br>{risk}: %{{y}}<extra></extra>",
            ))
        fig_age_grp.update_layout(
            **chart_base(),
            barmode="stack",
            height=280, margin=dict(l=12, r=12, t=10, b=35),
            xaxis=dict(title="Kelompok Usia", **ax_style(False)),
            yaxis=dict(title="Jumlah", **ax_style()),
            legend=dict(orientation="h", y=-0.22, font=dict(color=T["text_primary"])),
        )
        st.plotly_chart(fig_age_grp, use_container_width=True, config={"displayModeBar": False})
        st.markdown(card_close("insight : Kelompok usia 18–34 mendominasi populasi dataset"),
                    unsafe_allow_html=True)

    # ── Row 3: Gender donut + grouped bar breakdown ───────────────────────────
    col_a5= st.columns(1)


    st.markdown(card_open("Distribusi Risiko Obesitas berdasarkan Jenis Kelamin",
                          "Distribusi gender dalam populasi terfilter."),
                unsafe_allow_html=True)
    g_counts = df["Gender"].value_counts().reset_index()
    g_counts.columns = ["Gender", "count"]
    g_counts = g_counts.set_index("Gender").reindex(["Female", "Male"]).reset_index()  # ← paksa urutan

    total_gender = g_counts["count"].sum()

    fig_gender = go.Figure(go.Pie(
        values=g_counts["count"], labels=g_counts["Gender"], hole=0.62,
        marker=dict(colors=["#f9a8d4", "#93c5fd"], line=dict(color=T["bg_card"], width=2)),
        textinfo="none",
    ))
    fig_gender.update_layout(
        **chart_base(),
        height=260, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(orientation="h", y=-0.12, font=dict(color=T["text_primary"])),
        annotations=[dict(
            text=f"<b>{total_gender:,}</b><br>Total",
            x=0.5, y=0.5, font_size=15, showarrow=False,
            font=dict(color=T["text_title"]),
        )],
    )
    st.plotly_chart(fig_gender, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# PANEL B
# ══════════════════════════════════════════════════════════════════════════════
with tab_b:
    # B1 — Heatmap
    st.markdown(card_open(
        "Heatmap Profil Perilaku per Kategori",
        "Nilai rata-rata. Warna gelap = relatif tinggi, warna terang = relatif rendah."
    ), unsafe_allow_html=True)

    heatmap_vars   = ["FAF", "CH2O", "FCVC", "NCP"]
    heatmap_labels = [VAR_LABEL[v] for v in heatmap_vars]

    hm_means = df.groupby("NObeyesdad", observed=True)[heatmap_vars].mean()
    hm_norm  = (hm_means - hm_means.min()) / (hm_means.max() - hm_means.min())
    cats_present  = [c for c in CAT_ORDER if c in hm_norm.index]
    hm_norm       = hm_norm.loc[cats_present]
    hm_means      = hm_means.loc[cats_present]
    cat_labels_hm = [CAT_LABEL[c] for c in cats_present]
    annotations   = [[f"{hm_means.loc[cat, v]:.2f}" for v in heatmap_vars] for cat in cats_present]

    fig_hm = go.Figure(go.Heatmap(
        z=hm_means.values.tolist(), x=heatmap_labels, y=cat_labels_hm,
        text=annotations, texttemplate="%{text}",
        textfont=dict(size=12, color="white"),
        colorscale="Reds", showscale=True,
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.2f}<extra></extra>",
    ))
    fig_hm.update_layout(
        **chart_base(),
        xaxis=dict(side="top", tickfont=dict(size=12, color=T["tick_color"])),
        yaxis=dict(
            categoryorder="array",
            categoryarray=list(reversed(cat_labels_hm)),
            tickfont=dict(size=12, color=T["tick_color"]),
        ),
        height=360, margin=dict(l=10, r=80, t=60, b=10),
    )
    st.plotly_chart(fig_hm, use_container_width=True, config={"displayModeBar": False})
    st.markdown(card_close(
        "insight: Aktivitas fisik konsisten menurun dengan meningkatnya kategori berat badan."
        " Sementara itu, konsumsi air dan sayur relatif lebih tinggi pada kategori berat badan tinggi."
    ), unsafe_allow_html=True)

    st.divider()

    # B2 — Violin usia
    st.markdown(card_open(
        "Distribusi Usia per Kategori Berat Badan",
        "Lebar kurva mencerminkan kepadatan populasi di rentang usia tersebut."
    ), unsafe_allow_html=True)

    fig_viol = go.Figure()
    for cat in CAT_ORDER:
        if cat not in df["NObeyesdad"].unique():
            continue
        sub = df[df["NObeyesdad"] == cat]["Age"]
        fig_viol.add_trace(go.Violin(
            x=sub, name=CAT_LABEL[cat],
            line_color=CAT_COLOR[cat], fillcolor=CAT_COLOR[cat],
            opacity=0.6, orientation="h", side="positive", width=1.8,
            points=False, meanline=dict(visible=True, color="white", width=1.5),
            hovertemplate=f"<b>{CAT_LABEL[cat]}</b><br>Age: %{{x:.1f}}<extra></extra>",
        ))
    fig_viol.update_layout(
        **chart_base(),
        xaxis=dict(title="Usia", **ax_style()),
        yaxis=dict(
            categoryorder="array",
            categoryarray=[CAT_LABEL[c] for c in reversed(CAT_ORDER) if c in df["NObeyesdad"].unique()],
            **ax_style(False),
        ),
        height=420, margin=dict(l=10, r=20, t=10, b=50),
        showlegend=False, violingap=0.3, violingroupgap=0.1,
    )
    st.plotly_chart(fig_viol, use_container_width=True, config={"displayModeBar": False})
    st.markdown(card_close(
        "insight: Insuf. Weight terkonsentrasi dibawah usia 20, sementara overweight I hingga obeseity III cenderung terkonsentrasi pada usia 20 - 30"
    ), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL C
# ══════════════════════════════════════════════════════════════════════════════
with tab_c:
    col_c1, col_c2 = st.columns([3, 2])

    with col_c1:
        st.markdown(card_open(
            "Scatter Plot Antar Variabel",
            "Menampilkan hubungan antar variabel dengan opsi jitter untuk mengurangi overlap titik data."
        ), unsafe_allow_html=True)

        SCATTER_VARS = {
            "Physical Activity Frequency": "FAF",
            "Daily Water Intake":          "CH2O",
            "Vegetable Consumption":       "FCVC",
            "Technology Usage Time":       "TUE",
            "BMI":                         "BMI",
            "Age":                         "Age",
        }
        SCATTER_VARS_Y = {"Number of Main Meals": "NCP", **SCATTER_VARS}

        cx, cy, cj = st.columns(3)
        x_label = cx.selectbox("Sumbu X", list(SCATTER_VARS.keys()),   index=0)
        y_label = cy.selectbox("Sumbu Y", list(SCATTER_VARS_Y.keys()), index=0)
        jitter  = cj.slider("Jitter", 0.0, 0.3, 0.05, 0.01)

        x_ax, y_ax = SCATTER_VARS[x_label], SCATTER_VARS_Y[y_label]
        plot_df = df.copy()
        if jitter > 0:
            rng = np.random.default_rng(42)
            plot_df[x_ax] = plot_df[x_ax] + rng.uniform(-jitter, jitter, len(plot_df))
            plot_df[y_ax] = plot_df[y_ax] + rng.uniform(-jitter, jitter, len(plot_df))
        plot_df["label"] = plot_df["NObeyesdad"].map(CAT_LABEL)

        fig_c1 = px.scatter(
            plot_df, x=x_ax, y=y_ax, color="label",
            color_discrete_map={v: CAT_COLOR[k] for k, v in CAT_LABEL.items()},
            category_orders={"label": [CAT_LABEL[c] for c in CAT_ORDER]},
            opacity=0.55, hover_data={"Age": True, "BMI": True},
            labels={x_ax: x_label, y_ax: y_label}, height=400,
        )
        if x_ax == "FAF" and y_ax == "NCP":
            fig_c1.add_shape(
                type="rect",
                x0=df["FAF"].min(), x1=1.0, y0=3.0, y1=df["NCP"].max(),
                fillcolor="rgba(250,100,70,0.08)",
                line=dict(color="rgba(200,70,40,0.3)", dash="dot"),
            )
            fig_c1.add_annotation(
                x=0.5, y=df["NCP"].max() - 0.1,
                text="Zona Risiko", showarrow=False,
                font=dict(size=11, color="#993C1D"),
            )
        fig_c1.update_layout(
            **chart_base(),
            xaxis=dict(**ax_style()), yaxis=dict(**ax_style()),
            margin=dict(l=10, r=10, t=10, b=40),
            legend=dict(
            title="Kategori",
            title_font=dict(color=T["text_title"], size=12),
            font=dict(color=T["text_primary"]),
        ),
        )
        st.plotly_chart(fig_c1, use_container_width=True, config={"displayModeBar": False})
        
    with col_c2:
        st.markdown(card_open(
            "Distribusi Variabel per Kategori (Box Plot)",
            "Median, IQR, dan outlier per kategori."
        ), unsafe_allow_html=True)

        BOX_VARS = {
            "Age":                         "Age",
            "BMI":                         "BMI",
            "Physical Activity Frequency": "FAF",
            "Daily Water Intake":          "CH2O",
            "Vegetable Consumption":       "FCVC",
            "Number of Main Meals":        "NCP",
            "Technology Usage Time":       "TUE",
            "Weight":                      "Weight",
        }

        bv, bp = st.columns(2)
        y_label_box = bv.selectbox("Variabel", list(BOX_VARS.keys()), index=0)
        show_pts    = bp.checkbox("Tampilkan titik", value=False)

        y_var = BOX_VARS[y_label_box]
        fig_c2 = go.Figure()
        for cat in CAT_ORDER:
            if cat not in df["NObeyesdad"].unique():
                continue
            sub = df[df["NObeyesdad"] == cat]
            fig_c2.add_trace(go.Box(
                y=sub[y_var], name=CAT_LABEL[cat],
                marker_color=CAT_COLOR[cat], fillcolor=CAT_COLOR[cat],
                opacity=0.75, boxpoints="all" if show_pts else False,
                jitter=0.3, line_width=1.5,
                hovertemplate=f"<b>{CAT_LABEL[cat]}</b><br>{y_label_box}: %{{y:.2f}}<extra></extra>",
            ))
        fig_c2.update_layout(
            **chart_base(),
            showlegend=False,
            yaxis=dict(title=y_label_box, **ax_style()),
            xaxis=dict(
                categoryorder="array", categoryarray=cat_labels_ordered(),
                tickangle=-30, **ax_style(False),
            ),
            height=400, margin=dict(l=10, r=10, t=10, b=70),
        )
        st.plotly_chart(fig_c2, use_container_width=True, config={"displayModeBar": False})
        
# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"<hr style='border-color:{T['hr']};margin:1rem 0;'>", unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center;font-size:0.75rem;color:{T["text_muted"]};padding-bottom:1rem;">Obesity Risk Analytics Dashboard • Built with Streamlit & Plotly</div>', unsafe_allow_html=True)