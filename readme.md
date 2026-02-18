# 🌌 NEXUS AUDIO LAB - Zen Experience v3.5

> **High-Fidelity Audio Biohacking (96kHz / 32-bit Float)**

**Nexus Audio Lab** is not just a sound player; it is a therapeutic audio synthesis laboratory. Unlike YouTube videos or streaming apps that compress audio (destroying subtle frequencies), Nexus generates pure mathematical waves locally on your machine, ensuring a **Bit-Perfect** experience.

![Status](https://img.shields.io/badge/Status-Stable-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Audio](https://img.shields.io/badge/Audio-96kHz%20%7C%2032bit-purple)

## 🎯 The Compression Problem
When you listen to a "Binaural Beat" on Spotify or YouTube, the compression algorithm (MP3/AAC) removes data it considers "inaudible" to save space. However, in sound therapy and biohacking, the precision of the sine wave is critical for effective **brainwave entrainment**.

## ⚡ The Nexus Solution
This software uses the `NumPy` and `SciPy` libraries to calculate every single audio sample mathematically.

The generation formula used is:
$$y(t) = A \cdot \sin(2 \pi f t)$$

Rendering occurs at **96,000 samples per second (96kHz)** with a depth of **32-bit Float**. This results in a "liquid wave," free from digital distortion (*aliasing*) and quantization noise.

## 🛠️ Features

### 1. Pure Frequency Generator (Solfeggio)
Generates perfect sine tones based on the Solfeggio scale and natural frequencies.
- **Examples:** 528Hz (DNA Repair), 432Hz (Universal Math), 7.83Hz (Schumann Resonance).

### 2. Binaural Synthesizer
Creates two tones with slightly different frequencies for each ear, forcing the brain to create a third phantom frequency (the "beat").
- **Example:** Left Ear (200Hz) + Right Ear (210Hz) = Brain enters Alpha State (10Hz).

### 3. Colored Noise Generator
Stochastic algorithms to generate sonic masks:
- **White Noise:** Extreme focus.
- **Pink Noise:** Relaxation and sleep.
- **Brown Noise (Brownian):** The gold standard for ADHD and deep mental silencing.

### 4. Mixing Desk (Mixer)
Allows you to create complex "Sound Recipes".
- *Protocol Example:* 60% Brown Noise (Base) + 30% Binaural Theta 6Hz (Induction) + 10% Solfeggio 528Hz (Healing).

### 5. Integrated Guide
The software features a complete internal manual on hardware (DACs, Amps, KZ/Sennheiser IEMs) and usage protocols.

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/nexus-audio-lab.git](https://github.com/YOUR-USERNAME/nexus-audio-lab.git)
   cd nexus-audio-lab