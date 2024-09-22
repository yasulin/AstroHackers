import sys
import schedule
import time
import webbrowser

def open_browser():
    webbrowser.open("https://astro-hackers.vercel.app/")


def schedule_browser_opening():
    # Schedule the open_browser function based on user input
    schedule.every().day.at(sys.argv[1]).do(open_browser)
    print(f"Browser will open at {sys.argv[1]}.")


def main():

    schedule_browser_opening()
    # Run the scheduler loop
    while True:

        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
