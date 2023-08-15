FireSyncHub

A brief description of what this project does and who it's for.
Prerequisites

Ensure you have the following installed on your Linux machine:

    git
    python3
    pip
    virtualenv

If not, you can install them using your package manager. For example, on Ubuntu:

```bash

sudo apt-get install git python3 pip python3-virtualenv
```
Getting Started
1. Clone the Repository

To clone the repository and navigate into the directory:

```bash

git clone https://github.com/YOUR_USERNAME/YOUR_PROJECT_NAME.git
cd YOUR_PROJECT_NAME
```
Replace YOUR_USERNAME and YOUR_PROJECT_NAME with appropriate values.
2. Create a Virtual Environment

To create a virtual environment within the project directory:

bash
```
python3 -m venv venv

```

3. Activate the Virtual Environment

To activate the virtual environment:

```bash

source venv/bin/activate
```
4. Install Dependencies

Install all required packages:

```bash

pip install -r requirements.txt
```
5. Configuration
.env File

Copy the provided .env.sample (or a similar file) and rename it to .env. Edit the .env file and fill in the necessary configurations:

```bash

cp .env.sample .env
nano .env
```
.ini File

If your project uses an .ini configuration file, copy the provided .ini.sample and rename it to your desired .ini file name. Edit the .ini file and fill in the necessary configurations:

```bash

cp .ini.sample your_project.ini
nano your_project.ini
```
6. Initial Setup

Run the setup.sh script:

```bash

./setup.sh
```
If you encounter a permission error, make the script executable with:

```bash

chmod +x setup.sh
```
7. If you don't know how to work with firebase, you should dive into [official firebase docs](https://firebase.google.com/docs). 
Because you need to create connecting creds as `creds.json` to correctly run the program.

8. Run the Application

If you've completed the setup with setup.sh, the application should already be running. If you need to run it again in the future:
Manually

You can manually start each script:

```bash

python3 firebase_worker.py &
python3 main.py
```
