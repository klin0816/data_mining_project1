# Data Mining Project 1

## Files

1. `data_processing.py`: Process dataset that made produced from 'IBM-Quest-Generator.EXE'
2. `apriori.py`: Implement apriori algorithm
3. `fp_growth.py`: Implement apriori algorihtm
4. `dataset/`: Folder contains dataset
	* `data.ntrans_5.tlen_10.nitems_0.02`: Dataset produced from 'IBM-Quest-Generator.exe'
	* `data.ntrans_5.tlen_10.nitems_0.02_pre`: Dataset processed for `apriori.py` and `fp_growth.py`
	* `data.ntrans_5.tlen_10.nitems_0.02_p`: Dataset processed for association analysis tools (spmf for this project)
	* `pat.ntrans_5.tlen_10.nitems_0.02`: Pat file produced from 'IBM-Quest-Generator.exe'
	* `data_test`: Small dataset for testing
5. `result/`: Folder contains result from spmf and my two codes 
	* `result_apriori_spmf`: result produced from spmf
	* `result_fp_growth_spmf`: result produced from spmf
	* `result_apriori`: result produced from `apriori.py`
	* `result_fp_growth`: result produced from `fp_growth.py`
6. `IBM-Quest-Generator.exe`: Dataset Producer, provided by course
7. `spmf.jar`: Association Analysis tools

## Produce and Process Dataset

Execute `IBM-Quest-Generator.exe` on Windows to get dataset. For my dataset:
```
"IBM-Quest-Generator.exe" -ntrans 5 -tlens 10 -nitems 0.02
```
and will get `data.ntrans_5.tlen_10.nitems_0.02` and `pat.ntrans_5.tlen_10.nitems_0.02`,
we used only data file in this project

After get dataset, you need to do some process to make dataset suitable for program and spmf tools.
```
python3 data_processing.py data.ntrans_5.tlen_10.nitems_0.02
```
It will produce two files: 
1. `data.ntrans_5.tlen_10.nitems_0.02_pre`: stored dataset in list
2. `data.ntrans_5.tlen_10.nitems_0.02_p`: stored dataset in format that spmf needs

## Apriori

```
python3 apriori.py [dataset] [min_sup] [min_conf] > [result_file]
```
[dataset] : path of dataset<br/>
[min_sup] : minimum support rate (0.0-1.0)<br/>
[min_conf] : minimum confidence rate (0.0-1.0 and >= min_sup)<br/>
[result_file] : path of file to save result<br/>
for example result in `result/`
```
python3 apriori.py dataset/data.ntrans_5.tlen_10.nitems_0.02_pre 0.4 0.4 > result/result_apriori
```

## FP-growth

```
python3 fp_growth.py [dataset] [min_sup] [min_conf] > [result_file]
```
[dataset] : path of dataset<br/>
[min_sup] : minimum support rate (0.0-1.0)<br/>
[min_conf] : minimum confidence rate (0.0-1.0 and >= min_sup)<br/>
[result_file] : path of file to save result<br/>
for example result in `result/`
```
python3 fp_growth.py dataset/data.ntrans_5.tlen_10.nitems_0.02_pre 0.4 0.4 > result/result_fp_growth
```

## Comparison

1. Apriori
in `result/result_apriori_spmf`:
```
...
9 17 ==> 8 #SUP: 2004 #CONF: 0.8016
8 17 ==> 9 #SUP: 2004 #CONF: 0.7392106233862044
...
```

in `result/result_apriori`:
```
...
'{8, 17}->{9}': {'#CONF': 0.7392106233862044, '#SUP': 2004},
...
'{9, 17}->{8}': {'#CONF': 0.8016, '#SUP': 2004},
...
```
The result of confidence and sup are same,
only the presentation and order are different.

2. FP-growth
in `result/result_fp_growth_spmf`:
```
...
9 17 ==> 8 #SUP: 2004 #CONF: 0.8016
8 17 ==> 9 #SUP: 2004 #CONF: 0.7392106233862044
...
```

in `result/result_fp_growth`:
```
...
'{17, 9}->{8}': {'#CONF': 0.8016, '#SUP': 2004},
...
'{8, 17}->{9}': {'#CONF': 0.7392106233862044, '#SUP': 2004},
...
```
The result of confidence and sup are same,
only the presentation and order are different.
Like `9 17 ==> 8` in spmf will become `'{17, 9}->{8}'`
