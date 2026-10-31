---
title: Visualization of a Binary Black Hole Merger with Ray Tracing
date: 2026-10-31
type: page
---

<figure class="bbh-full">
  <video controls autoplay muted loop playsinline preload="metadata" poster="/media/bbh/q1a0_b_poster.jpg">
    <source src="/media/bbh/q1a0_b_1080p.webm" type="video/webm">
    <source src="/media/bbh/q1a0_b_1080p.mp4" type="video/mp4">
  </video>
  <figcaption>Inspiral, merger and ringdown of an equal-mass, non-spinning binary black hole. Numerical relativity simulation with the Einstein Toolkit; rendered with vistools.</figcaption>
</figure>

## Rendering

The gravitational-wave field is volume-rendered by ray marching. At each sample along a camera ray,
the field is evaluated directly from the spin-weight −2 spherical-harmonic modes of the strain
(ℓ ≤ 4) at the retarded time *t* − *r*/*s*, where *s* is a radial scale chosen for display. The
plotted quantity is the plus polarization without its 1/*r* falloff, so that the amplitude is
comparable throughout the volume. Only the positive crests are drawn, as nested isosurfaces; the
colour encodes the field value, from dark blue (low) through green and yellow to orange (high).

The background star field is gravitationally lensed by ray tracing. Near each black hole, rays are
integrated as null geodesics of the Kerr metric of that hole, with a fourth-order Runge–Kutta scheme
in Kerr–Schild coordinates; at larger impact parameters the analytic weak-field deflection,
including the first-order Lense–Thirring term, is used. Each black hole of the inspiral is a
separate lens, and the lenses are replaced by the remnant around merger. Rays that cross a horizon
are captured, so each black hole appears as its shadow. The wave field itself is not lensed.

## Simulation

- **System:** equal-mass, non-spinning binary black hole (mass ratio 1), evolved with the
  [Einstein Toolkit](https://einsteintoolkit.org/).
- **Gravitational waves:** Ψ₄ extracted on finite-radius spheres, extrapolated to future null
  infinity, and integrated twice in time to obtain the strain.
- **Remnant:** mass 0.952 *M* and dimensionless spin 0.687, where *M* is the total initial mass,
  computed from the quasi-local measures on the final apparent horizon.

## Downloads

- [1080p MP4 (14 MB)](/media/bbh/q1a0_b_1080p.mp4)
- [1080p WebM (7 MB)](/media/bbh/q1a0_b_1080p.webm)
