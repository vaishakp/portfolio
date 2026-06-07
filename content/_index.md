---
# Leave the homepage title empty to use the site title
title: ''
date: 2025-10-11
type: landing

design:
  # Default section spacing
  spacing: '6rem'
  background:
    image:
        filename: 'rubin.jpg'
        filters:
            darken: 0.82
    fit: cover
    focal_point: center

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
        I study strong-field gravity in black-hole mergers: how dynamical horizons deform, relax, and leave measurable structure in gravitational waves.

        My work connects numerical relativity, black-hole perturbation theory, and gravitational-wave data analysis. Recent themes include horizon shear and source multipoles in binary mergers, black-hole spectroscopy and area-law tests with loud events such as GW250114, accelerated time-domain inference, and waveform systematics for eccentric and precessing binaries.

        I am especially interested in tools that make these questions computable at scale, from parallel and heterogeneous algorithms to reliable analysis pipelines for next-generation detectors.
    design:
      css_class: research-summary
      columns: '1'
  - block: collection
    id: papers
    content:
      title: Featured Publications
      filters:
        folders:
          - publications
        featured_only: true
    design:
      view: article-grid
      columns: 2
  - block: collection
    content:
      title: Recent Publications
      text: ''
      filters:
        folders:
          - publications
        exclude_featured: true
    design:
      view: citation
  - block: collection
    id: talks
    content:
      title: Recent & Upcoming Talks
      filters:
        folders:
          - events
    design:
      view: card
---
