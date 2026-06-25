---
title: 'FishTracker: a lightweight, open-source tool for video tracking and space-use quantification of single aquatic animals in laboratory assays'
tags:
  - Python
  - animal tracking
  - computer vision
  - behavioural ecology
  - OpenCV
  - aquaculture
authors:
  - name: Dilshan Pathirana
    orcid: "0009-0008-2039-8884"
    affiliation: 1
affiliations:
  - name: "Department of Zoology, University of Peradeniya, Sri Lanka"  # TODO: Update with your institution
    index: 1
date: "25 June 2026"
bibliography: paper.bib
---

## Summary

FishTracker is a lightweight, open-source Python tool for tracking a single moving animal in laboratory video recordings and quantifying its movement. It uses adaptive Gaussian-mixture background subtraction [@zivkovic2004] implemented in OpenCV [@bradski2000] to isolate the animal from a static background, logs its centroid position and timestamp on every frame, and produces (i) a per-frame CSV trajectory, (ii) a Gaussian-blurred heatmap of space use overlaid on the source video, and (iii) a real-world distance-travelled summary calibrated from user-supplied tank dimensions. The tool ships with both a desktop GUI (Tkinter) for non-programmers and a parallelized command-line batch mode for higher-throughput use, and an interactive single-video debug mode for tuning detection on new footage.

## Statement of need

Quantifying activity and space use is central to behavioural ecology, ethology, and aquaculture research, and is typically assessed through standard single-subject assays such as open-field, novel-object, and mirror tests. Several capable open-source tracking packages exist — idtracker.ai [@romeroferrero2019] and TRex [@walter2021] for multi-animal identity tracking, and DeepLabCut [@mathis2018] for markerless pose estimation — but all three are built around problems (multi-individual disambiguation, body-part localization) that single-subject behavioural assays do not require, and typically expect a GPU and, for DeepLabCut, a trained model. Commercial alternatives such as EthoVision XT [@noldus2001] avoid the technical overhead but carry licensing costs that are often prohibitive for student projects and resource-limited labs, particularly outside well-funded institutions.

FishTracker is designed to sit in the gap between manual stopwatch/grid scoring and these heavier pipelines: a minimal-dependency, no-GPU, no-training-step tool for the common case of one animal in one arena, with a GUI simple enough for an undergraduate researcher to use unsupervised and a batch mode that scales to hundreds of videos on ordinary laboratory hardware. It was developed to support, and has been used to generate the movement and space-use variables (track length, time in zone) for, a behavioural-personality study comparing larvae of two sympatric Sri Lankan anuran species [@rajapaksha2025].

## Functionality

- Background-subtraction-based detection (`cv2.createBackgroundSubtractorMOG2`) with morphological noise filtering.
- Centroid logging to timestamped CSV, with short-gap interpolation (holding the last known bounding box for up to 10 frames) to reduce track fragmentation during brief inactivity or occlusion.
- Automatic heatmap generation (Gaussian-blurred trajectory density, JET colormap) overlaid on the final video frame.
- Pixel-to-real-world distance conversion given arena width/height, exported as a per-video and batch summary CSV.
- Parallelized batch processing (`concurrent.futures.ThreadPoolExecutor`) for multi-video datasets, with both a Tkinter GUI and a headless CLI entry point.
- An interactive ROI-selection debug mode for validating detection parameters on new footage before a full batch run.

## Comparison to existing tools

| | FishTracker | idtracker.ai / TRex | DeepLabCut | EthoVision XT |
|---|---|---|---|---|
| Multi-animal identity | ✗ | ✓ | ✓ (with extensions) | ✓ |
| Pose / body-part tracking | ✗ | ✗ | ✓ | ✗ |
| Requires GPU / trained model | ✗ | partial | ✓ | ✗ |
| Cost | Free, open-source | Free, open-source | Free, open-source | Commercial license |
| Setup complexity | Low | Moderate | Moderate–high | Low (closed-source) |

FishTracker deliberately trades multi-animal and pose capability for simplicity, making it suited to single-subject behavioural assays run on standard lab hardware.

## Validation

FishTracker's centroid-tracking and distance outputs underpin the movement (track length) and space-use (risky-zone time) variables in a companion behavioural study of amphibian larvae personality [@rajapaksha2025], in which it was used to batch-process several hundred open-field, novel-object, and mirror-test recordings across two species.

## Acknowledgements

We thank H.T.D. Rajapaksha and Dr. N.U.K. Pathirana (University of Peradeniya, Department of Zoology) for testing the tool on tadpole tracking data and providing the validation footage.

## References
