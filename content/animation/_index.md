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
  <figcaption>Inspiral, merger and ringdown of an equal-mass, non-spinning binary black hole. The simulation uses the Einstein Toolkit. The visualization was rendered with vistools.</figcaption>
</figure>

## Rendering

The gravitational-wave field is volume-rendered by ray marching. At each sample along a camera ray,
the field is evaluated from the spin-weight −2 spherical-harmonic modes of the strain (ℓ ≤ 4). The
modes are evaluated at the retarded time *t* − *r*/*s*, where *s* is a radial scale chosen for
display. The plotted quantity is the plus polarization without its 1/*r* falloff. Its amplitude is
therefore comparable throughout the volume. Only the positive crests are drawn, as nested
isosurfaces. The colour encodes the field value, from dark blue (low) through green and yellow to
orange (high).

The background star field is gravitationally lensed by ray tracing. Near each black hole, rays
follow null geodesics of the Kerr metric of that hole. They are integrated with a fourth-order
Runge–Kutta scheme in Kerr–Schild coordinates. At larger impact parameters, the analytic weak-field
deflection is used. It includes the first-order Lense–Thirring term. During the inspiral, each black
hole acts as a separate lens. Around merger, the remnant replaces both lenses. Rays that cross a
horizon are captured, and each black hole appears as its shadow. The wave field itself is not
lensed.

## Simulation

- **System:** equal-mass, non-spinning binary black hole (mass ratio 1), evolved with the
  [Einstein Toolkit](https://einsteintoolkit.org/).
- **Gravitational waves:** Ψ₄ is extracted on spheres of finite radius and extrapolated to future
  null infinity. It is integrated twice in time to obtain the strain.
- **Remnant:** the mass is 0.952 *M*, where *M* is the total initial mass. The dimensionless spin
  is 0.687. Both are computed from the quasi-local measures on the final apparent horizon.

## Downloads

- [1080p MP4 (14 MB)](/media/bbh/q1a0_b_1080p.mp4)
- [1080p WebM (7 MB)](/media/bbh/q1a0_b_1080p.webm)
