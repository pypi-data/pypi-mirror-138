class PreprocessingPresets:
    light_noise_reduction = {
        "noise_reduction": {
            "prop_decrease": 0.8
        },
        "set_volume": {
            "factor": 1.7
        },
        "compressor": {},
        "lowpass_filter": {
            "cutoff_frequency_hz": 6000
        }
    }
    heavy_noise_reduction = {
        "noise_reduction": {
            "prop_decrease": 1.0
        },
        "set_volume": {
            "factor": 2.0
        },
        "lowpass_filter": {
            "cutoff_frequency_hz": 5000
        }
    }
