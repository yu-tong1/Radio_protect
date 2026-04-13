# Radiation Protection Traditional Chinese Medicine Component Screening System

## 1. System Overview

This system is a radiation protection traditional Chinese medicine (TCM) component screening platform developed based on the Flask framework. It aims to help researchers quickly screen TCM components and formulas with radiation protection effects. The system integrates multiple functional modules, including compound screening, formula screening, heavy metal induced excretion prediction, etc., providing strong tool support for radiation protection research.

### 1.1 Technical Architecture

- **Backend**: Flask framework
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Data Processing**: Pandas, RDKit (molecular fingerprint generation)
- **Machine Learning**: Using joblib to load models
- **API Integration**: BATMAN2 API (target prediction)

### 1.2 System Directory Structure

```
website/
├── Compound screening results/    # Screening results storage directory
├── templates/                      # Frontend templates
│   ├── web_database_files/         # Static resource files
│   ├── Compound_screening.html     # Compound screening page
│   ├── Herb_and_Formula_screening.html  # TCM and formula screening page
│   ├── Herb_miRNA_data.html        # TCM miRNA data page
│   ├── Heavy_Metal_Induced_Excretion_Compound_Screening.html  # Heavy metal induced excretion screening page
│   └── AI_Analysis.html            # AI analysis page
├── Compound_Induced_Excretion_Prediction.py  # Heavy metal induced excretion prediction module
├── Compound_screening_cancer.py    # Compound screening in cancer mode
├── Compound_screening_normal.py    # Compound screening in normal mode
├── Herb_and_Formula_screening.py   # TCM and formula screening module
├── AI_Analysis.py                  # AI analysis module
├── U_RF_model.joblib               # Heavy metal induced excretion prediction model
├── app.py                          # Main application
└── Test-file Zisu.csv                # Test case file
```

## 2. Functional Modules

### 2.1 Radiation Protection Compound Screening (RadioProtect Compound Screening)

**Function Description**:
- Upload TCM component CSV files to screen compounds with radiation protection effects
- Support two screening modes: normal mode and cancer mode
- Generate matched and unmatched result files
- Provide result download functionality

**Technical Implementation**:
- Use `Compound_screening_normal.py` and `Compound_screening_cancer.py` to handle screening in different modes
- Perform data processing and matching through pandas
- Call BATMAN2 API for target prediction

### 2.2 Radiation Protection Formula Screening (RadioProtect Formula Screening)

**Function Description**:
- Provide 17 radiation protection TCMs and their components
- Search for related TCMs and formulas based on radiation protection compounds
- Display the number of radiation protection compounds contained in formulas

**Technical Implementation**:
- Use `Herb_and_Formula_screening.py` to implement screening logic
- Count the number of radiation protection compounds in formulas through Counter
- Load data from `herb_batman_matched.csv` and `formula_batman_matched.csv`

### 2.3 Heavy Metal Induced Excretion Compound Screening

**Function Description**:
- Upload CSV files containing SMILES structures
- Predict compounds' heavy metal induced excretion ability
- Display prediction results, including compound structure, prediction value, and fingerprint type used

**Technical Implementation**:
- Use `Compound_Induced_Excretion_Prediction.py` to implement prediction functionality
- Generate molecular fingerprints based on RDKit (3D pharmacophore fingerprint, 2D pharmacophore fingerprint, Morgan fingerprint)
- Use pre-trained random forest model for prediction

### 2.4 TCM miRNA Data (Herb miRNA data)

**Function Description**:
- Display TCM miRNA related data

**Technical Implementation**:
- Display miRNA data through frontend pages

### 2.5 AI Analysis of Screening Results

**Function Description**:
- Intelligently analyze compound screening results and generate professional analysis reports
- Support analysis of different radiation types (X-rays, γ-rays, α-particles, Heavy Metal, protons)
- Provide API configuration options, supporting multiple AI models
- Allow custom system prompts to adjust analysis direction

**Technical Implementation**:
- Use `AI_Analysis.py` to implement backend analysis logic
- Provide user interaction interface through frontend page `AI_Analysis.html`
- Integrate OpenAI SDK to call AI models for analysis
- Read screening result files from `Compound screening results` directory
- Group by medicinal materials, count main genes, pathways, compound types, etc.
- Generate structured analysis reports, including compound type enrichment, main gene pathways, drug likeness and oral bioavailability, protection mechanisms, etc.

## 3. Operation Guide

### 3.1 System Startup

1. Ensure that the required dependency packages are installed:
   ```
   pip install flask pandas rdkit joblib requests openai sklearn numpy
   ```

   **Note**: If using the AI analysis function, you need to install the openai library additionally.

2. Enter the website directory and run the application:
   ```
   python app.py
   ```

3. Open a browser and visit http://localhost:5000

### 3.2 Radiation Protection Compound Screening Operation Steps

1. Click "Tools" > "RadioProtect Compound Screening" in the navigation bar
2. Select the screening mode (normal or cancer) on the page
3. Click the "Select File" button to upload a CSV file containing TCM components
4. Click the "Submit" button to submit
5. Wait for the system to complete processing
6. View the screening results, including matched and unmatched compounds
7. Click the "Download" button to download the result files

### 3.3 Radiation Protection Formula Screening Operation Steps

1. Click "Tools" > "RadioProtect Formula Screening" in the navigation bar
2. The system automatically loads and displays the screening results
3. View the formula screening results in normal mode and cancer mode
4. View the related TCM list

### 3.4 Heavy Metal Induced Excretion Compound Screening Operation Steps

1. Click "Tools" > "Heavy Metal Decorporation Compound Screening" in the navigation bar
2. Click the "Select File" button to upload a CSV file containing SMILES structures
3. Click the "Submit" button to submit
4. Wait for the system to complete processing
5. View the prediction results, including compound structure, prediction value, and fingerprint type used

### 3.5 TCM miRNA Data Operation Steps

1. Click "Tools" > "Plant microRNA Targets in Human" in the navigation bar
2. Enter the external link page for miRNA target prediction

### 3.6 AI Analysis of Screening Results Operation Steps

1. Click "Tools" > "AI Analysis" in the navigation bar
2. Select the analysis mode (Compound AI Analysis) on the page
3. Select the sub-mode (Cancer Mode or Normal Mode)
4. Select the radiation type (available radiation types vary depending on the selected mode)
5. Configure API settings:
   - Enter API Key
   - Set API Base URL (default is https://api.deepseek.com)
   - Select AI model
6. Modify the system prompt as needed to adjust the analysis direction
7. Click the "Run AI Analysis" button to start analysis
8. Wait for the system to complete processing and view the AI-generated analysis report

**Note**: To use the AI analysis function, you need to first perform compound screening to generate screening result files. The AI will read these files from the `Compound screening results` directory for analysis.

## 4. Data Format Requirements

### 4.1 Radiation Protection Compound Screening Data Format

CSV files should contain the following columns (any one):
- CID columns: `cid`, `CID`, `Cid`, `cID`, `pubchem_id`, `PubChem_id`, `PubChem_ID`
- Gene name columns: `gene_name`, `Gene_name`

**Example file**: `Test-file Zisu.csv`

### 4.2 Heavy Metal Induced Excretion Compound Screening Data Format

CSV files should contain a `SMILE` column for storing compound SMILES structures.

## 5. Result Interpretation

### 5.1 Radiation Protection Compound Screening Results

- **Matching results**: Contain compounds that match radiation protection targets
- **Unmapped results**: Unmatched compounds

Result files are saved in the `Compound screening results` directory, named in the format:
- Normal mode: `Matching normal results of [filename] ingredients.csv`
- Cancer mode: `Matching cancer results of [filename] ingredients.csv`

### 5.2 Radiation Protection Formula Screening Results

- **Normal Formula**: Formula screening results in normal mode, showing formula names and the number of radiation protection compounds they contain
- **Cancer Formula**: Formula screening results in cancer mode
- **Herb Normal**: TCM list in normal mode
- **Herb Cancer**: TCM list in cancer mode

### 5.3 Heavy Metal Induced Excretion Compound Screening Results

- **smiles**: Compound SMILES structure
- **prediction**: Prediction value (1 indicates having heavy metal induced excretion ability, 0 indicates not having)
- **fp_type**: Fingerprint type used (3d_pharmacophore, 2d_pharmacophore, or morgan)

## 6. System Configuration and Maintenance

### 6.1 Configuration Files

- **app.py**: Main configuration file, containing routes and core functions
- **UPLOAD_FOLDER**: Upload file storage directory (default is 'uploads')
- **BATMAN2_API_URL**: BATMAN2 API address (default is 'http://batman2api.cloudna.cn/queryTarget')

### 6.2 Model Files

- **U_RF_model.joblib**: Heavy metal induced excretion prediction model

### 6.3 Data Files

- **DEGs_normal.csv**: Differentially expressed genes in normal mode
- **DEGs_cancer.csv**: Differentially expressed genes in cancer mode
- **herb_ingredient.csv**: TCM component data
- **results of target matching normal.csv**: Target matching results in normal mode
- **results of target matching cancer.csv**: Target matching results in cancer mode
- **herb_batman_matched.csv**: TCM and BATMAN matching data
- **formula_batman_matched.csv**: Formula and BATMAN matching data

## 7. Common Issues and Solutions

### 7.1 Upload File Failure

- **Issue**: The system prompts an error after uploading a file
- **Solution**: Check if the file format is correct and ensure the file contains the required columns (such as CID or SMILE)

### 7.2 Empty Screening Results

- **Issue**: No matched compounds after screening
- **Solution**: Check if the CID or gene names in the input file are correct and ensure the data format meets the requirements

### 7.3 Slow System Response

- **Issue**: The system responds slowly when processing large files
- **Solution**: Reduce file size or process data in batches

### 7.4 API Call Failure

- **Issue**: BATMAN2 API call failure
- **Solution**: Check network connection and ensure the API address is correct

## 8. Example Usage Flow

### 8.1 Using Test File for Radiation Protection Compound Screening

1. After starting the system, enter the "RadioProtect Compound Screening" page
2. Select "normal" mode
3. Upload "Test-file Zisu.csv"
4. Click the "Submit" button
5. View the screening results and download "Matching normal results of Test-file Zisu ingredients.csv"

### 8.2 Performing Heavy Metal Induced Excretion Compound Screening

1. Prepare a CSV file containing SMILES structures
2. Enter the "Heavy Metal Decorporation Compound Screening" page
3. Upload "Test-file Zisu.csv"
4. Click the "Submit" button
5. View the prediction results and analyze the compounds' heavy metal induced excretion ability

## 9. Technical Support

- **Contact**: Professor 马家骅 Email: jiahuama@swust.edu.cn
- **Developers**:
            马家骅 (PhD, Professor, School of Life Science and Agronomy, Southwest University of Science and Technology);
            柒世龙 (Master's student, School of Life Science and Agronomy, Southwest University of Science and Technology);
            周阳 (Undergraduate student, School of Life Science and Agronomy, Southwest University of Science and Technology).
- **Institution**: College of Life Sciences and Agri-forestry, Southwest University of Science and Technology
- **Project**: Radiation Protection TCM Component Screening System

## 10. Update Log

- **2026/4/13**: Added AI analysis of screening results function, supporting intelligent analysis of compound screening results and generating professional reports
- **2026/3/30**: Modified Gene name-based mapping logic to adapt to BATMAN API data
- **2026/3/16**: Added radiation protection formula screening function
- **2026/3/14**: Added radiation protection TCM compound screening function