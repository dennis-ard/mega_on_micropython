# Arducam mega camera micropython library

A library for running Arducam Mega camera with Micropython on Raspberry Pico.

  -------------
      |----arducam_mega.py - Arducam Mega camera Micropython library
      L----arducam_link.py - Example program for running full-featured examples

## Hardware Connection

| Arducam Mega   | Raspberry Pico\Pico W   |   USB TO TTL  |
|  :----------:  | :---------------------: | :-----------: |
|  VCC           | VCC                     |               |
|  GND           | GND                     |               |
|  SPI_SCK       | GP18                    |               |
|  SPI_MISO      | GP16                    |               |
|  SPI_MOSI      | GP19                    |               |
|  SPI_CS        | GP17                    |               |
|                | GP0                     | UART_TX       |
|                | GP1                     | UART_RX       |

## How to Run this Sample
> Note: you need to have the Python runtime environment installed on your local machine.
1. Refer to [this link](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#what-is-micropython) to flash the uf2 file to Pico and set up the Micropython development environment.

2. Copy arducam_link.py and arducam_mega.py to Pico for automatic execution
    1. Download pyboard.py

    ```Shell 
    cd path/to/mega_on_micropython
    curl -o pyboard.py  https://raw.githubusercontent.com/micropython/micropython/master/tools/pyboard.py
    ```

    2. Use pyboard.py to copy arducam_mega.py to the board.

    ```shell
    $ python .\pyboard.py -d COM6 -f ls
    ls :
    $ python .\pyboard.py -d COM6 -f cp .\arducam_mega.py :arducam_mega.py
    cp .\arducam_mega.py :arducam_mega.py
    $ python .\pyboard.py -d COM6 -f ls
    ls: 
           13420 arducam_mega.py
    ```

    3. Run arducam_link.py

    ```
    # Please replace "COM6" with the Micropython port of your local machine.
    $ python .\pyboard.py -d COM6 .\arducam_link.py 
    Hello,Arducam mega!
    ```

    4. Then, open the [Arducam Mega GUI](https://www.arducam.com/docs/arducam-mega/arducam-mega-getting-started/packs/GuiTool.html), and you can enjoy using it.

    5. Pico board will automatically run arducam_link.py. Copy arducam_link.py to the board as main.py and reboot Pico.
    ```
    $ python .\pyboard.py -d COM6 -f cp .\arducam_link.py :main.py
    ``` 