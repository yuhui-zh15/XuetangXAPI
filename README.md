# XuetangXAPI

Requirements：
- pymongo==2.9.2
- PILLOW==4.2.1
- wordcloud==1.4.1
- sudo apt-get install python3-tk
- add '127.0.0.1 localhost' to /etc/hosts

Build Dataset:
- python build_mongo.py
- python build_categories.py
- python build_courses.py

Run Server:
sudo python3 main.py

> Note: only support python3