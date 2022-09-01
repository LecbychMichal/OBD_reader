# OBD_reader
## Instalation
#### Clone the repository
```
git clone git@github.com:LecbychMichal/OBD_reader.git
```
```
cd OBD_reader
```
#### Create virtual environment
```
python3 -m venv env
```
#### Activate virtual environment
```
source env/bin/activate
```
#### Install requirements
```
pip install -r requirements.txt
```
#### The emulator allows batch and interactive mode.
```
python3 -m elm
```
#### Run Kafka consumer in new terminal with env
```
python3 consumer.py
```
#### Run Kafka producer in new terminal with env
```
python3 producer.py --port /dev/pts/9 --limit 5 --pause 0
```
