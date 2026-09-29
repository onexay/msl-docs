---
title: GPU acceleration
weight: 6
description: MSL doesn't give Linux distributions access to the Mac's GPU yet. What to use instead, and where the work is tracked.
---

MSL doesn't support GPU acceleration yet. Programs in a distribution can't use the Mac's GPU, so CUDA, ROCm, Vulkan and OpenCL workloads that need a GPU don't run with hardware acceleration.

GPU support for machine learning workloads is in progress, and tracked in [#13](https://github.com/onexay/msl/issues/13).

## Alternatives

- Run GPU workloads on macOS directly, with tools that use Metal, such as PyTorch's MPS backend or Apple's MLX. Keep the rest of your toolchain in the distribution, and share files through `/mnt/macos` (see [Working across file systems]({{< relref "/docs/concepts/filesystems" >}})).
- Run a model server on macOS and call it from the distribution over the network. From a distribution, `host.internal` points at macOS (see [Networking]({{< relref "/docs/concepts/networking" >}})).
