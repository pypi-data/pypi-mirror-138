# Text Me Keras

A TensorFlow callback that texts back... to let you know how training is going.

Have you ever found yourself at a party, all your friends are getting hundreds of texts... but not you? Well, now you can be popular. Just add this callback when training your models and it will send you a summary of your training procedure! Say goodbye to those lonely, message-free lock screens with the TextMeKeras callbacks!

[![run tests and code formatting](https://github.com/djvaroli/text_me_keras/actions/workflows/run_tests.yml/badge.svg)](https://github.com/djvaroli/text_me_keras/actions/workflows/run_tests.yml)

## Usage.
<hr />

### Clone and Install.
   
`git clone https://github.com/djvaroli/text_me_keras.git && cd text_me_keras/ && pip install -e .`

Or

`pip install git+https://github.com/djvaroli/text_me_keras.git`

### Export Twilio Credentials

Note: If you don't have Twilio credentials, you can create a free account at https://www.twilio.com/. Then create a new project and get a free phone number as well as the necessary credentials.

Python
```python
import os

os.environ["TWILIO_ACCOUNT_SID"] = <your_account_sid>
os.environ["TWILIO_AUTH_TOKEN"] = <your_auth_token>
```

Shell
```
export TWILIO_ACCOUNT_SID=<your_account_sid>
export TWILIO_AUTH_TOKEN=<your_auth_token>
```

### Try it Out
```python
import os

import numpy as np
from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, LeakyReLU
from tensorflow.keras.models import Model
from tensorflow.keras.datasets import mnist
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy

from text_me_keras.callbacks import TextMeCallback
# if you haven't set the credentials before hand you'll get a warning


# set the credentials
os.environ["TWILIO_ACCOUNT_SID"] = <your_account_sid>
os.environ["TWILIO_AUTH_TOKEN"] = <your_auth_token>

# download MNIST dataset
(trainX, trainy), (testX, testy) = mnist.load_data()
print(trainX.shape, trainy.shape)  # (60000, 28, 28) (60000,)

# reshape to have channel dimensions
trainX = np.expand_dims(trainX, axis=-1)
testX = np.expand_dims(testX, axis=-1)
print(trainX.shape, testX.shape)  # (60000, 28, 28, 1) (60000, 28, 28, 1)


# build a model for MNIST
i = Input((28, 28, 1))
x = Conv2D(32, (5, 5), 2, padding="same", use_bias=False)(i)
x = LeakyReLU()(x)
x = Conv2D(64, (5, 5), 2, padding="same", use_bias=False)(x)
x = LeakyReLU()(x)
x = Flatten()(x)
x = Dense(10)(x)
model = Model(i, x)
# model.summary()  # print the summary if you'd like to see it

# set upt the loss, metrics and compile
loss = SparseCategoricalCrossentropy(from_logits=True)
metrics = [SparseCategoricalAccuracy()]
model.compile("adam", loss, metrics=metrics)

# set up the callback
to = <number to send updates to>
from_ = <number associated with your Twilio account>

# if you haven't set the creds by this point, an exception will be raised
cbck = TextMeCallback(
    send_to=to, 
    send_from=from_,  # must be a number attached to your Twilio account 
    frequency=1,  # num epochs between texts
    run_id="Test Run"
)

model.fit(trainX, trainy, epochs=2, validation_data=[testX, testy], batch_size=256, callbacks=callbacks)

# trained with a Colab GPU
Epoch 1/2
235/235 [==============================] - 2s 7ms/step - loss: 0.6579 - sparse_categorical_accuracy: 0.9049 - val_loss: 0.1528 - val_sparse_categorical_accuracy: 0.9538
Epoch 2/2
235/235 [==============================] - 2s 6ms/step - loss: 0.1318 - sparse_categorical_accuracy: 0.9639 - val_loss: 0.1321 - val_sparse_categorical_accuracy: 0.9625
```

