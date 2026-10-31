---
title: A Binary Black Hole Merger
date: 2026-10-31
type: page
---

<figure class="bbh-full">
  <video controls autoplay muted loop playsinline preload="metadata" poster="/media/bbh/q1a0_b_poster.jpg">
    <source src="/media/bbh/q1a0_b_1080p.webm" type="video/webm">
    <source src="/media/bbh/q1a0_b_1080p.mp4" type="video/mp4">
  </video>
  <figcaption>Two equal-mass, non-spinning black holes spiral together, merge, and ring down to a single spinning black hole. Einstein Toolkit simulation; animation rendered with vistools.</figcaption>
</figure>

## What you are seeing

The glowing ball is the gravitational wave signal of the binary. Colour shows the strength of the
wave, from dark blue (weak) through green and yellow to orange (strong). The spiral arms follow the
orbit: each shell is a wavefront emitted earlier in the inspiral and carried outward at the speed of
light, so the outer shells show the binary as it was, and the inner shells as it is now.

As the holes approach, the orbit speeds up and the shells crowd together. At merger the signal is
at its strongest; afterwards the remnant black hole settles down and the last shells move out and
fade.

The starfield behind the binary is bent by the black holes. Each hole, and then the remnant, acts
as a gravitational lens computed from its mass and spin.

## The simulation

- **System:** equal-mass, non-spinning binary black hole (mass ratio 1), evolved with the
  [Einstein Toolkit](https://einsteintoolkit.org/).
- **Waves:** the strain is computed from the curvature scalar Ψ₄, extrapolated from finite
  extraction spheres to future null infinity, and built from the spherical-harmonic modes with
  ℓ ≤ 4. The plotted field is the plus polarisation multiplied by the distance from the source,
  so its amplitude stays comparable from the centre to the edge of the ball.
- **Remnant:** mass 0.952 and dimensionless spin 0.687, in units of the total initial mass,
  measured on the final apparent horizon.

## Downloads

- [1080p MP4 (14 MB)](/media/bbh/q1a0_b_1080p.mp4)
- [1080p WebM (7 MB)](/media/bbh/q1a0_b_1080p.webm)
