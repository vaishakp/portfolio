---
# Leave the homepage title empty to use the site title
title: ''
date: 2025-10-11
type: landing

design:
  # Default section spacing
  spacing: '4rem'

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ''
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Download Full CV
        url: /uploads/resume.pdf
      headings:
        about: ''
        education: ''
        interests: ''
    design:
      css_class: hero-profile
      # Avatar customization
      avatar:
        size: large # Options: small (150px), medium (200px, default), large (320px), xl (400px), xxl (500px)
        shape: circle # Options: circle (default), square, rounded
  - block: markdown
    content:
      title: 'Research'
      subtitle: ''
      text: |-
        <figure class="bbh-float">
          <a href="/animation/" aria-label="Visualization of a binary black hole merger">
            <video autoplay muted loop playsinline preload="metadata" poster="/media/bbh/q1a0_b_square_poster.jpg">
              <source src="/media/bbh/q1a0_b_square720.webm" type="video/webm">
              <source src="/media/bbh/q1a0_b_square720.mp4" type="video/mp4">
            </video>
          </a>
          <figcaption>Gravitational radiation from an equal-mass binary black hole merger, ray-traced from an Einstein Toolkit simulation. <a href="/animation/">Details of the visualization</a></figcaption>
        </figure>

        I study strong-field gravity in black-hole mergers. My focus is how dynamical horizons deform and relax, and the structure this leaves in gravitational waves.

        My work connects numerical relativity, black-hole perturbation theory and gravitational-wave data analysis. Recent topics include horizon shear and source multipoles in binary mergers. I also work on black-hole spectroscopy and area-law tests with high signal-to-noise events such as GW250114. Other topics are accelerated time-domain inference and waveform systematics for eccentric and precessing binaries.

        I develop parallel and heterogeneous algorithms and data-analysis pipelines for next-generation detectors.
    design:
      css_class: research-summary
      columns: '1'
  - block: resume-awards
    id: awards
    content:
      title: Grants, Awards & Computing Allocations
      username: admin
    design:
      css_class: awards-section
  - block: collection
    id: papers
    content:
      title: Selected Publications
      filters:
        folders:
          - publications
        featured_only: true
      archive:
        enable: true
        link: /cv/#publications
        text: All publications
    design:
      view: citation
  - block: collection
    id: talks
    content:
      title: Recent Talks
      count: 5
      filters:
        folders:
          - events
      archive:
        enable: true
        link: /cv/#talks
        text: All talks
    design:
      view: date-title-summary
---
