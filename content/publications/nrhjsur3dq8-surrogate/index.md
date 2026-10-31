---
title: 'NRHJSur3dq8: a spectral numerical-relativity surrogate family for non-eccentric aligned-spin binary-black-hole waveforms'
date: 2026-09-08
authors:
  - Vaishak Prasad
tags:
  - Waveform modeling
  - Numerical relativity
  - Surrogate models
  - Preprint
summary: A spectral numerical-relativity surrogate family for non-eccentric aligned-spin binary black holes. It uses an action-angle parameterization and provides its derivatives and modelling error.
abstract: >-
  We present NRHJSur3dq8, a family of numerical-relativity (NR) surrogates for non-eccentric
  aligned-spin binary-black-hole waveforms inspired by an action-angle parameterization. The model
  provides both the dynamics - the Hamiltonian values, the azimuthal action, and the orbital clock as
  functions of the phasing - and the radiative pieces, namely the waveforms, their near-analytic
  derivatives, and the modeling errors associated with each. The surrogated variables are conditioned into pieces
  that vary slowly on the radiation-reaction timescale, represented on shared hp-adaptive Chebyshev
  elements, and regressed across the intrinsic parameters with a Gaussian-process model. The model is
  implemented with performance portability using Kokkos for batched evaluations.
featured: true
publication: arXiv (gr-qc:2609.09088)
doi: 10.48550/arXiv.2609.09088
links:
  - name: arXiv
    url: https://arxiv.org/abs/2609.09088
  - name: PDF
    url: https://arxiv.org/pdf/2609.09088
  - name: DOI
    url: https://doi.org/10.48550/arXiv.2609.09088
  - name: Code
    url: https://github.com/vaishakp/nrhjsurrogate
---

**Status:** Preprint

**Authors:** Vaishak Prasad (single author)

**Venue:** arXiv:2609.09088 (2026)

A spectral numerical-relativity surrogate waveform model for aligned-spin, non-eccentric binary black
holes. It provides analytic derivatives and error envelopes with each waveform. The derivatives allow
gradient-based sampling.
