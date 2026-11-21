import re, csv, math

def main():
    print("--- Electromagnetic Shielding Effectiveness Calculator ---")
    inp = input("Enter frequency (e.g., 50Hz, 1kHz, 2.5MHz): ")

    try:
        freq = frequency_checker(inp)
        materials = get_material(freq)
        results = calculate_shielding(freq, materials)

        print(f"\nResults for frequency: {inp} ({freq} Hz)")
        print("-" * 50)
        for res in results:
            print(f"Material: {res['material']}")
            print(f"  - Absorption Loss: {res['absorption_dB']} dB")
            print(f"  - Reflection Loss: {res['reflection_dB']} dB")
            print(f"  - Total Shielding Effectiveness: {res['total_SE_dB']} dB")
            print("-" * 50)

    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")

#what frequency was provided by the user?
def frequency_checker(n):
    #input check
    match = re.search(r"^([\d.]+)\s*([kMGm]?Hz)$", n.strip())

    #if it is not correct
    if not match:
        raise ValueError(f"Not an SI unit")

    value, unit = match.group(1), match.group(2)

    try:
        value = float(value)
    except ValueError:
         raise ValueError(f"Value should be a number")

    #unit conversion
    #since both mili and mega hertz can start with m, first I need to determine which one I am dealing with
    if unit[0] == "m":
        value = value * 1e-3
    else:
        unit = unit.lower()
        multipliers = {
            "hz": 1,
            "khz": 1e3,
            "mhz": 1e6,
            "ghz": 1e9
        }
        if unit not in multipliers:
            raise ValueError("Unknown frequency unit")
        value = value * multipliers.get(unit, 1)

    return value

#now, having frequency, we can determine the material we can use
#along side the parameters needed for the calculations, file materials.csv contains also frequency ranges at which 3 standard materials are used
#mu-metal 0-10,000 Hz
#si-steal 10,000-1,000,000 Hz
#copper 100,000-1,000,000,000 Hz
def get_material(freq, filename="materials.csv"):

    #since, as visible, frequencies are not unique, I decided to return list, just in case that more than one material could be used
    materials = []

    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                min_hz = float(row["min_hz"])
                max_hz = float(row["max_hz"])

                if min_hz <= freq <= max_hz:
                    materials.append({
                        "material": row["material"],
                        "mu_r": float(row["mu_r"]),
                        "sigma_r": float(row["sigma_r"]),
                        "thickness": float(row["default_thickness_m"])
                    })

        if not materials:
            raise ValueError("Frequency out of all available material ranges.")

        return materials

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")

#Calculate SE [dB] based on material properties and the distance from the radiation source (here I assumed 0.3m). Source: Academy of EMC
def calculate_shielding(freq, materials, dist=0.3):

    #check if only one material can be used
    if isinstance(materials, dict):
        materials = [materials]

    results = []

    for mat in materials:
        t = mat["thickness"]
        mu_r = mat["mu_r"]
        sigma_r = mat["sigma_r"]

        #absorption loss [dB]
        absorption = 13.14 * t * math.sqrt(freq * mu_r * sigma_r)

        #reflection loss [dB]
        term = freq * mu_r / sigma_r

        #preventing divide by 0 error
        if term <= 0:
            reflection = 0.0
        else:
            part1 = 0.116 / (dist * math.sqrt(term))
            part2 = 0.0536 * dist * math.sqrt(term)
            reflection = 20 * math.log10(part1 + part2 + 0.354)

            #reflection can not be negative
            if reflection < 0:
                reflection = 0.0

        #total SE
        total_se = absorption + reflection

        results.append({
            "material": mat["material"],
            "absorption_dB": round(absorption, 2),
            "reflection_dB": round(reflection, 2),
            "total_SE_dB": round(total_se, 2)
        })

    return results

if __name__ == "__main__":
    main()
