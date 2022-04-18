# mz_calen
A calendar program with UI developed by PyQt5 and python 

# dependence
You only need to install the python and pyqt5.

# how to use
You can use `python main.py` to open the UI. 
The file `item.md` and `date.md` are the data file which record your plan.

## add one plan
If you want to add a new plan, you can point the `new` button and input the code as the follow
``` markdown
# CLASS
## ITEM1
* this is annotation1
* the time can be defined as:
*   1. time point, such as `2022-04-18`
*   2. a period of time, such as `2022-04-18 > 2023-04-18`
*   3. some time points at a period of time, such as 
*      `2022-04-18 > 2023-04-18 > c10, w3, m1, a4`.
*      It means the time points per 10 days, per Wednesday, or 1st day of per month from 2022-04-18 to 2023-04-18, or 4th day after 2022-04-18.
*      The `c10` means a cycle of 10 days.
*      The `w3` means per 3rd day of a week.
*      The `m1` means per 1st day of a month.
*      The `a4` means the 4th day after the start time.
* You can add many lines of time for one ITEM.
2022-04-18
2022-04-18 > 2023-04-18
2022-04-18 > 2023-04-18 > c10, w3, m1, a4

## ITEM2
* you can add many items for one CLASS
2022-04-18
2022-04-18 > 2023-04-18
2022-04-18 > 2023-04-18 > c10, w3, m1, a4

```

And then, you need point to the `save` button to save your new plan.

