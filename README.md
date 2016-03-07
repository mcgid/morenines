# morenines

`morenines` tracks the content of your files and can store them in cloudy places.
Its purpose is to verify the content of your files, and to manage putting them
in high-durability high-latency low-throughput storage. (i.e. cloud key-value
blog storage.)


## Index files? SHA-1 checksums? This Looks Suspiciously Similar to Git

Yes. `morenines` apes many ideas from `git`. The main differences:

- `git` stores the content of the files it tracks. `morenines` only stores the
  checksums.
- `git` is a distributed version control system. `morenines` is a
  content change detector and higher-durability-storage coordinator.

