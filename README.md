# Summary

[Unison](http://www.cis.upenn.edu/~bcpierce/unison) is a multi-master
file-synchronization tool. This repo is creating
[rpm packages](https://copr.fedorainfracloud.org/coprs/hlovdal/unison-sync/)
of it.

[![Copr build status](https://copr.fedorainfracloud.org/coprs/hlovdal/unison-sync/package/unison-sync/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/hlovdal/unison-sync/package/unison-sync/)

This repository is primarily created for my own personal use, but if it is
useful for others, good on them.

# Details

Unison allows two replicas of a collection of files and directories to be stored
on different hosts (or different locations on the same host), modified
separately, and then brought up to date by propagating the changes in each
replica to the other. It provides both a text based and a graphical interface.

Previously, unison version incompability was a horrible mess leading to kludges
like embedding versions into the package name like `unison240`. This rpm package
removes all that cruft and deliberately has a different name and will conflict
with any of the old packages.

This package will **not** work with unison versions older than 2.52.0 (which
introduced the new version independent marshalling format).

## Rpm package

This package is based on
<http://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/home%3A/radiorabe%3A/misc/Fedora_Rawhide/src/unison251-2.51.2-8.8.src.rpm>,
with modifications as described above.

### Installation example

```bash
dnf install unison-sync
```
