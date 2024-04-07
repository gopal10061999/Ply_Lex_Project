
import os

def print_menu():
    """Print the COVID-19 comparison menu."""
    print("COVID-19 comparison Menu:")
    print("a. Total cases")
    print("b. Active cases")
    print("c. Total deaths")
    print("d. Total recovered")
    print("e. Total tests")
    print("f. Death/million")
    print("g. Tests/million")
    print("h. New cases")
    print("i. New deaths")
    print("j. New recovered")

def get_user_choice():
    """Get user choice from the menu."""
    while True:
        choice = input("Choose from [a-j]: ").strip().lower()
        if choice not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
            print("Invalid choice! Please choose from [a-j].")
        else:
            return choice

def get_country_name():
    """Get user input for country name."""
    return input("Enter Country name: ").strip()

def run_pipeline(choice, country):
    """Run the pipeline with user's choice and country."""
    os.system(f"python3 mapper312.py {choice} {country} | python3 combiner312.py | python3 reducer312.py")

def main():
    print_menu()
    choice = get_user_choice()
    country = get_country_name()
    run_pipeline(choice, country)

if __name__ == "__main__":
    main()
