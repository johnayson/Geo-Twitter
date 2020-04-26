import os

os.system('python twitter.py')
os.system('python tweets_clean.py')
os.system('python kafka_publish.py')
os.system('python load_files.py')
