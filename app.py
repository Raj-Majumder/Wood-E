import streamlit as st
import json
import os
import woody_engine as engine

# 1. Page Configuration Setups
st.set_page_config(page_title="Wood-E Pro Dashboard", page_icon="🪵", layout="wide")

# Custom Professional Premium Dark Theme styling overrides
st.markdown("""
    <style>
        .stApp { background-color: #0f1115 !important; color: #f4f5f6 !important; }
        .metric-card {
            background-color: #161a22; border: 1px solid #2d3139; border-radius: 8px;
            padding: 22px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); margin-bottom: 18px;
        }
        .metric-value { font-size: 32px; font-weight: 700; color: #2a9d8f; }
        .metric-label { font-size: 14px; color: #8d99ae; text-transform: uppercase; letter-spacing: 0.75px; margin-bottom: 6px; }
        .large-subtext { font-size: 16px !important; line-height: 1.6 !important; color: #c9d1d9 !important; }
        .stTabs [data-baseweb="tab"] { font-size: 16px !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Dynamic Database Initializations
@st.cache_data
def load_timber_database():
    with open("wood_species_db.json", "r") as f:
        return json.load(f)

species_db = load_timber_database()

# 3. Sidebar Layout
st.sidebar.markdown("### 🌐 System Preferences")
unit_system = st.sidebar.radio("Measurement System", options=["Imperial (Inches/Lbs)", "Metric (mm/Kgs)"])
is_metric = unit_system == "Metric (mm/Kgs)"
u_length = "mm" if is_metric else "inches"
u_weight = "Kgs" if is_metric else "lbs"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🪵 Active Material Profile")
species_key = st.sidebar.selectbox("Select Timber Species", options=list(species_db.keys()), format_func=lambda x: species_db[x]["common_name"])
wood = species_db[species_key]

st.sidebar.metric("Elasticity (MOE)", f"{wood['modulus_of_elasticity_psi']:,} PSI")
st.sidebar.metric("Janka Hardness", f"{wood['janka_hardness_lbf']:,} lbf")

st.title("Wood-E // Industrial Calculation Matrix")
st.caption(f"Optimizing calculations against structural components of **{wood['common_name']}**")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat with Wood-E", "📐 Structural Deflection", 
    "🪵 Volume & Costing", "🪚 Joinery Trigonometry", "💨 Environmental Physics"
])

with tab1:
    st.markdown("### 💬 Ask Wood-E Your Shop Questions")
    st.markdown("<p class='large-subtext'>Wood-E parses messy natural language prompts, automatically extracts your project dimensions, and runs them against exact mathematical backend functions.</p>", unsafe_allow_html=True)
    st.caption("Examples: 'How many board feet is 10 planks of walnut 1.16\"x10\"x48\" at 14/bf?'")
    
    import woody_agent
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What calculation can I handle for you today?", key="chat_input_bar"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant", avatar="🪵"):
            response_text = woody_agent.chat_with_woody(prompt)
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()


with tab2:
    st.markdown("### Shelf Deflection Analysis")
    st.markdown("<p class='large-subtext'><strong>Method:</strong> Euler-Bernoulli Beam Stress Matrix.<br><strong>Required Measurements:</strong> Span width, thickness, depth profile, and load weight constraints.</p>", unsafe_allow_html=True)
    st.markdown("---")
    col1, space, col2 = st.columns([1.2, 0.1, 1.5])
    with col1:
        load_input = st.number_input(f"Total Distributed Load ({u_weight})", min_value=1.0, value=50.0 if not is_metric else 22.0, key="shelf_load")
        span_input = st.number_input(f"Shelf Total Span ({u_length})", min_value=1.0, value=36.0 if not is_metric else 900.0, key="shelf_span")
        thick_input = st.number_input(f"Core Board Thickness ({u_length})", min_value=0.1, value=0.75 if not is_metric else 19.0, key="shelf_thick")
        depth_input = st.number_input(f"Shelf Profile Depth ({u_length})", min_value=1.0, value=10.0 if not is_metric else 250.0, key="shelf_depth")
        load_type = st.checkbox("Uniformly Distributed Load?", value=True, key="shelf_type")
        load_lbs = engine.kgs_to_lbs(load_input) if is_metric else load_input
        span_in = engine.mm_to_inches(span_input) if is_metric else span_input
        thick_in = engine.mm_to_inches(thick_input) if is_metric else thick_input
        depth_in = engine.mm_to_inches(depth_input) if is_metric else depth_input
    with col2:
        deflection_in = engine.calculate_shelf_deflection(load_lbs, span_in, thick_in, depth_in, wood["modulus_of_elasticity_psi"], load_type)
        deflection_display = engine.inches_to_mm(deflection_in) if is_metric else deflection_in
        u_disp = "mm" if is_metric else "inches"
        if deflection_display <= (0.5 if is_metric else 0.02):
            st.success(f"✔️ **Deflection: {deflection_display:.4f} {u_disp}**\n\nStructural thresholds completely safe.")
        elif deflection_display <= (1.2 if is_metric else 0.05):
            st.warning(f"⚠️ **Deflection: {deflection_display:.4f} {u_disp}**\n\nBorderline limits. Sag will be visible.")
        else:
            st.error(f"❌ **Deflection: {deflection_display:.4f} {u_disp}**\n\nCritical structural sag failure limits!")

with tab3:
    st.markdown("### Volumetric Material Volume & Cost Estimator")
    st.markdown("<p class='large-subtext'><strong>Method:</strong> Linear Volumetric Lumber Conversion Metric.<br><strong>Required Measurements:</strong> Part quantity count, thickness, width, length dimensions, and lumber cost rate variables.</p>", unsafe_allow_html=True)
    st.markdown("---")
    col_v1, col_v2 = st.columns([1.5, 1.2])
    with col_v1:
        c1, c2, c3, c4 = st.columns(4)
        pieces = c1.number_input("Part Qty", min_value=1, value=1, key="vol_p")
        t_raw = c2.number_input(f"Thickness ({u_length})", min_value=0.1, value=1.0 if not is_metric else 25.0, key="vol_t")
        w_raw = c3.number_input(f"Width ({u_length})", min_value=0.1, value=6.0 if not is_metric else 150.0, key="vol_w")
        l_raw = c4.number_input(f"Length ({u_length})", min_value=1.0, value=96.0 if not is_metric else 2400.0, key="vol_l")
        cost_basis = st.number_input("Lumber Cost Rate (US$ per Board Foot)", min_value=0.0, value=6.50, step=0.25, key="vol_c")
        bf_total = engine.calculate_board_feet(pieces, engine.mm_to_inches(t_raw) if is_metric else t_raw, engine.mm_to_inches(w_raw) if is_metric else w_raw, engine.mm_to_inches(l_raw) if is_metric else l_raw)
        project_cost = engine.calculate_total_lumber_cost(bf_total, cost_basis)
    with col_v2:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">Total Volume</div><div class="metric-value">{bf_total:.2f} BF</div></div><div class="metric-card"><div class="metric-label">Estimated Cost</div><div class="metric-value" style="color:#2a9d8f;">US$ {project_cost:,.2f}</div></div>""", unsafe_allow_html=True)

with tab4:
    st.markdown("### Miter & Compound Bevel Calculation Grid")
    st.markdown("<p class='large-subtext'><strong>Method:</strong> Non-Planar Spherical Trigonometric Projection Vector Geometry.<br><strong>Required Measurements:</strong> Symmetrical frame structure side counts and overall side flare slope angle degrees.</p>", unsafe_allow_html=True)
    st.markdown("---")
    col_j1, col_j2 = st.columns([1.2, 1.5])
    with col_j1:
        sides = st.number_input("Total Polygon Frame Sides", min_value=3, value=4, step=1, key="join_s")
        slope = st.slider("Structure Splay/Flare Angle (Degrees)", min_value=0.0, max_value=85.0, value=15.0, key="join_sl")
    with col_j2:
        m_deg, b_deg = engine.calculate_compound_miter(sides, slope)
        st.markdown(f"""<div style="display:flex; gap:15px;"><div class="metric-card" style="flex:1;"><div class="metric-label">Miter Saw Setting</div><div class="metric-value">{m_deg:.2f}°</div></div><div class="metric-card" style="flex:1;"><div class="metric-label">Blade Tilt Bevel</div><div class="metric-value" style="color:#ef233c;">{b_deg:.2f}°</div></div></div>""", unsafe_allow_html=True)

with tab5:
    st.markdown("### Seasonal Dimensional Movement Risk Matrix")
    st.markdown("<p class='large-subtext'><strong>Method:</strong> Species Radial/Tangential Shrinkage Coefficient Projections.<br><strong>Required Measurements:</strong> Grain cross-board widths, current workshop humidity parameters, and target regional moisture contents.</p>", unsafe_allow_html=True)
    st.markdown("---")
    col_p1, col_p2 = st.columns([1.2, 1.5])
    with col_p1:
        width_raw = st.number_input(f"Total Board Grain Width ({u_length})", min_value=1.0, value=36.0 if not is_metric else 1000.0, key="phys_w")
        current_mc = st.slider("Current Timber Moisture (%)", min_value=4.0, max_value=25.0, value=12.0, key="phys_cmc")
        target_mc = st.slider("Target Climate Equilibrium Moisture (%)", min_value=4.0, max_value=25.0, value=7.0, key="phys_tmc")
        width_in = engine.mm_to_inches(width_raw) if is_metric else width_raw
    with col_p2:
        movement_in = engine.calculate_wood_movement(width_in, current_mc, target_mc, wood["tangential_coefficient"])
        movement_display = engine.inches_to_mm(movement_in) if is_metric else movement_in
        
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #ef233c;">
            <div class="metric-label">Predicted Dimensional Shift</div>
            <div class="metric-value" style="color:#ef233c;">± {movement_display:.4f} {u_length}</div>
            <p style="font-size: 15px; color: #c9d1d9; margin-top: 12px;">
                <strong>⚠️ Workshop Alert:</strong> Extreme environmental shifts cause wood cracking and joint failure. Keep your instruments monitored safely!
            </p>
            <hr style="margin: 15px 0; border: 0; border-top: 1px solid #2d3139;">
            <p style="font-size: 14px; margin-bottom: 0; color: #8d99ae;">
                🪵 <em>Building fine instruments? Check out our stands featuring precision hygrometers at 
                <a href="https://timberlenscreations.com" target="_top" style="color:#2a9d8f; font-weight:bold; text-decoration:none;">TimberLens Creations</a>.</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
