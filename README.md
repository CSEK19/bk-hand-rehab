# BKHandRehab: A Gesture-Based Gaming Application for Post-Stroke Hand Rehabilitation

## About this Project

Welcome to BKHandRehab, our capstone project dedicated to revolutionizing post-stroke hand rehabilitation through a captivating hand gesture-based gaming application. Leveraging the Leap Motion Controller for precise hand skeleton extraction and incorporating a robust SVM model for gesture recognition, we aim to provide an engaging and effective rehabilitation experience.

**Note:** The current version of the application is compatible with Windows 10/11 only.

## Documentation

For an in-depth understanding of our project, please refer to our comprehensive project report [here](final_report.pdf).

Explore the features and capabilities of our application by watching the demo video [here](demo.mp4).

## Prerequisites

Before getting started, ensure you have the following prerequisites:

1. **Leap Motion Controller**
2. **Leap Motion Hand Tracking Software**  
Download the installation file [here](https://www.ultraleap.com/tracking/gemini-hand-tracking-platform/).

## Installation

1. Create a Conda environment with Python 3.9 and activate it.

    ```bash
    conda create -n myenv python=3.9
    conda activate myenv
    ```

2. Navigate to the code directory and install dependencies.

    ```bash
    cd bk_hand_rehab
    pip install -r requirements.txt
    ```

## Running the Application

Execute the following command to run the application:

```bash
python main.py
```
##
Feel free to reach out if you encounter any issues or have suggestions for improvement. We hope BKHandRehab contributes positively to the field of hand rehabilitation.