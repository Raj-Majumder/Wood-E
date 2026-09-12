import math

def mm_to_inches(mm_val: float) -> float:
    return float(mm_val / 25.4)

def inches_to_mm(in_val: float) -> float:
    return float(in_val * 25.4)

def kgs_to_lbs(kg_val: float) -> float:
    return float(kg_val * 2.20462)

def calculate_board_feet(pieces: int, thickness_in: float, width_in: float, length_in: float) -> float:
    if pieces <= 0 or thickness_in <= 0 or width_in <= 0 or length_in <= 0:
        return 0.0
    return float(pieces * (thickness_in * width_in * length_in) / 144.0)

def calculate_total_lumber_cost(board_feet: float, cost_per_bf: float) -> float:
    if board_feet <= 0 or cost_per_bf <= 0:
        return 0.0
    return float(board_feet * cost_per_bf)

def calculate_shelf_deflection(load_lbs: float, span_in: float, thickness_in: float, depth_in: float, modulus_of_elasticity_psi: float, is_uniform: bool = True) -> float:
    if thickness_in <= 0 or depth_in <= 0 or modulus_of_elasticity_psi <= 0:
        return 0.0
    inertia = (depth_in * (thickness_in ** 3)) / 12.0
    if is_uniform:
        deflection = (5.0 * load_lbs * (span_in ** 3)) / (384.0 * modulus_of_elasticity_psi * inertia)
    else:
        deflection = (load_lbs * (span_in ** 3)) / (48.0 * modulus_of_elasticity_psi * inertia)
    return float(deflection)

def calculate_compound_miter(side_count: int, slope_angle_deg: float) -> tuple:
    if side_count <= 2:
        return 0.0, 0.0
    butt_angle = 360.0 / (2.0 * side_count)
    r_butt = math.radians(butt_angle)
    r_slope = math.radians(slope_angle_deg)
    miter_rad = math.atan(math.tan(r_butt) * math.cos(r_slope))
    bevel_rad = math.asin(math.sin(r_butt) * math.sin(r_slope))
    return float(math.degrees(miter_rad)), float(math.degrees(bevel_rad))

def calculate_wood_movement(width: float, initial_mc: float, final_mc: float, species_coefficient: float) -> float:
    delta_moisture = abs(final_mc - initial_mc)
    return float(width * species_coefficient * delta_moisture)
