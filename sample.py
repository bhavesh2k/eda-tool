import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"],
    "Age": [29, 35, 28, 42, 31, 38, 25],
    "Salary": [70000, 85000, None, 120000, 90000, 110000, 65000],
    "Department": ["Sales", "Engineering", "HR", "Engineering", "Marketing", None, "Sales"],
    "JoiningDate": ["2020-05-10", "2018-08-21", "2021-01-15", "2010-03-30", "2019-11-05", "2015-07-22", "2022-06-01"]
}

df = pd.DataFrame(data)
df.to_csv("test_data.csv", index=False)
