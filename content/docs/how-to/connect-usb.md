---
title: Connect USB devices
weight: 4
description: USB device passthrough isn't available in MSL; how to reach USB drives and devices instead.
---

Connecting a USB device to a distribution, as `usbipd-win` does for WSL, isn't available in MSL. Linux can't see a keyboard, serial adapter, security key or other USB device plugged into the Mac.

What you can do instead:

- **USB drives:** use them from macOS as usual, and copy files between the drive and your macOS folders, which distributions see under `/mnt/macos`. See [Working across file systems]({{< relref "/docs/concepts/filesystems" >}}).
- **Linux-formatted drives:** copy the whole drive into an image file on macOS (find its number with `diskutil list`, then `sudo dd if=/dev/rdiskN of=drive.img bs=4m`), and attach the image with `msl --mount`. See [Mount a disk in MSL]({{< relref "/docs/how-to/mount-disk" >}}).
- **Devices with macOS tools:** use the macOS tool for the device (a flasher, a serial terminal) outside MSL. MSL never runs macOS programs from Linux.

Internally, `msl --mount` attaches disk images to the VM as USB mass storage, but that's a virtual disk, not passthrough of a real device.
