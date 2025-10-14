## Notebooks

This folder contains any jupyter notebooks.


## Analysis report

### columns to be input
Because those are highly correlated according to the chi squre test or some patttern was observed with status and region
- source
- management
- quality_group
- payment
- region
- payment_type
- quantity_group
- construction_year
- gps_height
- population


### columns to be output
- status_group


### Columns alernatively used when the model's performance isn't enough. 
- payment
- extraction type
- management_group
- water_quality
- quantity
- source_type
- source_class
- waterpoint_type
- waterpoint_type_group
- longitude 
- latitude


### columns to dropped
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



### Don't know yet
Because correlation can be high according to the chi square test, but sounds like not so important.
- public_meeting
- scheme_management
- permit

### dropping missing values
- drop rows if construction_year == 0 (construction_year == 0 if population == 0, so simply data isn't recorded).
If this infleunces the model performance, the following missing value filling scheme can be applied.

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