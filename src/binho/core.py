from enum import Enum
import serial
import serial.threaded
import queue

class LedColours(Enum):
	OFF = "OFF"
	WHITE = "WHITE"
	RED = "RED"
	GREEN = "GREEN"
	BLUE = "BLUE"
	YELLOW = "YELLOW"
	CYAN = "CYAN"
	MAGENTA = "MAGENTA"

class BinhoNovaError:
	pass

class Reader(serial.threaded.LineReader):
	def __init__(self, rx_queue):
		super().__init__()
		self.rx_queue = rx_queue

	def handle_line(self, text):
		self.rx_queue.put(text)

def build_reader(rx_queue):
	def inner():
		return Reader(rx_queue)
	return inner


class BinhoNova:
	def __init__(self, port):
		self.rx_queue = queue.Queue()
		self.serial = serial.Serial(port=port, baudrate=1_000_000, timeout=0.1)
		self.reader = serial.threaded.ReaderThread(self.serial, build_reader(self.rx_queue))
		self.protocol = None
		self.timeout = 0.1
		

	def __enter__(self):	
		self.protocol = self.reader.__enter__()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.reader.__exit__(exc_type, exc_val, exc_tb)
		self.protocol = None

	def id(self) -> str:
		self.protocol.write_line("+ID")
		response = self.rx_queue.get(timeout=self.timeout).split(" ")
		if len(response) == 2 and response[0] == "-ID":
			return response[1]
		else:
			raise BinhoNovaError

	def ping(self) -> None:
		self.protocol.write_line("+PING")
		response = self.rx_queue.get(timeout=self.timeout).split(" ")
		if len(response) != 1 or response[0] != "-OK":
			raise BinhoNovaError

	def led_colour(self, colour: LedColours) -> None:
		self.protocol.write_line("+LED " + colour.value)
		response = self.rx_queue.get(timeout=self.timeout).split(" ")
		if len(response) != 1 or response[0] != "-OK":
			raise BinhoNovaError
