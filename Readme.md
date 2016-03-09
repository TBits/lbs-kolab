purpose
=======

This is a mirror of the packaging instructions of https://obs.kolabsys.com.


branches
========

Find the actual packages in the branches, eg. Kolab_3.4_Updates or Kolab_16 or Kolab_Winterfell


updatecode
==========

See the task updatecode for the LightBuildServer.

It collects the packaging instructions from obs.kolabsys.com, and uploads them to Github.

The packaging instructions are transformed so that they work on LBS.


copr
====

See the script buildsrpm.sh which creates source rpms and uploads them to a webspace so that they can be build on copr.

For the correct build order of the packages, see https://github.com/TBits/lbs-kolab-release-preparation/wiki/Preparing-a-release
