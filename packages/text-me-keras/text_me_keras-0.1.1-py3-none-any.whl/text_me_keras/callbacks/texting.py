import numpy as np
from tensorflow.keras.callbacks import Callback

from ..messaging.sms import TextMessage

# warn the user if credentials are not set
TextMessage._check_if_credentials_set()


class TextMeCallback(Callback):
    def __init__(
        self,
        send_to: str,
        send_from: str,
        frequency: int,
        run_id: str = None,
        round_to: int = 4,
    ):
        """TensorFlow callback that enables sending SMS messages during model training.

        Args:
            send_to (str): Number to text model metrics to.
            send_from (str): Number from which the message is sent. Must be a valid Twilio number attached to the provided SID.
            frequency (int): Number of epochs between successive text mesages.
            run_id (str): An identifier for the run. If set will be added at the top of each text message.
            round_to (int, optional): Number of digits to round metrics to. Defaults to 4.
        """
        super(TextMeCallback, self).__init__()

        # better to raise exception here than at model training time
        TextMessage._check_if_credentials_set(action="raise")

        self.send_to = send_to
        self.send_from = send_from
        self.frequency = frequency
        self.run_id = run_id
        self.round_to = round_to
        self.text_message = TextMessage()

    def on_epoch_end(self, epoch, logs=None):
        """Checks if enough epochs have elapsed and if so,
        adds all metrics present in logs to the body of the text message and sends message.

        Args:
            epoch ([type]): [description]
            logs ([type], optional): [description]. Defaults to None.
        """
        if epoch % self.frequency != 0:
            return

        if self.run_id:
            self.text_message.add_line(f"Run ID - {self.run_id}.")

        self.text_message.add_line(f"Epoch - {epoch}.")
        if logs is not None:
            for k, v in logs.items():
                rounded_value = np.round(v, self.round_to)
                self.text_message.add_line(f"{k} = {rounded_value}.")

        self.text_message.send(self.send_to, self.send_from)
        self.text_message.reset_message()
