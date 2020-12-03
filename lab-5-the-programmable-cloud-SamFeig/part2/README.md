# Part Two - Clone a machine

In this part, you'll do the following:

* Create a snapshot of the disk from your instance in the first part, once you have the `flask` application installed. You can assume you know the name of the instance, but you should then create the snapshot from the appropriate disk. You use the [createSnapshot API from the disk interface](https://cloud.google.com/compute/docs/reference/rest/v1/disks/createSnapshot) to do this. You should name your snapshot `base-snapshot-<instance>` where `<instance>` is the name of your instance.
* Now, create three instances using that `base-snapshot` and [measure the time it takes to create each one](https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution). Create a file `TIMING.md` that lists the times and commit that to your repo.