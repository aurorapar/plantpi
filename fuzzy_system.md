## Input variables

|Name|Input range|
|----|-----------|
|Temperature|32-212|
|Humidity|0-100|
|Water|0-20|

## Output variables

|Name|Output range|
|----|------------|
|Pump|0-100|
|Fan|0-100|


## Fuzzy sets

### Inputs

Temperature:

- Low: 0,0,50,65
- Normal: 50,65,75,80
- High: 80,90,212,212

Humidity:

- Low: 0,0,20,35
- Normal: 20,35,50,60
- High: 55,70,100,100

Water:

- Low:  0,0,3,5
- Normal: 3,5,10,12
- High: 11,15,20,20

### Outputs

Pump:
- Low: 0,0,30,70
- High: 30,70,100,100

Fan:
- Low: 0,0,35,65
- High: 35,65,100,100


## Rule set

IF Temperature is High OR Humidity is High -> Fan is 

IF Humidity is Low OR Temperature is Low -> Fan is Low

IF Water is Low -> Pump is High

IF Water is High -> Pump is Low
