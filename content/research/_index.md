---
title: Research
date: 2026-10-31
type: page
---

I study strong-field gravity in binary black hole mergers, and the methods needed to measure it with
the next generation of gravitational-wave detectors. Cosmic Explorer, the Einstein Telescope and LISA
will observe signals so loud that the accuracy of our waveform models and analysis methods will limit
many tests of fundamental physics. My work addresses this in four connected areas.

## Dynamical horizons and strong-field gravity {#horizons}

I study the horizons of merging black holes with dynamical horizons, the tubes of marginally trapped
surfaces defined by the local geometry, and with numerical relativity simulations. The shear of a
horizon measures the gravitational radiation it absorbs. In collaboration with Anshu Gupta, Sukanta
Bose, Badri Krishnan and Erik Schnetter, I showed that during the inspiral it is strongly correlated with the gravitational-wave signal at infinity
([Phys. Rev. Lett. 125, 121101](https://doi.org/10.1103/PhysRevLett.125.121101)). After the merger,
the shear of the common horizon contains quasi-normal frequencies and information about the masses and
spins of the remnant and parent black holes
([Phys. Rev. D 111, 084070](https://doi.org/10.1103/PhysRevD.111.084070)).

In collaboration with Anshu Gupta, Sukanta Bose and Badri Krishnan, I defined the tidal deformability
of a dynamical horizon through its source multipole moments
([Phys. Rev. D 105, 044019](https://doi.org/10.1103/PhysRevD.105.044019)). I was the first to show
that the horizons of a binary acquire multipolar deformations (hair) during the inspiral, and that
these deformations are strongly correlated with the gravitational-wave signal at infinity. The common
horizon inherits them at merger and settles to the Kerr state by absorbing gravitational radiation,
with quasi-normal decay of its multipole moments
([Phys. Rev. D 109, 044033](https://doi.org/10.1103/PhysRevD.109.044033)). In a work led by Yu-Cun Xie, we found that the first common horizon in a generic merger forms with a universal square-root structure
([arXiv:2609.11819](https://arxiv.org/abs/2609.11819)).

## Tests of general relativity {#tests}

In the LIGO-Virgo-KAGRA Collaboration, I contributed to the area-law analysis and the ringdown model
for GW250114 ([Phys. Rev. Lett. 135, 111403](https://doi.org/10.1103/kw5g-d732);
[Phys. Rev. Lett. 136, 041403](https://doi.org/10.1103/6c61-fm1n)), and a targeted numerical
relativity simulation for the investigation of GW230814
([Astrophys. J. Lett. 1004, L23](https://doi.org/10.3847/2041-8213/ae2ad3)). I developed
multi-segment consistency tests of general relativity and demonstrated them on GW250114
([arXiv:2603.05835](https://arxiv.org/abs/2603.05835)). In a work led by Monica Rincón-Ramírez, we showed that nature possibly selects the remnants of
binary black hole mergers by a maximum-entropy principle, constrained by the Bondi mass and angular
momentum of the binary
([Phys. Rev. Lett. 137, 021406](https://doi.org/10.1103/hvp6-ydbq)). I co-lead the
testing-general-relativity section of the Cosmic Explorer Science Traceability Matrix.

## Precision data analysis {#data-analysis}

Gravitational-wave inference usually assumes that the detector noise has a circulant covariance. This
discards correlations and can make posteriors too narrow. The exact time-domain likelihood avoids this approximation, but evaluating it costs *O*(*N*²)
operations for *N* data samples. Profiling showed that its matrix–vector product was limited by memory
bandwidth, not by arithmetic. I therefore looked for a way to replace it with operations on vectors alone.
While browsing the Penn State library to learn about structured matrices, I came across *Fast Reliable
Algorithms for Matrices with Structure* (T. Kailath and A. H. Sayed, eds., SIAM, 1999). The book
presents the Gohberg–Semencul formula (1972), which expresses the inverse of a Toeplitz matrix through
products of triangular Toeplitz matrices. I realised that, because multiplying by a Toeplitz matrix is
a convolution, the convolution theorem reduces the memory traffic of the exact likelihood from
*O*(*N*²) to *O*(*N*) and its cost to *O*(*N* log *N*). I developed this approach independently in 2025.
[tdanalysis](https://pypi.org/project/tdanalysis/), built on it and in production use since December
2025, evaluates the exact likelihood (without heterodyning), handles gaps and multiple disjoint data segments,
and runs on GPUs. Its first paper demonstrates full 15-parameter estimation with precessing waveforms, and, to my
knowledge, the first application of this method to real detector data, GW250114
([arXiv:2603.06010](https://arxiv.org/abs/2603.06010)). It is released as a Python package.
Sharma, Vijaykumar and Kumar arrived at the same representation independently and concurrently, and
used it with a heterodyned time-domain likelihood ([arXiv:2601.11239](https://arxiv.org/abs/2601.11239)).

The choice of priors also matters for what we infer about black holes. With B. S. Sathyaprakash, I
showed that the usual uniform spin prior can bias the inferred spins of binary black
holes ([arXiv:2602.12859](https://arxiv.org/abs/2602.12859)).

## Waveform modelling {#waveforms}

I built NRHJSur3dq8, a spectral numerical relativity surrogate for aligned-spin binaries. It provides
analytic derivatives and a calibrated error estimate along with each waveform
([arXiv:2609.09088](https://arxiv.org/abs/2609.09088)), and is released as the
[nrhjsurrogate](https://pypi.org/project/nrhjsurrogate/) package. With Abhay Ashtekar and B. S.
Sathyaprakash, I use the waveform balance laws to test how well a numerical relativity waveform
satisfies Einstein's equations without a reference waveform. In a work led by Divyajyoti, we studied the
biases in parameter inference for eccentric and precessing binaries
([Phys. Rev. D 113, 103022](https://doi.org/10.1103/jdkc-65lz)).

The [visualization page](/animation/) shows one of my binary black hole simulations. The full list of
papers is in my [CV](/cv/#publications).
