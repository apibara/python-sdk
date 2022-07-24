Changelog
=========


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