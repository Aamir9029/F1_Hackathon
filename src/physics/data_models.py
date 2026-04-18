# Tyre and Weather Properties from Specification (Page 5)

TYRE_PROPERTIES = {
    "Soft": {
        "base_friction": 1.8,
        "multipliers": {
            "dry": 1.18,
            "cold": 1.00,
            "light_rain": 0.92,
            "heavy_rain": 0.80
        },
        "degradation_rates": {
            "dry": 0.11,
            "cold": 0.09,
            "light_rain": 0.12,
            "heavy_rain": 0.13
        }
    },
    "Medium": {
        "base_friction": 1.7,
        "multipliers": {
            "dry": 1.08,
            "cold": 0.97,
            "light_rain": 0.88,
            "heavy_rain": 0.74
        },
        "degradation_rates": {
            "dry": 0.10,
            "cold": 0.08,
            "light_rain": 0.09,
            "heavy_rain": 0.10
        }
    },
    "Hard": {
        "base_friction": 1.6,
        "multipliers": {
            "dry": 0.98,
            "cold": 0.92,
            "light_rain": 0.82,
            "heavy_rain": 0.68
        },
        "degradation_rates": {
            "dry": 0.07,
            "cold": 0.06,
            "light_rain": 0.07,
            "heavy_rain": 0.08
        }
    },
    "Intermediate": {
        "base_friction": 1.2,
        "multipliers": {
            "dry": 0.90,
            "cold": 0.96,
            "light_rain": 1.08,
            "heavy_rain": 1.02
        },
        "degradation_rates": {
            "dry": 0.14,
            "cold": 0.11,
            "light_rain": 0.08,
            "heavy_rain": 0.09
        }
    },
    "Wet": {
        "base_friction": 1.1,
        "multipliers": {
            "dry": 0.72,
            "cold": 0.88,
            "light_rain": 1.02,
            "heavy_rain": 1.20
        },
        "degradation_rates": {
            "dry": 0.16,
            "cold": 0.12,
            "light_rain": 0.09,
            "heavy_rain": 0.05
        }
    }
}

def get_tyre_specs(tyre_type, weather_condition):
    """
    Returns (base_friction, friction_multiplier, degradation_rate)
    """
    # Normalize inputs to lowercase to avoid matching errors
    t_type = tyre_type.capitalize()
    w_cond = weather_condition.lower().replace(" ", "_")
    
    specs = TYRE_PROPERTIES.get(t_type, TYRE_PROPERTIES["Medium"])
    
    base = specs["base_friction"]
    mult = specs["multipliers"].get(w_cond, 1.0)
    deg = specs["degradation_rates"].get(w_cond, 0.1)
    
    return base, mult, deg
