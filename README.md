# Natural Language Querying of Structured Data

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

## Overview
Welcome to the repository for the **Natural Language to Structured Data Querying** methodology, developed in conjunction with the **FUTURAL** project. 


This repository provides a fully open-source pipeline for translating natural language questions into executable queries on highly structured, non-textual datasets. Unlike traditional Retrieval-Augmented Generation (RAG) pipelines that struggle with numerical and structured information, our approach trains a compact Large Language Model (DeepSeek R1-Distill-8B) to generate accurate, executable data queries directly from user prompts.

By utilizing QLoRA with 4-bit quantization, this methodology ensures high-accuracy, privacy-preserving question-answering that can be deployed entirely on commodity hardware, bypassing the high operational costs and privacy concerns associated with massive proprietary LLMs.

## Key Features
- **Synthetic Training-Data Generation:** A principled pipeline to produce diverse, high-quality question-answer pairs capturing localized user intent and dataset semantics.
- **Cost-Effective Fine-Tuning:** Leverages advanced parameter-efficient fine-tuning (PEFT) on 7-8B parameter models, enabling high precision during deployment without external API dependencies.
- **Robust Generalization:** Demonstrates high accuracy across monolingual, multilingual, and unseen-location scenarios.
- **Resource-Efficient Deployment:** Designed to be lightweight and deployable on resource-constrained environments (e.g., standard laptops), making it highly accessible for stakeholders and edge deployments.

## Methodology Architecture

<p align="center">
  <img src="https://mermaid.ink/img/Z3JhcGggVEQKICAgIEFbTmF0dXJhbCBMYW5ndWFnZSBRdWVyeV0gLS0-fERpc3RpbGxlZCBMTE18IEIoUXVlcnkgR2VuZXJhdG9yKQogICAgQiAtLT58R2VuZXJhdGVkIEV4ZWN1dGFibGUgUXVlcnl8IENbKFN0cnVjdHVyZWQgRGF0YXNldCldCiAgICBDIC0tPnxSZXR1cm4gUmVzdWx0c3wgRFtTdGFrZWhvbGRlciBBbnN3ZXJdCiAgICBzdHlsZSBBIGZpbGw6I2UxZjVmZSxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4CiAgICBzdHlsZSBDIGZpbGw6I2ZmZjNlMCxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4CiAgICBzdHlsZSBEIGZpbGw6I2U4ZjVlOSxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4" alt="Methodology Architecture Flowchart" />
</p>

## Use Case: Durangaldea Accessibility
The methodology is currently applied and evaluated on a comprehensive rural accessibility dataset from Durangaldea, Spain. The dataset tracks coordinates and travel times (walking, cycling, driving) to essential services (hospitals, supermarkets, and pharmacies). The system acts as a natural-language interface for stakeholders to perform Quality of Life assessments and demographic settlement analysis.

## Repository Structure

```text
.
├── deploy/                  # Deployment scripts and server utilities
│   ├── ngrok                # Network tunneling for exposing local servers
│   └── run_backend.slurm    # SLURM batch script for running the backend on a cluster
├── scripts/                 # Data preparation and model training
│   ├── finetune_model.py              # Fine-tuning script (DeepSeek via QLoRA)
│   ├── generate_dataset.py            # Synthetic QA data generation pipeline
│   └── generate_distance_dataset.py   # Distance & accessibility metric generation
└── src/                     # Core application source code
    ├── app.py               # Main application entry point / UI
    ├── filters.py           # Structured dataset filtering logic
    ├── location_script.py   # Coordinate and location tracking logic
    └── utils.py             # General purpose utility functions
```

## Getting Started

### Prerequisites
- Python 3.8+
- PyTorch with CUDA support (for model fine-tuning and fast inference)
- SLURM workload manager (optional, if using the provided cluster scripts)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/valy3124/Futural_UNSTPB.git
   cd Futural_UNSTPB
   ```

### Usage
- **Data Generation:** Run the scripts in the `scripts/` directory to generate your custom synthetic training pairs.
- **Fine-Tuning:** Execute `scripts/finetune_model.py` to initiate the QLoRA 4-bit fine-tuning process.
- **Deployment:** Use `deploy/run_backend.slurm` to start up the model backend on a SLURM-managed cluster, and execute `src/app.py` to launch the user interface.

## Research & Methodology 
This repository implements the methodologies discussed in our research on querying structured data through natural language using language models. It emphasizes fully automated workflows and independence from external APIs at deployment time.
