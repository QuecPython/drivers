# RC522 RFID Module User Manual

## Overview

This document explains how to use the RC522 RFID module based on QuecPython for card reading and writing operations. The RC522 is a contactless read/write chip that supports the ISO14443A protocol, commonly used in access control systems, membership card systems, and other applications.

## Hardware Connection

Before using the RC522 module, ensure proper hardware connections:

- SPI interface connection
- RST pin connected to GPIO12
- IRQ pin connected to GPIO11 (optional interrupt function)

## Quick Start

### 1. Initialize the RC522 Module

```python
from mfrc522 import Mfrc522_spi  
reader = Mfrc522_spi(pin_rst=Pin.GPIO12, pin_irq=Pin.GPIO11)  
print("RC522 module initialization complete")  
```

### 2. Basic Functionality

#### Read Card ID

```python
card_id = reader.read_id()  
print('Detected card ID: {0}'.format(card_id))  
```

#### Write Data to Card

```python
# Define the block address and data to write  
blockAddr = 0x01  # Block address  
data = [0x00, 0x0A, 0x10, 0x00, 0x0C, 0x00, 0xA0, 0x05, 0x00, 0x40, 0x40, 0x00, 0x10, 0x20]  

# Perform write operation  
reader.Mfrc522_Write(blockAddr, data)  
print("Data write complete")  
```

#### Read Data from Card

```python
# Read data from the specified block address  
read_data = reader.Mfrc522_Read(blockAddr)  
print('Read data: {0}'.format(read_data))  
```

## Advanced Features

### 1. Interrupt Mode

The module supports interrupt-based card detection. Pass the `irq_cb` parameter during initialization to set a custom interrupt callback function:

```python
def my_callback(para):  
    print("Card detected nearby!")  
    card_id = reader.read_id_no_block()  
    if card_id:  
        print("Card ID:", card_id)  

reader = Mfrc522_spi(pin_rst=Pin.GPIO12, pin_irq=Pin.GPIO11, irq_cb=my_callback)  
```

### 2. Multi-Block Read/Write

The module supports reading and writing multiple data blocks:

```python
# Define multiple block addresses  
block_addrs = [8, 9, 10]  

# Write long text data (automatically distributed across blocks)  
text_data = "This is a long text to be stored"  
reader.write(text_data)  

# Read multi-block data  
id, read_text = reader.read()  
print("Read text:", read_text)  
```

## Notes

1. The GPIO ports in the text are for reference only. For specific interfaces, please refer to the manual of the actual development board used
2. Ensure stable power supply to the RFID module.
3. Storage structures may vary by card type—refer to the respective card specifications.
4. Some blocks may be key or control blocks—verify before writing.
5. Read/write operations require key authentication. The default key is `[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]`.

## Troubleshooting

1. **Unable to Detect Card**:
   - Check antenna connection.
   - Ensure the card type is ISO14443A.
   - Adjust the distance between the card and the module.
2. **Read/Write Failures**:
   - Verify if the card is writable.
   - Confirm the correct block address.
   - Check if the authentication key is correct.
3. **Communication Errors**:
   - Inspect SPI connections.
   - Verify RST pin configuration.
   - Ensure stable power supply.

## API Reference

### Key Methods

- `read_id()`: Read card ID (blocking).
- `read_id_no_block()`: Read card ID (non-blocking).
- `read()`: Read card data (blocking).
- `read_no_block()`: Read card data (non-blocking).
- `write(text)`: Write text data (blocking).
- `write_no_block(text)`: Write text data (non-blocking).
- `Mfrc522_Read(blockAddr)`: Read data from a specified block.
- `Mfrc522_Write(blockAddr, writeData)`: Write data to a specified block.

## Example Code

Complete test code:

```python
import _thread  
from mfrc522 import Mfrc522_spi  
import utime  

def rc522_test():  
    # Initialize RC522 module  
    reader = Mfrc522_spi(pin_rst=Pin.GPIO12, pin_irq=Pin.GPIO11)  
    print("RC522 module initialized")  
    
    while True:  
        # Attempt to read card ID  
        card_id = reader.read_id_no_block()  
        if card_id:  
            print('Detected card ID: {0}'.format(card_id))  
            
            # Read data  
            id, text = reader.read_no_block()  
            if text:  
                print('Card data:', text)  
            
            # Write data  
            new_data = "Hello, RFID!" + str(utime.time())  
            reader.write(new_data)  
            print('New data written:', new_data)  
        
        utime.sleep_ms(500)  

# Run test in a new thread  
_thread.start_new_thread(rc522_test, ())  
```

## Version Information

- Current Version: v1.0
- Last Updated: 2023-10-15
- Compatible Platform: QuecPython

For further assistance, refer to the full module source code or contact technical support.