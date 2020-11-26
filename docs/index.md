---
layout: default
---
# Description

A proof of concept of schema checker for Insights Platform.

## Problem description

1. Research how we can define a schema for tables.
1. Find out where this definition should be with respect to consuming it from various sources like RDS and pipeline services.
1. The goal is to have a defined schema that can be used when creating parquet, reading parquet, and also when converting parquet to pandas dataframe to ensure that all columns have correct types.

## Notes

1. Python libraries can be used since all consumers of this schema are written in python.
1. The schemas should support columns type validation as well.
1. Cooperation with the processing team required.
1. Consider future use case with Amazon RDS.

## Acceptance criteria

1. Implementation task defined

## Additional goals (added by me)

1. Currently there is no known schema for OCP results. In order to implement more checks, make sure OCM UI displays correct results etc. we'd need to have schema for OCP result format.
1. As aggregator developer I'd like to be sure that incoming reports that are consumed from Kafka topic are correct and are not created by malicious code. Incoming messages are thus needed to be checked against schema and additionally for basic content.
1. Security problem: CCX pipeline doesn’t employ validation checks for consumed topics from the Kafka bus

## Why schema check?

### Possible security problems

1. Consuming messages from Kafka
1. Consuming messages from SQS
1. Consuming raw data from any cluster

### Some problems with standard Pandas behaviour

#### Missing values handling

```
Block size,Time to read
1,672512695
2,338152789
3,280886198
4,261732244
5,241726381
6,222869657
7,214296698
8,202491102
9,182263641
10,177141401
```

Is imported as:

```
Data frame
---------------------------
   Block size  Time to read
0           1     672512695
1           2     338152789
2           3     280886198
3           4     261732244
4           5     241726381
5           6     222869657
6           7     214296698
7           8     202491102
8           9     182263641
9          10     177141401

Column types
---------------------------
Block size      int64
Time to read    int64
dtype: object
```

But:

```
Block size,Time to read
1,672512695
2,338152789
3,280886198
4,261732244
5,
6,222869657
7,214296698
8,202491102
9,182263641
10,177141401
```

Is imported as:

```
Data frame
---------------------------
   Block size  Time to read
0           1   672512695.0
1           2   338152789.0
2           3   280886198.0
3           4   261732244.0
4           5           NaN
5           6   222869657.0
6           7   214296698.0
7           8   202491102.0
8           9   182263641.0
9          10   177141401.0

Column types
---------------------------
Block size        int64
Time to read    float64
dtype: object
```

Can be handled by using `Int64` datatype instead of `int64`:

```
Data frame
---------------------------
   Block size  Time to read
0           1     672512695
1           2     338152789
2           3     280886198
3           4     261732244
4           5          <NA>
5           6     222869657
6           7     214296698
7           8     202491102
8           9     182263641
9          10     177141401

Column types
---------------------------
Block size      int64
Time to read    Int64
dtype: object
```

#### Custom format handling

```
20.11.2020 #224
země|měna|množství|kód|kurz
Austrálie|dolar|1|AUD|16,231
Brazílie|real|1|BRL|4,160
Bulharsko|lev|1|BGN|13,467
Čína|žen-min-pi|1|CNY|3,381
Dánsko|koruna|1|DKK|3,536
USA|dolar|1|USD|22,201
Velká Británie|libra|1|GBP|29,464
```

Is processed as:

```
Data frame
---------------------------
                                           20.11.2020 #224
země               měna       množství kód            kurz
Austrálie          dolar      1        AUD          16,231
Brazílie           real       1        BRL           4,160
Bulharsko          lev        1        BGN          13,467
Čína               žen-min-pi 1        CNY           3,381
Dánsko             koruna     1        DKK           3,536
USA                dolar      1        USD          22,201
Velká Británie     libra      1        GBP          29,464

Column types
---------------------------
20.11.2020 #224    object
dtype: object
```

After ignoring first line:

```
Data frame
---------------------------
                  země        měna  množství  kód    kurz
0            Austrálie       dolar         1  AUD  16,231
1             Brazílie        real         1  BRL   4,160
2            Bulharsko         lev         1  BGN  13,467
3                 Čína  žen-min-pi         1  CNY   3,381
4               Dánsko      koruna         1  DKK   3,536

31                 USA       dolar         1  USD  22,201
32      Velká Británie       libra         1  GBP  29,464

Column types
---------------------------
země        object
měna        object
množství     int64
kód         object
kurz        object
dtype: object
```

The last column type is incorrect.


## Possible solutions

### Common schema check libraries

### Schema check libraries based on Pandas

## Proposal
