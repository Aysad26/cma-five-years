# CMA: assets for illustration motion, version 23

Created with the built-in imagegen tool. The generated PNGs had genuine transparent alpha; WebP conversion preserved it. Both hand layers retain the original 1086 × 1448 canvas. Original hands, lion, bicycle and dandelion rasters remain unchanged.

Final project asset paths:

- `/workspace/sites/cma-five-years/dist/assets/hands-female.webp`
- `/workspace/sites/cma-five-years/dist/assets/hands-male.webp`
- `/workspace/sites/cma-five-years/dist/assets/chestnut-flight.webp`

## Prompts

### Female hand — reference: hands.webp

Use case: precise-object-edit / background-extraction. Edit target: supplied black-and-white halftone illustration of two people holding hands. Create a SINGLE isolated layer of ONLY the woman on the RIGHT: her sweater sleeve, forearm, hand and right skirt edge. Completely remove the man on the left including his sleeve, body and his hand. Reconstruct the woman's palm and fingers that are currently hidden behind the man's hand, keeping them curled into the same clasp-ready pose, anatomical five fingers, no extra digits. Preserve ALL visible right-side pixels, contours, pose, perspective, sleeve ribbing and realistic halftone engraving style as closely as possible. The woman's forearm, wrist and visible curled fingertips must remain at the EXACT SAME coordinates on the SAME full portrait canvas (1086 x 1448 proportion), including right-edge skirt and sleeve clipping. Do not center, enlarge, crop or reposition the woman. The missing man and all empty areas must be genuine transparent alpha, no white fill and no shadow. Only the hidden hand area may be reconstructed. No text, no extra objects. Intended as a layer that slides into the existing original male hand in a website animation.

### Male hand — reference: hands.webp

Use case: precise-object-edit / background-extraction. Edit target: the provided two people holding hands halftone illustration. Create ONLY the male person on the LEFT as a separate transparent layer. Preserve his denim sleeve and left trouser edge, arm, wrist, back of hand and each visible finger at the SAME exact original coordinates, scale and outlines on the SAME full 1086x1448 portrait canvas. Remove the entire female person on the right, including her forearm and her curled fingers visible between and below the male fingers. Complete ONLY the small male hand contours that were obscured by those female fingers, so his thumb and fingers have natural full unbroken edges. Keep his hand in the SAME clasp-ready pose, fingers gently curved, not spread or changed. Fine realistic black-and-white halftone engraving exactly as source. Transparent alpha where woman and white background used to be, no shadow, no white rectangle. Do not center, crop, enlarge, move, redesign or change clothing. No text or new objects. This layer slides right into the separate female hand and then settles to the original clasped image in a website animation.

### Horse chestnut leaf — style reference: sprout.webp

Use case: stylized-concept. The supplied oak sprout illustration is STYLE REFERENCE ONLY, do not reproduce its oak leaves or acorn. Generate one isolated realistic HORSE CHESTNUT LEAF: one palmate compound leaf with seven elongated serrated leaflets radiating from a single point, delicate stem. Black ink and white paper tonal detail, fine realistic engraved halftone identical to the reference's black-and-white leaf textures. Fully visible natural leaf with crisp silhouette and believable organic irregularities. No tree, no nuts, no other leaves, no words or decoration. Generous transparent margins. Genuine transparent background, no grey backdrop or drop shadow. This is a small standalone leaf to fly across the bicycle illustration on the website.

The generated leaf has five leaflets; it is used as the requested chestnut leaf. The hand layers are transient reconstructed poses: a short crossfade restores the exact original clasped illustration after their approach, avoiding a permanent change to the original anatomy.

## Motion and verification

- One chestnut flight with an arc-length sampled Catmull–Rom loop: 4.7 seconds mobile / 5.4 seconds desktop. Both endpoints are outside the actual viewport. No looped repeat.
- Hands approach from opposite sides over 1.85 seconds; the original clasped raster then returns by a soft crossfade.
- Architecture fades first, then the original masked lion appears with a 2% approach and 10px upward translation. The original full raster returns after settling, preventing permanent mask seams.
- Four dandelion cutouts were enlarged/refined to include the umbrella tips; stem clipping near the first seed is tighter. The mask URL is versioned to refresh older browser caches.
- Subject-based viewport triggers; loaded-image guards; reduced-motion, unsupported-feature, late-load and print fallbacks.
- Verification: JS syntax, source diff whitespace, deterministic desktop/mobile path and scene simulation, alpha/canvas checks, local asset references, static layer/compositing diagnostics. Browser rendering was unavailable in this environment.

## Update: version 24
The chestnut flight is removed from the page. Its source asset is retained for reuse. Hands now use a ±32% offset, a 280ms fade-in, then a 2.4-second approach with a slower start. Bicycle/railings are separated by complementary masks of the original raster, without image generation or changes to the underlying illustration.
