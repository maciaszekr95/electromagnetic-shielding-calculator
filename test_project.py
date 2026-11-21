import pytest
from project import frequency_checker, get_material, calculate_shielding

### FREQUENCY CHECKER ###

def test_frequency_checker_valid():
    #proper SI unit conversion
    assert frequency_checker("50Hz") == 50.0
    assert frequency_checker("1kHz") == 1000.0
    assert frequency_checker("1GHz") == 1000000000.0
    assert frequency_checker("100 Hz") == 100.0
    assert frequency_checker("500 mHz") == 0.5
    assert frequency_checker("2.5 MHz") == 2500000.0


def test_frequency_checker_invalid_unit():
    #ValueError for wrong units
    with pytest.raises(ValueError):
        frequency_checker("500")
    with pytest.raises(ValueError):
        frequency_checker("10XYZ")


def test_frequency_checker_invalid_value():
    #ValueError for wrong values
    with pytest.raises(ValueError):
        frequency_checker("abc Hz")

### GET MATERIAL ###

def test_get_material_valid():
    #one material is matching the frequency (Mu_metal)
    result = get_material(500)
    assert isinstance(result, list)
    assert result[0]["material"] == "Mu-metal"

    #two materials are matching the frequency (Si-steel and Copper)
    result_overlap = get_material(500000)
    material_names = [m["material"] for m in result_overlap]
    assert "Silicon_Steel" in material_names
    assert "Copper" in material_names

def test_get_material_out_of_range():
    #frequency out of range
    with pytest.raises(ValueError):
        get_material(-10)

def test_get_material_file_not_found():
    #file not found
    with pytest.raises(FileNotFoundError):
        get_material(100, filename="non_existent_file.csv")

### CALCULATE SHIELDING ###

def test_calculate_shielding_single_material():
    #single material
    mu_metal = {
        "material": "Mu-metal",
        "mu_r": 50000.0,
        "sigma_r": 0.035,
        "thickness": 0.001
    }

    result = calculate_shielding(1000, mu_metal)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["material"] == "Mu-metal"
    assert result[0]["total_SE_dB"] > 0
    assert "absorption_dB" in result[0]
    assert "reflection_dB" in result[0]


def test_calculate_shielding_multiple_materials_overlap():
    #multiple materials
    overlapping_materials = [
        {
            "material": "Silicon_Steel",
            "mu_r": 2000.0,
            "sigma_r": 0.1,
            "thickness": 0.0005
        },
        {
            "material": "Copper",
            "mu_r": 1.0,
            "sigma_r": 1.0,
            "thickness": 0.00075
        }
    ]

    results = calculate_shielding(500000, overlapping_materials)

    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]["material"] == "Silicon_Steel"
    assert results[1]["material"] == "Copper"
    #check if both have SE
    assert "total_SE_dB" in results[0]
    assert "total_SE_dB" in results[1]
