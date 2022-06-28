Apibara Python SDK
==================

.. warning::
    This SDK is alpha software. The API will change drastically until the beta.

    `Open an issue on GitHub <https://github.com/apibara/python-sdk>`_ to report bugs or provide feedback.


Build web3-powered applications in Python. 

`Apibara <https://github.com/apibara/apibara>`_ is a tool to build web APIs that
integrate data from one or more blockchains. Simply define a new indexer service
and the Apibara service will send it historical and live events to index.


Getting started
---------------

Start by running MongoDB and Apibara using the `docker-compose.yml` file included in `examples/starknet`.

.. code::

    docker-compose up


Then you can run the example script.

.. code::

    python examples/starknet/main.py


License
-------

   Copyright 2022 GNC Labs Limited

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
