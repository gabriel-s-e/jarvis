## Setup
cd into project directory
run `python3 -m venv [PROJECT_NAME]`
to create a virtual environment, then run 
`source [PROJECT_NAME]/bin/activate`
**Note:** this is the windows command. Below are the commands to run this in powershell/windows.
**For CMD:**
`.\[PROJECT_NAME]\Scripts\Activate.ps1`
**For bash:**
`.\[PROJECT_NAME]\Scripts\activate.bat

this will activate the virtual environment, where we can install the dependencies
## Dependencies:
`pip3 install livekit-agents livekit-plugins-openai livekit-plugins-google livekit-plugins-silero python-dotenv`