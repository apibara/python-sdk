Apibara Python SDK
==================

.. warning::
    This SDK is alpha software. The API will change drastically until the beta.

    `Open an issue on GitHub <https://github.com/apibara/python-sdk>`_ to report bugs or provide feedback.


Build web3-powered applications in Python. 


Development
-----------

Install the following packages using your OS package manager:

* protobuf
* poetry
* docker (for testing)

Install all Python dependencies with:

.. code::

    poetry install

Run tests with:

.. code::

    poetry run pytest tests

Format code with:

.. code::

    poetry run black src examples test
    poetry run isort src examples test

To update the protobuf definitions:

.. code::

    protoc -I=protos/starknet/ \
        --python_out=src/apibara/starknet/proto/ \
        --pyi_out=src/apibara/starknet/proto protos/starknet/*


Development (with Nix)
----------------------

This repository provides a Nix development environment. To use it simply run:

.. code::

   nix develop

All dependencies, including pre-commit hooks, will be installed for you.


License
-------

   Copyright 2023 GNC Labs Limited

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
