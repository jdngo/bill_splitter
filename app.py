# coding=utf-8
import streamlit as st

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
        st.session_state.data[i] = {"name": ""}
        for j in range(1, st.session_state.n_items + 1):
            st.session_state.data[i][j] = {"name": "", "amount": 0}

left_button, right_button = st.beta_columns([0.5, 1])

# Name incrementer
increment_splits = left_button.button("+1 split")
decrement_splits = left_button.button("-1 split")
if increment_splits:
    st.session_state.n_splits += 1
    st.session_state.data[st.session_state.n_splits] = {"name": ""}
    for j in range(1,  st.session_state.n_items + 1):
        st.session_state.data[st.session_state.n_splits][j] = {"name": "", "amount": 0}
if decrement_splits:
    if st.session_state.n_splits > 2:
        del st.session_state.data[st.session_state.n_splits]
        del st.session_state[f"name_{st.session_state.n_splits}"]
        for j in range(1, st.session_state.n_items + 1):
            del st.session_state[f"item_amount_{st.session_state.n_splits}_{j}"]
        st.session_state.n_splits -= 1

# Item incrementer
increment_items =  right_button.button("+1 item")
decrement_items = right_button.button("-1 item")
if increment_items:
    st.session_state.n_items += 1
    for i in range(1, st.session_state.n_splits + 1):
        st.session_state.data[i][st.session_state.n_items] = {"name": "", "amount": 0}
if decrement_items and st.session_state.n_items > 1:
    for i in range(1, st.session_state.n_splits + 1):
        del st.session_state.data[i][st.session_state.n_items]
        del st.session_state[f"item_amount_{i}_{st.session_state.n_items}"]
    del st.session_state[f"item_name_{st.session_state.n_items}"]
    st.session_state.n_items -=1

# Generate column placeholders
columns = st.beta_columns([0.75, 1] + [1] * (st.session_state.n_splits))

# Generate name columns
def update_name(i, key):
    st.session_state.data[i]["name"] = st.session_state.get(key, "")
for i in range(1, st.session_state.n_splits + 1):
    key = f"name_{i}"
    name = columns[i+1].text_input(f"Name {i}", key = key, on_change = update_name(i, key))

# Generate item name rows
def update_item_name(j, key):
    for i in range(1, st.session_state.n_splits + 1):
        st.session_state.data[i][j]["name"] = st.session_state.get(key, "")
columns[1].text_input("", key = f"item_name_empty")
for j in range(1, st.session_state.n_items + 1):
    key = f"item_name_{j}"
    item_name = columns[1].text_input(f"Item {j}", key = key, on_change = update_item_name(j, key))

# Generate even split select rows
columns[0].text_input("", key = f"even_split_empty")
for j in range(1, st.session_state.n_items + 1):
    columns[0].selectbox("Even split?", ["Yes", "No"], 0, key = f"even_split_{j}")

# Generate item amount rows
def update_item_amount(i, j, key):
    amount = st.session_state.get(key, 0)
    if amount == "":
        amount = 0
    else:
        amount = float(amount)
    st.session_state.data[i][j]["amount"] = round(amount, 2)
    st.session_state[f"item_amount_{i}_{j}"] = str(round(amount, 2))

    # if st.session_state.get(f"even_split_{j}", "") == "Yes" and i == st.session_state.n_splits and "original_amount" in st.session_state.data[1][j]:
    #     original_amount = st.session_state.data[1][j]["original_amount"]
    #     if original_amount != 0:
    #         amount = original_amount / st.session_state.n_splits
    #         for i in range(1, st.session_state.n_splits + 1):
    #             st.session_state.data[i][j]["original_amount"] = original_amount
    #             st.session_state.data[i][j]["amount"] = round(amount, 2)
    #             st.session_state[f"item_amount_{i}_{j}"] = str(round(amount, 2))
    # elif amount == st.session_state.data[i][j]["amount"]:
    #     pass
    # else:
    #     if st.session_state.get(f"even_split_{j}", "") == "Yes" and i == 1:
    #         original_amount = amount
    #         amount = amount / st.session_state.n_splits
    #         for i in range(1, st.session_state.n_splits + 1):
    #             st.session_state.data[i][j]["original_amount"] = original_amount
    #             st.session_state.data[i][j]["amount"] = round(amount, 2)
    #             st.session_state[f"item_amount_{i}_{j}"] = str(round(amount, 2))
    #     else:
    #         st.session_state.data[i][j]["amount"] = round(amount, 2)
    #         st.session_state[f"item_amount_{i}_{j}"] = str(round(amount, 2))

for i in range(1, st.session_state.n_splits + 1):
    for j in range(1, st.session_state.n_items + 1):
        key = f"item_amount_{i}_{j}"
        columns[i+1].text_input(f"Amount {j}", key = key, on_change = update_item_amount(i, j, key))

st.write({
    "n_splits": st.session_state.n_splits,
    "n_items": st.session_state.n_items,
    "bill_data": st.session_state.data
})
