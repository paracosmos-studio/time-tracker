Time Tracker

The application allows you to track time for different projects. 
The data is stored locally in a csv file. The location of the 
csv file can be changed from the settings.

---

Project Setup

1. Clone the repository and navigate to the project directory

   git clone https://github.com/paracosmos-studio/time-tracker.git
   cd time-tracker

2. Create a virtual environment and activate it

   python3 venv .venv
   source .venv/bin/activate

3. Install the required packages
   
   pip3 install -r requirements.txt

4. Ignore changes to the `default` directory content

   git update-index --assume-unchanged src/default/settings.json src/default/timesheet.csv

5. Run the application:

   cd src
   python3 main.py
