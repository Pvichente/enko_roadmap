import streamlit as st
import pandas as pd
import altair as alt
import urllib.parse
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="ENKO Road Map 2026", layout="wide")

# Paleta estricta por componente
COLOR_SCALE = alt.Scale(
    domain=["Alianzas", "Comunidad", "Redes Sociales", "Tecnología", "Procesos"],
    range=["#FF8C00", "#FFD700", "#4B0082", "#00CED1", "#708090"],
)

CATEGORY_ORDER = ["Alianzas", "Comunidad", "Redes Sociales", "Tecnología", "Procesos"]
MESES_STD = [
    "ENERO", "FEBRERO", "MARZO", "ABRIL",
    "MAYO", "JUNIO", "JULIO", "AGOSTO",
    "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE",
]


def inject_global_css():
    """
    Fuerza fondo blanco + grid sutil tipo roadmap ejecutivo.
    """
    st.markdown(
        """
        <style>
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
        }

        [data-testid="stAppViewContainer"] {
            background-image:
                linear-gradient(to right, rgba(0, 0, 0, 0.04) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(0, 0, 0, 0.04) 1px, transparent 1px);
            background-size: 32px 32px;
        }

        .block-container {
            background-color: #FFFFFF !important;
            padding: 1.5rem 2.5rem 2.5rem 2.5rem !important;
            max-width: 1400px !important;
        }

        .enko-card {
            background-color: #FFFFFF;
            padding: 1.8rem 2.2rem;
            border-radius: 20px;
            box-shadow: 0 18px 45px rgba(0, 0, 0, 0.12);
            border: 1px solid #E5E7EB;
        }

        h1, h2, h3, h4, p, span, label {
            font-family: -apple-system, BlinkMacSystemFont, "Inter", system-ui, sans-serif;
            color: #111827 !important;
        }

        .stAlert {
            background-color: #F9FAFB !important;
            color: #111827 !important;
            border-radius: 999px;
            border: 1px solid #E5E7EB !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# ID y pestañas de Google Sheets
# ---------------------------------------------------------
SHEET_ID = "1uyCoNM_dcVH4hFGBfsEw82n1Tr9vKHdFl6geGdMux3g"

SHEET_TABS = {
    "Alianzas": "Alianzas",
    "Comunidad": "Comunidad",
    "Redes Sociales": "Redes Sociales ",
    "Tecnología": "Tecnología",
    "Procesos": "Procesos Generales",
}


# ---------------------------------------------------------
# FUNCIÓN DE CARGA (SIN CACHÉ)
# ---------------------------------------------------------
def load_data_safe(sheet_id, tab_name_sheet, category_label):
    encoded_tab_name = urllib.parse.quote(tab_name_sheet)
    url = (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        f"/gviz/tq?tqx=out:csv&sheet={encoded_tab_name}"
    )
    
    try:
        df = pd.read_csv(url, header=1)

        if len(df.columns) < 4:
            return None, f"La pestaña '{tab_name_sheet}' tiene muy pocas columnas."

        df.rename(columns={
            df.columns[0]: 'Componente',
            df.columns[1]: 'Initiativa',
            df.columns[2]: 'Objetivo'
        }, inplace=True)

        df = df[df['Initiativa'].notna() & (df['Initiativa'] != '')]
        df.columns = df.columns.astype(str).str.strip().str.upper()

        valid_months = [m for m in MESES_STD if m in df.columns]
        if not valid_months:
            return None, f"No encontré columnas de meses en '{tab_name_sheet}'."

        df_melt = df.melt(
            id_vars=['INITIATIVA'],
            value_vars=valid_months,
            var_name='Mes',
            value_name='Status'
        )
        df_melt = df_melt[df_melt['Status'].notna()]

        if df_melt.empty:
            return None, f"La pestaña '{tab_name_sheet}' no tiene actividades marcadas."

        month_map = {m: i + 1 for i, m in enumerate(MESES_STD)}
        df_melt['MonthNum'] = df_melt['Mes'].map(month_map)
        df_melt['Start'] = df_melt['MonthNum'].apply(
            lambda m: pd.Timestamp(year=2026, month=m, day=1)
        )
        df_melt['End'] = df_melt['Start'] + pd.offsets.MonthEnd(0)
        df_melt['Category'] = category_label
        df_melt.rename(columns={'INITIATIVA': 'Initiativa'}, inplace=True)

        return df_melt, None

    except Exception as e:
        return None, f"Error en '{tab_name_sheet}': {str(e)}"


# ---------------------------------------------------------
# GANTT HIGH-FIDELITY (sin headers de categoría)
# ---------------------------------------------------------
def build_enko_gantt(master_df: pd.DataFrame) -> alt.Chart:
    df = master_df.copy()

    df["Category"] = pd.Categorical(df["Category"], CATEGORY_ORDER, ordered=True)
    df["Mes"] = pd.Categorical(df["Mes"], MESES_STD, ordered=True)

    month_ticks = [datetime(2026, i, 1) for i in range(1, 13)]

    base = (
        alt.Chart(df)
        .mark_bar(size=24, cornerRadius=999, cornerRadiusEnd=999)
        .encode(
            x=alt.X(
                "Start:T",
                title="Calendario 2026",
                axis=alt.Axis(
                    values=month_ticks,
                    format="%b",
                    labelAngle=0,
                    labelFontSize=11,
                    labelColor="#111827",
                    grid=True,
                    gridOpacity=0.25,
                    gridColor="#E5E7EB",
                ),
            ),
            x2="End:T",
            y=alt.Y(
                "Initiativa:N",
                title=None,
                axis=alt.Axis(labelLimit=0, labelFontSize=12, labelColor="#111827"),
            ),
            color=alt.Color(
                "Category:N",
                title="Componente",
                scale=COLOR_SCALE,
                legend=alt.Legend(orient="top", direction="horizontal"),
            ),
            tooltip=["Category", "Initiativa", "Mes"],
        )
        .properties(width=1050, height=alt.Step(32))
    )

    chart = (
        base.facet(
            row=alt.Row(
                "Category:N",
                header=alt.Header(labelFontSize=0, labelPadding=0),
            ),
            spacing=18,
        )
        .resolve_scale(y="independent")
        .configure_view(strokeWidth=0, fill="#FFFFFF")
        .configure(background="#FFFFFF")
        .configure_axis(labelColor="#111827", titleColor="#111827")
        .configure_legend(labelColor="#111827", titleColor="#111827")
    )

    return chart


# ---------------------------------------------------------
# APP STREAMLIT
# ---------------------------------------------------------
inject_global_css()

st.title("ENKO | Operational Road Map: 2026")
st.caption("Visualización ejecutiva de iniciativas por componente y mes.")

st.info("Cargando datos desde Google Sheets...")

dfs, errors = [], []

for label, tab_name in SHEET_TABS.items():
    df_result, error_msg = load_data_safe(SHEET_ID, tab_name, label)
    if error_msg:
        errors.append(error_msg)
    if df_result is not None:
        dfs.append(df_result)

if errors:
    with st.expander("⚠️ Detalles de errores"):
        for err in errors:
            st.warning(err)

if dfs:
    master_df = pd.concat(dfs, ignore_index=True)

    st.markdown('<div class="enko-card">', unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.subheader("Mapa Operativo 2026")
        st.markdown(
            "Cada barra representa una iniciativa activa durante el mes indicado. "
            "Los *swimlanes* agrupan las iniciativas por componente del programa ENKO."
        )
    with col_right:
        st.markdown("**Notas rápidas**")
        st.markdown("- Colores fijos por componente.")
        st.markdown("- Posiciona el cursor para ver detalles por iniciativa.")

    st.altair_chart(build_enko_gantt(master_df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("No se pudieron cargar datos. Verifica el Google Sheets.")
