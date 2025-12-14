class InputValidator:
    @staticmethod
    def _to_float(value, field_name):
        if value is None or str(value).strip() == "":
            return False, f"{field_name} is required.", None
        try:
            return True, "", float(value)
        except ValueError:
            return False, f"{field_name} must be a number.", None

    @staticmethod
    def validate_fc(fc, conversion):
        ok, msg, fc_val = InputValidator._to_float(fc, "Carrier Frequency")
        if not ok:
            return False, msg, None

        # Unit conversion
        conversions = {
            0: 1,        # Hz
            1: 1e6,      # MHz
            2: 1e9       # GHz
        }

        if conversion not in conversions:
            return False, "Invalid frequency unit.", None

        fc_val *= conversions[conversion]

        if fc_val <= 0:
            return False, "Carrier Frequency must be greater than 0.", None

        return True, "", fc_val

    @staticmethod
    def validate_speed(speed, speed_unit):
        ok, msg, v = InputValidator._to_float(speed, "Speed")
        if not ok:
            return False, msg, None

        if speed_unit == 1:
            v = v / 3.6 # (Km/h) => (m/s)

        if v < 0:
            return False, "Speed cannot be negative.", None

        return True, "", v

    @staticmethod
    def validate_angle(angle):
        ok, msg, ang = InputValidator._to_float(angle, "Angle")
        if not ok:
            return False, msg, None

        if not (0 <= ang <= 360):
            return False, "Angle must be between 0 and 360 degrees.", None

        return True, "", ang
