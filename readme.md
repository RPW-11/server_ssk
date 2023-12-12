To run the server:

1. Create a virtual environment using venv
`python3 -m venv .venv`

2. Run this command to activate the virtual env
`source .venv/bin/activate`
   For windows, run this command
`.venv\Scripts\activate`

3. Install depedencies using pip
`pip install flask gunicorn`

4. Make sure you are in the root folder of the project, then run this to activate the server. Replace \[ip] with your ip
`gunicorn -w 4 -b [ip]:5000 server:server`