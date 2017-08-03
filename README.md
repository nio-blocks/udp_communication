DEPRECATED
==========

Use [UDPServer](https://github.com/nio-blocks/udp_server) instead.

****

GeneralUDP
=======

Blocks that can communicate with general UDP objects

***

GeneralUDP
===========

Recieve and convert general UDP data into signals.

General UDP data is in the form `name:type:data` where where type and data follow [python struct guidelines](https://docs.python.org/2/library/struct.html)

Properties
--------------

-   **host**: IP Address to bind the host UDP server to
-   **port**: Integer port number to bind the host UDP server to

Dependencies
----------------
None

Commands
----------------
None

Input
-------
None

Output
---------
One signal per streamed UDP packet. 

The name will be the name specified in the packet

The data will always be an **array of data** of the format specified in the packet 
