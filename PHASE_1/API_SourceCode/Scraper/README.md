## Run the web scraper in the virtual environment
**Please notice that the scraper will only work if you have installed GNU version command line tools**  
Set up a virtual environment outside our project folder and activate it
```bash
python3 -m venv seng3011venv
source < path-to-seng3011venv/bin/activate >
```
You can diactivate the virtual environment anytime in any folder by the following instruction
```bash
deactivate
```
The next step is to go into our scraper folder and install necessary dependencies 
```bash
cd SENG3011_A-GROUP-FOR-SENG3011/PHASE_1/API_SourceCode/Scraper
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```
This step can be relatively slow, it's going to take few minutes and ... some patience :)
