# Wood-E Calculation Engine Schema
This document defines the deterministic backend mathematical modules for the Wood-E single-agent architecture. It decouples the Natural Language Processing (NLP) / Agentic intent layer from the execution equations.

## Module 1: Volumetric & Financial Module
*   **Board Footage (BF):** `(Thickness (in) * Width (in) * Length (in)) / 144`
*   **Material Yield:** Includes specific commercial wastage offsets (10%-25%).
*   **Kerf Loss Allocation:** Deducts cumulative saw blade widths (`0.125"` standard) from stock yields.

## Module 2: Structural Module (Mechanical Stress)
*   **Shelf Deflection (Euler-Bernoulli Beam Theory):** Computes physical sag based on wood Modulus of Elasticity (E), load type, and dimensions.
*   **Screw Pilot & Embedment Depth:** Calculates drill bite specifications matching Janka Hardness and fastener ratings.

## Module 3: Geometric Layout Module
*   **Pythagorean Cross-Corner Squaring:** `sqrt(A² + B²)` tracking assembly alignments.
*   **Symmetrical Slat/Baluster Spacing:** Automatically centers vertical framing inserts with perfectly equal borders.
*   **Hambridge / Golden Ratio Drawer Gradients:** Determines progressive structural depths for visually balanced drawer towers.

## Module 4: Cutting & Yield Module
*   **Linear Part Parsing:** Tracks cut counts and scrap remainders over long stock.
*   **2D Sheet Good Optimization:** Layout logic for structural plywood panel breakdown profiles.

## Module 5: Joinery Trigonometry Module
*   **Planar Multi-Sided Miter Profiles:** `180 / sides` for standard flat polygons.
*   **Non-Planar Spherical Compound Miters:** Simultaneously calculates miter gauge angles and blade bevel tilts for splayed structures.
*   **Segmented Woodturning Ring Matrices:** Computes segment widths and edge cut targets for turning block construction layers.

## Module 6: Shop Physics & Tool Safety Module
*   **Wood Movement Model:** Calculates moisture-induced expansion/contraction across grain widths using radial and tangential wood properties.
*   **Machinery RPM Safety Scaler:** Maps router/drill bits diameters to safe surface speeds to prevent wood scorching or kickback.
*   **Dust Collection Static Pressure Drop:** Estimates CFM airflow requirements across line drops and elbows.