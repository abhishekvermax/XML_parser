data= {
  "name": "root",
  "type": {"sample":"text"},
  "teacher": [
    {
      "name": "properties",
      "type": "feature",
      "father": [
        {
          "name": "print",
          "type": "feature",
          "children": [
            {
              "name": "graphic print",
              "type": "feature",
              "inherits": "true"
            },
            {
              "name": "striped print",
              "type": "feature",
              "inherits": "true",
              "sister": [
                {
                  "name": "pinstriped",
                  "type": "feature",
                  "inherits": "true"
                },
                {
                  "name": "light stripe",
                  "type": "feature",
                  "inherits": "true"
                },
                {
                  "name": "wide stripe",
                  "type": "feature",
                  "inherits": "true"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "colours",
      "type": "colour",
      "father": [
        {
          "name": "main colours",
          "type": "colour",
          "reacher": [
            {
              "name": "black",
              "type": "colour",
              "sister": [
                {
                  "name": "light black",
                  "type": "colour",
                  "inherits": "true"
                },
                {
                  "name": "blue black",
                  "type": "colour",
                  "inherits": "true"
                }
              ]
            },
            {
              "name": "red",
              "type": "colour",
              "teacher": [
                {
                  "name": "bright red",
                  "type": "colour",
                  "inherits": "true"
                },
                {
                  "name": "light red",
                  "type": "colour"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "genders",
      "type": "gender",
      "children": [
        {
          "name": "female",
          "type": "gender"
        },
        {
          "name": "male",
          "type": "gender"
        }
      ]
    }
  ]
}

import pandas as pd
def nested_parser(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in nested_parser(value, pre + [key+'_dict']):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for idx,v in enumerate(value):
                    for d in nested_parser(v, pre + [key+'_array_'+str(idx)]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]
lst = [i for i in nested_parser(data)]
max_dept_elem = len(max(lst, key=len))
padded_list = [i[:-1]+ [None] * (max_dept_elem-len(i)) + i[-1:] if len(i)<max_dept_elem else i for i in lst]
df = pd.DataFrame(padded_list)
df_cols = ["root_level_"+str(col) for col in df.columns.values]
df.columns = df_cols
print(df)





rows = []
def processData(data, prefix = "root", row = dict(), doEmit = True):
    #add a column for each new attribute
    hasChildren = False
    for k in data.keys():
        if type(data[k]) == str:
            colName = prefix + "_" + k
            row[colName] = data[k]
        elif type(data[k]) == dict:
            prefix += "_" + k
            child = data[k]
            processData(child,prefix = prefix, row = row, doEmit = False);
    for k in data.keys():
        if type(data[k]) == list:
            hasChildren = True
            #update prefix
            prefix += "_" + k
            for child in data[k]:
                processData(child,prefix = prefix, row = row.copy());
    if not hasChildren and doEmit:
        #finished row when there is no child
        rows.append(row);
        return


processData(data)
df = pd.DataFrame(rows)
print(df)

