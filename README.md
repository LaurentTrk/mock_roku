Roku Mock
====

Used to mock Roku Device on a local network.
First step to use Roku interface to receive commands from the Harmony Logitech hub.

Harmony logitech hub does not support sending custom commands over IP, but support sending commands to Roku device over IP.
The idea is to fake Roku device to receive commands over IP.

- answer_ssdp : simple ssdp listener to answer to Harmony Logitech hub SSDP broadcast (see https://sdkdocs.roku.com/display/sdkdoc/External+Control+Guide)
- roku.py : http server to answer http request from Harmony Logitech hub commands



