# Water Pump Functionality Prediction

## Project Overview
This proejct develops machine learning models to predict the functionality status of water pumps across Tanzania based on a variety of features including location, water quality, management structure, and technical specifications.  

This project addresses a critical infrastructure challenge: identifying which water pumps are functional, which need repairs, and which are non-functional to improve maintenance operations and ensure communities have access to clean water.

---

## Competition Link
[DrivenData - Pump it Up: Data Mining the Water Table](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/)

---

## Project Goals
- Develop classification models to predict three target classes:  
  - **Functional water pumps**  
  - **Water pumps that need repair**  
  - **Non-functional water pumps**
- Analyze which factors most strongly influence water pump functionality
- Create geospatial visualizations to communicate findings effectively
- Deploy a simple dashboard to showcase models and insights

---

## Data Description

### Dataset Source
The data comes from **Taarifa** and the **Tanzanian Ministry of Water**, which aggregates information about water points across Tanzania.

### Features Overview
The dataset contains **40+ columns** representing:
- **Geographic information**: coordinates, region, basin  
- **Technical specifications**: pump type, extraction method  
- **Management details**: installer, funder, payment type  
- **Water characteristics**: quality, quantity, source  
- **Temporal information**: construction year, recording date  

### Target Variable
**`status_group`**: The operating condition of the waterpoint with three possible values:
- `functional` → operational with no repairs needed  
- `functional needs repair` → operational but needs repairs  
- `non functional` → not operational  

## Acknowledgements

We would like to express our sincere gratitude to the following:  

- **ReDI School of Digital Integration** for providing the opportunity, guidance, and learning environment that made this project possible.  
- **DrivenData** for organizing the *Pump it Up: Data Mining the Water Table* competition and providing an engaging platform to apply data science for social good.  
- **Taarifa** and the **Tanzanian Ministry of Water** for making the dataset available, enabling research and innovation aimed at improving water infrastructure.  
- The broader **open-source community** for providing the tools, libraries, and frameworks that make projects like this possible.  
- Our peers, mentors, and collaborators for their valuable feedback, support, and encouragement throughout this project.  
