# DrexelChatbot
Repository for the DrexelChatbot senior project. 

#### Members:
  Hoa Vu <htv27@drexel.edu>,
  Tom Amon <tpa27@drexel.edu>,
  Daniel Fitzick <dwf35@drexel.edu>,
  Aaron Campbell <ajc382@drexel.edu>,
  Nanxi Zhang <nz66@drexel.edu>,
  Shishir Kharel <sk3432@drexel.edu>.

#### Application demo:
http://10.246.251.67:8080/chatbot

##### How to run the Spring Rest Service:
[Aaron]

##### How to start gac Python Server for gac:
1. Navigate to chatbot directory.
2. If restarting, make sure to kill the previous gacServer process. The process ID can be found using `pgrep -af python`
3. Run command `nohup python3 gacServer.py &`

##### How to retrain the neural network:
1. Navigate to the tools directory.
2. Make sure the training data in gac_data_combined.csv is the data you want to train on.
3. Run `sudo python3 gac_training.py`
4. Move the newly created "trained_model.m5" file to the chatbot directory.
5. Restart the gac Python Server.

#### How to run the information extraction:
1. Navigate to the ie directory.
2. If you want to gather all available information and regenerate all ttl files, run the command `python3 iemain.py -t`
3. If you want to recreate the database using the ttl files, run the command `python3 iemain.py -d`
4. If you want to do both 2. and 3., you can run the command `python3 iemain.py`

#### IE prototype libraries:
BeautifulSoup (installation: pip install bs4),
Requests (installation: pip install Requests)
