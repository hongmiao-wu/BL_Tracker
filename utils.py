def get_carrier_from_bl(bl_number):
    if bl_number.startswith("MEDU"):
        return "MSC"
    elif bl_number.startswith("MAEU"):
        return "MAERSK"
    elif bl_number.startswith("EGLV"):
        return "EVERGREEN"
    else:
        return "UNKNOWN"