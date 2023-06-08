Changelog
=========

Apibara Python SDK 0.6.7 (2023-06-08)
--------------------------------------

Fixed
^^^^^

 - Improve compatibility with Python 3.8


Apibara Python SDK 0.6.6 (2023-04-14)
--------------------------------------

Changed
^^^^^^^

 - Rescan blocks after filter update.

Fixed
^^^^^

 - Exception when receiving invalidate message and log level is debug.
 - Invalidate data when receiving an invalidate message.


Apibara Python SDK 0.6.5 (2023-03-16)
--------------------------------------

Added
^^^^^

 - Add :code:`update_filter` method to :code:`Indexer` to dynamically update the stream filter.


Apibara Python SDK 0.6.4 (2023-02-24)
--------------------------------------

Added
^^^^^

 - Add support for authenticating with the server


Apibara Python SDK 0.6.3 (2023-02-21)
--------------------------------------

Added
^^^^^

 - Set recommended grpc client options by default.
 - Add :code:`StreamAddress` class with a list of well-known Apibara streams.

Fixed
^^^^^

 - Include timeout waiting for messages.


Apibara Python SDK 0.6.2 (2023-01-19)
--------------------------------------

Added
^^^^^

 - :code:`Filter.to_proto` method that returns the filter's protobuf object.


Apibara Python SDK 0.6.1 (2023-01-18)
--------------------------------------

Added
^^^^^

 - Header filter has now a :code:`weak` flag to include header data only if
 any other filter matches. The flag can be set with :code:`Filter().with_header(weak=True)`.


Apibara Python SDK 0.6.0 (2023-01-16)
--------------------------------------

Added
^^^^^

 - New :code:`Indexer` and :code:`StarkNetIndexer` interfaces for developers to implement indexers.
 - Low-level :code:`StreamService`, :code:`StreamClient`, and :code:`StreamIter` to communicate with the
 streams directly.
 - A :code:`apibara.starknet` module with StarkNet specific filters and data.

Changed
^^^^^^^

 - :code:`IndexerRunner` is now responsible for applying an `Indexer` over a stream.


Apibara Python SDK 0.5.16 (2022-12-05)
--------------------------------------

Added
^^^^^

 - Events now include their transaction. Use :code:`event.transaction` to access it.


Apibara Python SDK 0.5.15 (2022-12-01)
--------------------------------------

Fixed
^^^^^

 - Fix exception when starting block is not specified.


Apibara Python SDK 0.5.14 (2022-11-26)
--------------------------------------

Fixed
^^^^^

 - Fix exception caused by pending block handler.


Apibara Python SDK 0.5.13 (2022-11-25)
--------------------------------------

Fixed
^^^^^

 - Don't skip previously handled pending blocks on restart.


Apibara Python SDK 0.5.12 (2022-11-24)
--------------------------------------

Added
^^^^^

 - Introduce :code:`MessageHandler` to simplify testing.


Apibara Python SDK 0.5.11 (2022-11-23)
--------------------------------------

Fixed
^^^^^

 - Handle deploy account transactions

Changed
^^^^^^^

 - Invalidate data between pending blocks handlers.


Apibara Python SDK 0.5.10 (2022-11-22)
--------------------------------------

Changed
^^^^^^^

 - Invalidate data on chain reorgs and after pending blocks.


Apibara Python SDK 0.5.9 (2022-11-17)
-------------------------------------

Fixed
^^^^^

 - Keep library backward-compatible with older Apibara streams.


Apibara Python SDK 0.5.8 (2022-11-16)
-------------------------------------

Added
^^^^^

 - Add support for pending blocks and events.


Apibara Python SDK 0.5.7 (2022-11-05)
-------------------------------------

Changed
^^^^^^^

 - Raise :code:`asyncio.TimeoutError` if the message stream hangs and doesn't
 receive any message for more than 45 seconds.


Apibara Python SDK 0.5.6 (2022-10-14)
-------------------------------------

Fixed
^^^^^

 - Use the new :code:`Node.StreamMessages` method.


Apibara Python SDK 0.5.5 (2022-10-07)
-------------------------------------

Fixed
^^^^^

 - Handle StarkNet blocks with no transactions. This usually happens on custom
 connections to devnet.


Apibara Python SDK 0.5.4 (2022-10-01)
-------------------------------------

Added
^^^^^

 - Add dynamic event filters to indexer.
 - Add block handler callback to indexer.


Apibara Python SDK 0.5.3 (2022-09-27)
-------------------------------------

Fixed
^^^^^

 - Include transaction hash in :code:`StarknetEvent`.


Apibara Python SDK 0.5.2 (2022-09-15)
-------------------------------------

Fixed
^^^^^

 - Add :code:`starknet-py` to dependencies.


Apibara Python SDK 0.5.1 (2022-09-14)
-------------------------------------

Changed
^^^^^^^

 - Remove :code:`network_name` :code:`IndexerRunner` argument.
 - Support filtering events by name only.


Apibara Python SDK 0.5.0 (2022-09-14)
-------------------------------------

Changed
^^^^^^^

 - Support Apibara stream protocol.

Added
^^^^^

 - Add flag to reset indexer state.


Apibara Python SDK 0.4.3 (2022-08-04)
-------------------------------------

Added
^^^^^

 - Include transaction hash in events.


Apibara Python SDK 0.4.2 (2022-07-24)
-------------------------------------

Added
^^^^^

 - Option to sort returned elements to :code:`Storage.find`.


Fixed
^^^^^

 - Fix :code:`Storage.find` default parameters.
 - Fix :code:`Storage.delete_one` and :code:`Storage.delete_many`. They now delete only current values.


Apibara Python SDK 0.4.1 (2022-07-21)
-------------------------------------

Fixed
^^^^^

 - Connection issue with Apibara 0.3.0


Apibara Python SDK 0.4.0 (2022-07-18)
-------------------------------------

Added
^^^^^

- Introduce support for EVM-compatible networks.


Changed
^^^^^^^

- Change minimum Apibara version required to :code:`0.2.0`.


Apibara Python SDK 0.3.0 (2022-07-08)
-------------------------------------

Added
^^^^^

- Introduce :code:`IndexerStorage` and :code:`Storage` classes to interface with
document storage.


Apibara Python SDK 0.2.0 (2022-07-05)
-------------------------------------

Added
^^^^^

- Add :code:`IndexerRunner` to initialize and run the indexer in a more managed way.


Changed
^^^^^^^

- Indexer now reconnects on disconnect.


Apibara Python SDK 0.1.1 (2022-06-27)
-------------------------------------

- Initial release.
