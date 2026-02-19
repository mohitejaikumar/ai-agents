def math(expression: str):
    return eval(expression)

def lookup_population(country: str):
    populations = {
        "India": 1_400_000_000,
        "Japan": 125_000_000,
        "United States": 330_000_000,
        "Brazil": 210_000_000,
        "Indonesia": 270_000_000,
        "Mexico": 126_000_000,
        "Russia": 145_000_000,
        "United Kingdom": 67_000_000
    }
    return populations.get(country, "Country not found")

