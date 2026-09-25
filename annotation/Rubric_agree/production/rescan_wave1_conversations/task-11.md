# task 11 — the full conversation

Companion to the wave file. Every block, numbered, with the blocks carrying a proposed cell marked. Open it when a decision step asks for the request, the prior turn, the next block, the whole turn or the whole block.

## b0 · human

```
I'm working on HMDA data and using dask to clean and analyze the data but I'm stumped on why my code isnt replacing any of the values in the dataframe.
I've tried using the replace function by itself and it doesnt work
data["co_applicant_ethnicity_1"] = data["co_applicant_ethnicity_1"].replace([1,11,12,13,14,2,3,4,5],
["<REDACTED> or Latino","Mexican","Puerto Rican","Cuban","Other <REDACTED> or Latino","Not <REDACTED> or Latino",
"Information not provided by applicant in mail, internet, or telephone application",
"Not applicable","No co-applicant"],regex=True)
```

## b1 · ai  ←  a proposed cell sits on this block

```
The issue is likely that you're using regex=True when you don't need it. The regex=True parameter tells pandas/dask to treat your replacement patterns as regular expressions, but you're trying to do direct value mapping.
Here are a few solutions:
Option 1: Remove regex=True (simplest fix)
python
data["co_applicant_ethnicity_1"] = data["co_applicant_ethnicity_1"].replace([1,11,12,13,14,2,3,4,5],
["<REDACTED> or Latino","Mexican","Puerto Rican","Cuban","Other <REDACTED> or Latino","Not <REDACTED> or Latino",
"Information not provided by applicant in mail, internet, or telephone application",
"Not applicable","No co-applicant"])
Option 2: Use dictionary mapping (more readable)
python
ethnicity_mapping = {
    1: "<REDACTED> or <REDACTED>",
    11: "<REDACTED>", 
    12: "<REDACTED>",
    13: "<REDACTED>",
    14: "Other <REDACTED> or <REDACTED>",
    2: "Not <REDACTED> or <REDACTED>",
    3: "Information not provided by applicant in mail, internet, or telephone application",
    4: "Not applicable",
    5: "No co-applicant"
}

data["co_applicant_ethnicity_1"] = data["co_applicant_ethnicity_1"].replace(ethnicity_mapping)
Option 3: Use map() if you want to ensure only mapped values are kept
python
data["co_applicant_ethnicity_1"] = data["co_applicant_ethnicity_1"].map(ethnicity_mapping)
Additional troubleshooting steps:
Check your data types - Make sure the column contains integers, not strings:
python
print(data["co_applicant_ethnicity_1"].dtype)
print(data["co_applicant_ethnicity_1"].unique())
Force compute if using dask - Dask operations are lazy by default:
python
data["co_applicant_ethnicity_1"] = data["co_applicant_ethnicity_1"].replace(ethnicity_mapping)
data = <REDACTED>()  # or data.persist()
Check for missing values or unexpected data types:
python
print(data["co_applicant_ethnicity_1"].value_counts())
The dictionary approach (Option 2) is generally preferred as it's more readable and less error-prone than maintaining two separate lists.
```

