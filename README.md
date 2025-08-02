# is-this-a-pigeon
An image recognition ML model that will answer one of life's great questions: is this a pigeon? Written in Python 3.11.9. Flask used as web app framework.

The model itself is a result of transfer learning using ResNet50V2. Pigeon photos for training and test data were sourced using the Bluesky and Reddit APIs.

## Installation
1. Clone repo to your directory of choice
2. Set up venv in the root folder 
3. Install requirements.txt. Make sure you're running Python 3.11.9 or Tensorflow won't install
4. Run 'flask run' in the terminal
5. Open app in 127.0.0.1:5000
