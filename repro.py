
import sys, time
from smartcard.System import readers

EXPECTED_ATR = b';\x04I2C.'
CARD_IDENTITY = [0x18, 64, 2, 0x00, 0x00, 0x20, 0x00]
INIT_APDU = [0xFF, 0x30, 0x00, 0x04] + \
            [1 + len(CARD_IDENTITY)] + [0x01] + CARD_IDENTITY

PREFIX = [0xFF, 0x30, 0x00]
READ_PREFIX = PREFIX + [0x05]
WRITE_PREFIX = PREFIX + [0x06]
VERSION = 0x01

ADDRESS_0 = [0,0,0,0]
ADDRESS_20 = [0,0,0,0x20]

TEST_MESSAGE = "The Quick Brown Fox Jumps Over the Lazy Dog. It was the best of times, it was the worst of times."

TEST_MESSAGE_BYTES=TEST_MESSAGE.encode('ascii')

# Look for a single reader
connected_readers = readers()
if len(connected_readers) != 1:
    print("Please connect exactly one reader")
    sys.exit(1)

print("Found 1 card reader.")

connection = connected_readers[0].createConnection()

# Wait for the right card to be inserted
while True:
    try:
        print("Looking for Card...")
        
        connection.connect()

        print("Got Card, checking type")

        atr = bytes(connection.getATR())

        if atr == EXPECTED_ATR:
            print("Got the right card.")
            break
        else:
            print("Wrong type of card, please remove and insert AT24C64.")
            time.sleep(5)
    except:
        print("No card connected, trying again in 5s.")
        time.sleep(5)

def transmit(apdu):
    print("Send:\n", [hex(i) for i in apdu])
    data, sw1, sw2 = connection.transmit(apdu)
    print("Recv:\n", [hex(i) for i in data], hex(sw1), hex(sw2))
    return data, sw1, sw2

print("Init\n")
transmit(INIT_APDU)

def write_and_read_message(address, message_bytes):
    print("\nAttempting to write and read ", message_bytes)
    
    # Write the test message
    write_apdu = WRITE_PREFIX + [5 + len(message_bytes)] + [VERSION] + address + list(message_bytes)
    print("Writing")
    transmit(write_apdu)
    
    # wait 5s
    time.sleep(2)

    # read back the same location and length
    read_apdu = READ_PREFIX + [9] + [VERSION] + address + list(len(message_bytes).to_bytes(4, 'big'))
    print("Reading")
    data, sw1, sw2 = transmit(read_apdu)
    data_bytes = bytes(data)

    if data_bytes == message_bytes:
        print("Success!")
    else:
        print("Boo, failure.")
    

for address in [ADDRESS_0, ADDRESS_20]:
    print("\n\n\n====> Writing/Reading at Offset", address)
    write_and_read_message(address, TEST_MESSAGE_BYTES[:32])
    write_and_read_message(address, TEST_MESSAGE_BYTES[:64])
    write_and_read_message(address, TEST_MESSAGE_BYTES)
