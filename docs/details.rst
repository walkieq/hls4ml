======================
Backends and I/O Types
======================

Backends
--------

``hls4ml`` supports the concept of a *backend* that determines the target HLS language.
Currently, Vivado HLS, Intel HLS, and Vitis HLS (experimental) are supported.

I/O Types
---------

``hls4ml`` supports multiple styles for handling data between layers, known as the ``io_type``.

io_parallel
^^^^^^^^^^^
Data is passed in parallel between the layers. This is good for MLP networks and small CNNs. Synthesis may fail for larger networks.

io_stream
^^^^^^^^^
Data is passed one "pixel" at a time. Each pixel is an array of channels, which are always sent in parallel. This method for sending
data between layers is recommended for larger CNNs. For ``Dense`` layers, all the inputs are streamed in parallel as a single array.

With the ``io_stream`` IO type, each layer is connected with the subsequent layer through first-in first-out (FIFO) buffers.
The implementation of the FIFO buffers contribute to the overall resource utilization of the design, impacting in particular the BRAM or LUT utilization.
Because the neural networks can have complex architectures generally, it is hard to know a priori the correct depth of each FIFO buffer.
By default ``hls4ml`` choses the most conservative possible depth for each FIFO buffer, which can result in a an unnecessary overutilization of resources.

In order to reduce the impact on the resources used for FIFO buffer implementation, we have a FIFO depth optimization flow. This is described
in the :ref:`FIFO Buffer Depth Optimization` section.
