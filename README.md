<div id="top" align="center">

<!-- Shields Header -->
[![Contributors][contributors-shield]](https://github.com/franckferman/SATAN2_Cleaner/graphs/contributors)
[![Forks][forks-shield]](https://github.com/franckferman/SATAN2_Cleaner/network/members)
[![Stargazers][stars-shield]](https://github.com/franckferman/SATAN2_Cleaner/stargazers)
[![Issues][issues-shield]](https://github.com/franckferman/SATAN2_Cleaner/issues)
[![License][license-shield]](https://github.com/franckferman/SATAN2_Cleaner/blob/stable/LICENSE)

<!-- Logo -->
<a href="https://github.com/franckferman/SATAN2_Cleaner">
  <img src="https://raw.githubusercontent.com/franckferman/SATAN2_Cleaner/stable/docs/github/graphical_resources/Logo-without_background-SATAN2_Cleaner.png" alt="SATAN2_Cleaner Logo" width="auto" height="auto">
</a>

<!-- Title & Tagline -->
<h3 align="center">☢️ SATAN2_Cleaner</h3>
<p align="center">
    <em>Secure Anti-Forensics and Total Annihilation of iNformation.</em>
    <br>
    Because true privacy means erasing beyond recovery — not just pressing <code>delete</code>.
</p>

</div>

## 📜 Table of Contents

<details open>
  <summary><strong>Click to collapse/expand</strong></summary>
  <ol>
    <li><a href="#-about">📖 About</a></li>
    <li><a href="#-license">📜 License</a></li>
    <li><a href="#-contact">📞 Contact</a></li>
  </ol>
</details>

## 📖 About

`SATAN2_Cleaner` is a personal project born from my interest in counter-forensics, privacy, and advanced data destruction.

Originally conceived as a personal tool to securely wipe disks and make recovery impossible in the event of forensic analysis or physical seizure, SATAN2_Cleaner is now evolving towards a public, advanced, and modular solution for cybersecurity professionals, privacy advocates, and anyone seeking reliable and modern data destruction capabilities.

> ⚙️ The core philosophy behind SATAN2_Cleaner is to go far beyond basic wiping or classical shredding techniques. The aim is to integrate a wide range of counter-forensics methods, designed to confuse, slow down, or even block forensic analysis attempts, making data recovery either impossible or excessively time-consuming and costly.

### Key Features & Planned Counter-Forensics Techniques

- Multi-pass shredding (DoD 5220.22-M, Gutmann, Schneier patterns, configurable random passes).
- ATA Secure Erase & Enhanced Secure Erase commands for firmware-level erasure when supported.
- Embedded (nested) encryption: encrypt → overwrite → re-encrypt (configurable multi-layer encryption).
- Triple-layer encryption with dynamic and embedded keys.
- Partition scheme obfuscation (corrupting GPT/MBR, hidden/ghost partitions, invalid partition tables).
- Chained overwrites & misaligned sector wiping (to evade hardware-level recovery and forensic imaging).
- Volume Shadow Copy poisoning (creating corrupted but "valid" snapshots to mislead analysts).
- Filesystem implosion (systematic corruption of superblocks, inodes, and metadata structures).
- Compression/Decompression traps (intentionally corrupted archives as decoys or traps).
- Steganography-based fake data injection (hidden irrelevant data to divert attention).
- File Signature Masking (breaking file headers, magic numbers to prevent carving).
- MACE timestamps scrambling (Modified, Accessed, Created, Entry) — randomization & corruption.
- Restricted/illegal filenames & non-standard Unicode injection (to destabilize forensic tools and parsers).
- Broken and misleading log files, fake system traces (to create false trails and waste analyst's time).
- Cross-linked file fragments & intentional partial overlaps (to prevent file reassembly and integrity analysis).
- Bad sector simulation & allocation (marking areas as defective to avoid overwriting suspicion or carving attempts).
- Decoy file injection ("honey files" and misleading artifacts to misdirect analysis efforts).
- Partial block overwriting (leaving only false fragments to confuse recovery tools).
- Cluster tip wiping & slack space erasure (ensuring no residual data in partially used blocks).
- Disk surface "noise" generation (injection of meaningless data to disrupt entropy analysis and carving).

> ⚙️ Note: SATAN2_Cleaner is currently under private development. The goal is to release a stable, modular, and community-driven version, with pluggable modules for different destruction and anti-forensics strategies — so users can customize and combine techniques based on their specific threat model and operational needs.

## 📚 License

This project is licensed under the GNU Affero General Public License, Version 3.0. For more details, please refer to the LICENSE file in the repository: [Read the license on GitHub](https://github.com/franckferman/SATAN2_Cleaner/blob/stable/LICENSE)

<p align="right">(<a href="#top">🔼 Back to top</a>)</p>

## 📞 Contact

[![ProtonMail][protonmail-shield]](mailto:contact@franckferman.fr)
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/franckferman)
[![Twitter][twitter-shield]](https://www.twitter.com/franckferman)

<p align="right">(<a href="#top">🔼 Back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/franckferman/SATAN2_Cleaner.svg?style=for-the-badge
[contributors-url]: https://github.com/franckferman/SATAN2_Cleaner/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/franckferman/SATAN2_Cleaner.svg?style=for-the-badge
[forks-url]: https://github.com/franckferman/SATAN2_Cleaner/network/members
[stars-shield]: https://img.shields.io/github/stars/franckferman/SATAN2_Cleaner.svg?style=for-the-badge
[stars-url]: https://github.com/franckferman/SATAN2_Cleaner/stargazers
[issues-shield]: https://img.shields.io/github/issues/franckferman/SATAN2_Cleaner.svg?style=for-the-badge
[issues-url]: https://github.com/franckferman/SATAN2_Cleaner/issues
[license-shield]: https://img.shields.io/github/license/franckferman/SATAN2_Cleaner.svg?style=for-the-badge
[license-url]: https://github.com/franckferman/SATAN2_Cleaner/blob/stable/LICENSE
[protonmail-shield]: https://img.shields.io/badge/ProtonMail-8B89CC?style=for-the-badge&logo=protonmail&logoColor=blueviolet
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=blue
[twitter-shield]: https://img.shields.io/badge/-Twitter-black.svg?style=for-the-badge&logo=twitter&colorB=blue

