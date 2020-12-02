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

1. Python libraries can be used since all consumers of this schema are written in Python.
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

### Possible security problems in both pipelines

1. Consuming messages from Kafka
1. Consuming messages from SQS
1. Consuming raw data from any cluster

### Some problems with standard Pandas behaviour

Pandas library can be used to process data in a form of data frames. But there are some shortcomings:

1. missing values handling
1. custom date/time format handling
1. non-standard data formats problems
1. comma vs. dot seperator in FP numeric values

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

But if any value is missing in input data:

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

That table is imported as:

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

* Use schema check whenever possible
* Golgen design: `clojure.spec`
* But we need to work in Python instead
* Ideally one solution for all checks

### Places for schema checks

1. Incomming messages in `platform.upload.buckit` topic in ext. data pipeline
1. Raw data stored in AWS S3 bucket
1. Messages in `ccx.ocp.results` topic in ext. data pipeline
1. Data consumed by Parquet service in int. data pipeline
1. Messages consumed from SQS in int. data pipeline

### Common schema check libraries

1. Schemagic
1. Schema
1. Voluptuous

### Schema check libraries based on Pandas

1. Opulent Pandas
1. Pandas Schema

### Examples

#### Pandas data frame schema checks based on Opulent Pandas

Simple type validations

```python
def validate_data_frame(data_frame):
    schema = Schema({
        Required('Block size'): [TypeValidator(int)],
        Required('Time to read'): [TypeValidator(int)],
        })

    schema.validate(data_frame)


df = pandas.read_csv("integer_values.csv")
print_data_frame(df)
validate_data_frame(df)
```

Custom validator implementation and usage

```python
class PosintValidator(BaseValidator):
    def validate(self, values):
        if not (values > 0).all():
            raise Error("positive integer value expected")


def validate_data_frame(data_frame):

    schema = Schema({
        Required('Block size'): [PosintValidator()],
        Required('Time to read'): [PosintValidator()],
        })

    schema.validate(data_frame)


df = pandas.read_csv("integer_values.csv")
print_data_frame(df)
validate_data_frame(df)
```

Impossible to use `Any`!!!

```python
class PosintValidator(BaseValidator):
    def validate(self, values):
        if not (values > 0).all():
            raise Error("positive integer value expected")


class IntOrNAValidator(BaseValidator):
    def validate(self, values):
        for value in values:
            if (type(value) == np.int64):
                return
            if not (pandas.isna(value)):
                raise Error("Int value or NA expected")


def validate_data_frame(data_frame):

    schema = Schema({
        Required('Block size'): [PosintValidator()],
        Required('Time to read'): [IntOrNAValidator()],
        })

    schema.validate(data_frame)


df = pandas.read_csv("missing_integer_values.csv", dtype={"Time to read": "Int64"})
print_data_frame(df)
validate_data_frame(df)
```

#### Voluptuous

* Validators are simple callables
* Errors are simple exceptions
* Schemas are basic Python data structures
* Designed from the ground up for validating more than just forms
* Consistency

#### Pandas data frame schema checks based on Voluptuous

Very simple example based on checking tuples

```python
def validate_data_frame(data_frame):
    print()

    print("Validation")
    print("---------------------------")

    schema = Schema((int, int, float))

    for record in df.itertuples():
        validate_item(schema, record)


df = pandas.read_csv("missing_integer_values.csv")
print_data_frame(df)
validate_data_frame(df)
```

Real example based on custom schema

```python
def validate_item(schema, data):
    try:
        print("\n")
        # print(schema)
        print(data)
        schema(data._asdict())
        print("pass")
    except Exception as e:
        print(e)


def posint(value):
    if type(value) is not int or value <= 0:
        raise Invalid("positive integer value expected, but got {v} instead".format(v=value))


def posfloat(value):
    if type(value) is not float or value <= 0:
        raise Invalid("positive float value expected, but got {v} instead".format(v=value))


def validate_data_frame(data_frame):
    print()

    print("Validation")
    print("---------------------------")

    schema = Schema({
        "Index": int,
        "_1": posint,
        "_2": posint,
        "Change": Any(str, float),
        "Language": str,
        "Ratings": posfloat,
        "Changep": float,
        })

    for record in df.itertuples():
        validate_item(schema, record)


df = pandas.read_csv("tiobe.tsv", sep="\t")
print_data_frame(df)
validate_data_frame(df)
```

#### Custom schema validation using Voluptuous libary

```python
user = Schema({"name": str,
               "surname": str,
               "id": pos})

validate(user, {"name": "Eda",
                "surname": "Wasserfall",
                "id": 1})

validate(user, {"name": "Eda",
                "id": 1})

validate(user, {"name": "Eda",
                "surname": "Wasserfall",
                "id": 0})
```

Real schema

```python
SCHEMA = S({"name": "metadata",
            "version": Any("3-1-0", "3-2-0", "3-3-0")})

SUMMARY = S(list)

CODE_REPOSITORY = S({"type": str,
                     "url": Url()})

DETAIL = S({Optional("code_repository"): CODE_REPOSITORY,
            Optional("declared_license"): str,
            Optional("declared_licenses"): [str],
            Optional("dependencies"): [str],
            Optional("description"): Any(None, str),
            Optional("devel_dependencies"): [str],
            Optional("ecosystem"): str,
            Optional("homepage"): Url(),
            Optional("name"): str,
            Optional("version"): str})


DETAILS = S([DETAIL])

COMPONENT_METADATA_SCHEMA = S({"_audit": Any(None, AUDIT),
                               Optional("_release"): str,
                               "schema": SCHEMA,
                               "status": STATUS,
                               "summary": SUMMARY,
"details": DETAILS})
```

## Final proposal

1. Create Git repository in Insights group with all schemas
1. Use Voluptuous library as it is the most stable & versatile solution right now
1. Use schema versioning
1. All structured data can be validated, including rule content
1. Probably worth to add schema version into data as well (where applicable!)

## Possible problems

1. Missing versioning + problems with updates
1. Schema check might be kinda slow, but it is scalable thing

## Action items

1. Demo
1. Epic for tracking all schema checks that needs to be implemented
1. Task to create Git repository with schemas
1. Task to write description about incomming messages in `platform.upload.buckit`
1. Task to write description about incomming messages in `ccx.ocp.results`
1. Task to write description about rule content (YAML files etc.)
1. Task to write description about incomming messages in SQS
1. Task to create schema for data to be consumed by Parquet service
1. Task to create schema for incomming messages in `platform.upload.buckit`
1. Task to create schema for incomming messages in `ccx.ocp.results`
1. Task to create schemas for rule content (YAML files etc.)
1. Task to create schema for incomming messages in SQS
1. Task to create schema for data to be consumed by Parquet service
1. Spikes to investigate possibility to version messages, content etc.
