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
Navigate to chatbot directory.
If restarting, make sure to kill the previous gacServer process. The process ID can be found using `pgrep -af python`
Run command `nohup python3 gacServer.py &`

##### How to retrain the neural network:
Navigate to the tools directory.
Make sure the training data in gac_data_combined.csv is the data you want to train on.
Run `sudo python3 gac_training.py`
Move the newly created "trained_model.m5" file to the chatbot directory.
Restart the gac Python Server.

#### How to run the information extraction:
[Tom]

#### IE prototype libraries:
BeautifulSoup (installation: pip install bs4),
Requests (installation: pip install Requests)
