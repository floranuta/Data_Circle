## Notebooks

This folder contains any jupyter notebooks.


## Data cleaning proposal

My data cleaning proposal is as below:    
- First of all, **remove invalid data**, meaning remove the row if "date_recorded" - "construction_year" < 0.  
Then, the following attempt can be apply while sseing the model performance.  

1. First attempt: using the following columns and see the model performance. Click [here](#columns-to-be-used) to see the columns to be used.
2. Second attempt: Using source in stead of "source" and see the model performance. Click [here](#columns-alernatively-used) to see more details.
3. Third attempt: Add a column "construction_year" and remove the rows where the value is zero. And then see the model performance.
4. Forth attempt: Add a column "construction_year" and fill the zeros with alternative values. And see the model performance. Click [here](#filling-missing-values) to see how to fill the zero values.

Reason why I propose this attempts:   
- If the data is complete and no null values, the model could learn well even though the data size is small.
- Functionality is highly correlated with region, so the model could learn well without pump age.
- Filling zero values in "construction_year" could change the data distribution, so trying with low risk strategy can be efficient. 
- Columns "source", "extraction_type_class", and "waterpoint_type_group" are correlated each other, so using one of them would be enough. I assume "source" is more correlated with region then other two columns and overlapped information might be redundant, so I'd try with "extraction_type_class" first.


### Columns to be used
Because those are highly correlated according to the chi squre test or some patttern was observed with status and region
- quantity_group
- region
- payment_type
- extraction_type_class
- management
- quality_group
- gps_height
- status_group



### Columns alernatively used 
- source or waterpoint_type_group (alternative of extraction_type because those are highly correlated with extraction_type)
- basin or longitude & latutude (alternative of region because those are highly correlated with region)
- payment 
- water_quality
- quantity



### Columns to dropped
- constrction_year
- population
- basin (highly associate wuth region, so we don't need the same information)
- date_recorded (too same values)
- funder (too unique values)
- installer (too unique values)
- wtp_name (too unique values)
- subvillage (region is enough)
- lga (region is enough)
- ward (region is enough)
- recorded_by (too same values)
- scheme_name (too unique values)
- amount_tsh (inconsistent with water quantity, so better to stick to quantity)
- distirct_code (region is enough, also we can encode region into numerical data, so not must-have)
- id
- num_private (we can't explain what it is)
- management_group



### Filling missing values
- construction_year:
    - Dodoma
        1. fill with mean of construction_year (because it wouldn't change distribution so much)
        2. fill with the oldest year (I assume there is no data bacsue it's old)
        3. fill with the 1980 (because the capital transition project started 1974 and failed by 2000)[https://en.wikipedia.org/wiki/Dodoma]
    - Kagera
        1. fill with mean of construction_year (because it wouldn't change distribution so much)
        2. fill with the oldest year (The same reason above ane because there was war with Uganda between 1978 - 1979, so I assume most are broken, but still remines)[https://en.wikipedia.org/wiki/Uganda%E2%80%93Tanzania_War]
    - Mbeya
        1. fill with mean of construction_year (because it wouldn't change distribution so much)
        2. fill with the oldest year (I assume there is no data bacsue it's old)
        3. fill with 1978 (because population was increased between 1978 - 1988)[https://en.wikipedia.org/wiki/Mbeya_Region]
    - Tabora
        1. fill with mean of construction_year (because it wouldn't change distribution so much)
        2. fill with the oldest year (I assume there is no data bacsue it's old)
        3. fill with 2002 (because population was increased between 2002 - 2012)[https://en.wikipedia.org/wiki/Tabora_Region]
        
- other missing categorical data
    - fill with unknown