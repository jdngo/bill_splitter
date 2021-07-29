# coding=utf-8
import streamlit as st
import pandas as pd

st.set_page_config(
    layout = "wide",
    page_title = "Bill Splitter",
    page_icon = "💸"
)

st.title("Jonathan's Bill Splitter")

if "n_splits" not in st.session_state:
    st.session_state.n_splits = 2
if "n_items"  not in st.session_state:
    st.session_state.n_items = 1
if "data" not in st.session_state:
    st.session_state.data = {}
    for i in range(1, st.session_state.n_splits + 1):
        st.session_state.data[i] = {}
        for j in range(1, st.session_state.n_items + 1):
            st.session_state.data[i][j] = 0
if "original_amount" not in st.session_state:
    st.session_state.original_amount = {"n_splits": st.session_state.n_splits}
    for j in range(1, st.session_state.n_items + 1):
        st.session_state.original_amount[j] = {"current_split": "", "total": ""}

left_button, right_button = st.beta_columns([0.25, 1])

# Name incrementer
increment_splits = left_button.button("+1 split")
if increment_splits:
    st.session_state.n_splits += 1
    i = st.session_state.n_splits
    st.session_state.data[i] = {}
    for j in range(1,  st.session_state.n_items + 1):
        st.session_state.data[i][j] = 0

# Name decrementer
decrement_splits = left_button.button("-1 split")
if decrement_splits:
    if st.session_state.n_splits > 2:
        i = st.session_state.n_splits
        del st.session_state.data[i]
        for j in range(1, st.session_state.n_items + 1):
            del st.session_state[f"item_amount_{i}_{j}"]
        st.session_state.n_splits -= 1

# Item incrementer
increment_items =  right_button.button("+1 item")
if increment_items:
    st.session_state.n_items += 1
    j = st.session_state.n_items
    for i in range(1, st.session_state.n_splits + 1):
        st.session_state.data[i][j] = 0
        st.session_state.original_amount[j] = {"current_split": "", "total": ""}

# Item decrementer
decrement_items = right_button.button("-1 item")
if decrement_items and st.session_state.n_items > 1:
    j = st.session_state.n_items
    del st.session_state.original_amount[j]
    for i in range(1, st.session_state.n_splits + 1):
        del st.session_state.data[i][j]
        del st.session_state[f"item_amount_{i}_{j}"]
    st.session_state.n_items -=1

# Generate column placeholders
columns = st.beta_columns([0.75, 1] + [1] * (st.session_state.n_splits))

# Generate name columns
for i in range(1, st.session_state.n_splits + 1):
    key = f"name_{i}"
    name = columns[i+1].text_input(f"Name {i}", key = key)

# Generate item name rows
columns[1].text_input("", key = f"item_name_empty")
for j in range(1, st.session_state.n_items + 1):
    key = f"item_name_{j}"
    item_name = columns[1].text_input(f"Item {j}", key = key)

# Generate even split select rows
columns[0].text_input("", key = f"even_split_empty")
for j in range(1, st.session_state.n_items + 1):
    columns[0].selectbox("Even split?", ["Yes", "No"], 1, key = f"even_split_{j}")

# Generate item amount rows
def update_item_amount(i, j, key):
    amount = st.session_state.get(key, "")
    if amount.isdigit():
        amount = int(amount)
    else:
        try:
            amount = round(float(amount), 2)
        except:
            if st.session_state[f"even_split_{j}"] == "No":
                st.session_state.data[i][j] = 0
                st.session_state[key] = ""
            elif st.session_state[f"even_split_{j}"] == "Yes":
                if i == 1:
                    st.session_state.original_amount[j] = {"current_split": "", "total": ""}
                    for i in range(1, st.session_state.n_splits + 1):
                        st.session_state.data[i][j] = 0
                        st.session_state[f"item_amount_{i}_{j}"] = ""
                else:
                    st.session_state.data[i][j] = st.session_state.data[1][j]
                    st.session_state[f"item_amount_{i}_{j}"] = st.session_state[f"item_amount_{1}_{j}"]
            return None

    if st.session_state[f"even_split_{j}"] == "Yes":
        if i == 1:
            if (st.session_state.original_amount["n_splits"] != st.session_state.n_splits) and (st.session_state.original_amount[j]["total"] != ""):
                st.session_state.original_amount['n_splits'] = st.session_state.n_splits
                split_amount = round(st.session_state.original_amount[j]["total"] / st.session_state.n_splits, 2)
                st.session_state.original_amount[j]["current_split"] = split_amount
            elif amount == st.session_state.original_amount[j]["current_split"]:
                  return None
            else:
                st.session_state.original_amount[j]["total"] = amount
                st.session_state.original_amount['n_splits'] = st.session_state.n_splits
                split_amount = round(amount / st.session_state.n_splits, 2)
                st.session_state.original_amount[j]["current_split"] = split_amount

            for i in range(1, st.session_state.n_splits + 1):
                st.session_state.data[i][j] = split_amount
                try:
                    st.session_state[f"item_amount_{i}_{j}"] = str(split_amount)
                except:
                    pass
        else:
            st.session_state[f"item_amount_{i}_{j}"] = st.session_state[f"item_amount_1_{j}"]
    else:
        st.session_state.data[i][j] = amount
        st.session_state[key] = str(amount)

for i in range(1, st.session_state.n_splits + 1):
    for j in range(1, st.session_state.n_items + 1):
        key = f"item_amount_{i}_{j}"
        columns[i+1].text_input(f"Amount {j}", key = key, on_change = update_item_amount(i, j, key))

tax = st.text_input("Tax amount", value = 0)
try:
    tax = float(tax)
    valid_tax = True
except:
    st.error("Please enter a valid tax amount.")
    valid_tax = False

tip = st.text_input("Tip amount", value = 0)
try:
    tip = float(tip)
    valid_tip = True
except:
    st.error("Please enter a valid tip amount.")
    valid_tip = False

if valid_tax and valid_tip:
    for i in st.session_state.data:
        i_total = 0
        for j in st.session_state.data[i]:
            if j not in ["subtotal", "tax", "tip", "total"]:
                i_total += st.session_state.data[i][j]
        st.session_state.data[i]["subtotal"] = i_total

    total = 0
    for i in st.session_state.data:
        total += st.session_state.data[i]["subtotal"]

    for i in st.session_state.data:
        if total > 0:
            st.session_state.data[i]["tax"] = round(tax * (st.session_state.data[i]["subtotal"] / total), 2)
        else:
            st.session_state.data[i]["tax"] = 0

    for i in st.session_state.data:
        if total > 0:
            st.session_state.data[i]["tip"] = round(tip * (st.session_state.data[i]["subtotal"] / total), 2)
        else:
            st.session_state.data[i]["tip"] = 0

    for i in st.session_state.data:
        st.session_state.data[i]["total"] = round(st.session_state.data[i]["subtotal"] + st.session_state.data[i]["tax"] + st.session_state.data[i]["tip"], 2)

    names = []
    subtotals = []
    taxes = []
    tips = []
    totals = []

    for i in st.session_state.data:
        name = st.session_state[f"name_{i}"].strip()
        if name == "":
            name = "Name 1"
        names.append(name)
        subtotals.append(st.session_state.data[i]["subtotal"])
        taxes.append(st.session_state.data[i]["tax"])
        tips.append(st.session_state.data[i]["tip"])
        totals.append(st.session_state.data[i]["total"])

    names.append("")
    subtotals.append(round(sum(subtotals), 2))
    subtotals = [f"{i:.2f}" for i in subtotals]

    taxes.append(round(sum(taxes), 2))
    taxes = [f"{i:.2f}" for i in taxes]

    tips.append(round(sum(tips), 2))
    tips = [f"{i:.2f}" for i in tips]

    totals.append(round(sum(totals), 2))
    totals = [f"{i:.2f}" for i in totals]

    st.table(pd.DataFrame({
        "Name": names,
        "Subtotal": subtotals,
        "Tax": taxes,
        "Tip": tips,
        "Total": totals
    }))

# st.write({
#     "n_splits": st.session_state.n_splits,
#     "n_items": st.session_state.n_items,
#     "data": st.session_state.data,
#     "original_amount": st.session_state.original_amount
# })
