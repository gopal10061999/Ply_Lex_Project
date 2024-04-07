import subprocess
import os

# Get the current directory path
current_directory = os.path.dirname(os.path.abspath(__file__))
print("----Wait while we are extracting the required file----")
subprocess.run(["python3", os.path.join(
    current_directory, "extractNR.py")])

subprocess.run(["python3", os.path.join(
    current_directory, "Run_australia.py")])

subprocess.run(["python3", os.path.join(
    current_directory, "Run_england.py")])

subprocess.run(["python3", os.path.join(
    current_directory, "Run_india.py")])

subprocess.run(["python3", os.path.join(
    current_directory, "Run_malaysia.py")])

subprocess.run(["python3", os.path.join(
    current_directory, "Run_singapore.py")])

subprocess.run(["python3", os.path.join(
    current_directory, "./Module15/DataConvertor.py")])


def run_menu312():
    subprocess.run(["python3", os.path.join(
        current_directory, "menu312.py")])


def run_menu313():
    subprocess.run(["python3", os.path.join(
        current_directory, "./module15/menu313.py")])


def run_322a():
    subprocess.run(["bash", os.path.join(os.path.dirname(os.path.abspath(__file__)), "run322a.sh")])


def run_322b():
    subprocess.run(["bash", os.path.join(os.path.dirname(os.path.abspath(__file__)), "run322b.sh")])


def run_323():
    subprocess.run(["python3", os.path.join(
        current_directory, "country_news_range.py")])


def run_324():
    subprocess.run(["python3", os.path.join(
        current_directory, "country_range_time.py")])


def run_325():
    subprocess.run(["python3", os.path.join(
        current_directory, "Jaccard.py")])

def main():
    while True:
        print("\nMenu:")
        print("1. To compare given country data with world data...")
        print("2. To compare given countries data in given time range...")
        print("3. To show all the worldwide news between given time range...")
        print("4. To show all the worldwide responses between given time range...")
        print("5. To show the date range for which news information is available for given country...")
        print("6. To extract all the news for given country between given date range...")
        print("7. To find the name of the closest country according to the Jaccard similarity for given country with given time range...")
        print("8. Go back...")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            run_menu312()
        elif choice == '2':
            run_menu313()
        elif choice == '3':
            run_322a()
        elif choice == '4':
            run_322b()
        elif choice == '5':
            run_323()
        elif choice == '6':
            run_324()
        elif choice == '7':
            run_325()
        elif choice == '8':
            print("Exiting the menu.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
