UDPReceive
==========
**DEPRECATED** Use [UDPServer](https://github.com/nio-blocks/udp_server) instead.  Recieve and convert general UDP data into signals.

Properties
----------
- **collect**: The amount of time to collect UDP data between signals.
- **host**: IP Address to bind the host UDP server to.
- **port**: Integer port number to bind the host UDP server to.

Inputs
------
None

Outputs
-------
- **default**: One signal per streamed UDP packet. The name will be the name specified in the packet The data will always be an **array of data** of the format specified in the packet.

Commands
--------
None

Dependencies
------------
None