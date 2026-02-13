from main import extract_driver_hybrid, extract_team_hybrid, extract_year

def test() :
    tests = [
        # Dictionary should catch these
        ("Tell me about Max", "Max Verstappen"),
        ("How is Ferrari doing?", "Scuderia Ferrari"),
        ("Lewis stats", "Lewis Hamilton"),
        
        # spaCy should catch these (if not in dictionary)
        ("What about Antonio Giovinazzi?", "Antonio Giovinazzi"),  # Former driver
        ("Tell me about Mick", "Mick"),  # First name only
    ]

    print("TESTIN ...")

    for test , excepted in tests :
        result = extract_driver_hybrid(test)
        status = "✅" if excepted.lower() in str(result).lower() else "❌"
        print(f"input : {test}")
        print(f"excepted : {excepted}")
        print(f"{status}Got{result}")
if __name__ == "__main__":
    test()
