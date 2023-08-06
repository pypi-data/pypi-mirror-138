# streamlit-text-annotation
streamlit-text-annotation is a simple streamlit component for displaying and editing text annotations.
Its display functions are similar to [st-annotated-text](https://github.com/tvst/st-annotated-text), with the following added functions:
- support for multiple labels on the same token
- optional CSS style customization for each label
- automatic distinct color assignment (can be overridden with CSS styles)
- horizonal and vertical label layouts

Its (optional) editing functions allow users to easily add or delete multi-label annotations.

This component is built on [streamlit-component-template-vue](https://github.com/andfanilo/streamlit-component-template-vue).

# Installation
```
pip install streamlit-text-annotation
```

## Parameters
The text_annotation function accepts the following parameters:

- tokens (required): an array of token objects whose properties include 'text' (required) and 'labels' (optional), in the following format:
```
    [
        { text: "Text1"},
        { text: "Text2", labels: ["Label1", "Label2"] },
    ]
```
- labels (optional, default=[]): an array of label objects whose properties include 'text' (required) and 'style' (optional), in the following format:
```
    [
            {"text": "Pronoun"},
            {"text": "Verb", "style": {
                "color": "green",
                "background-color": "white",
                "font-size": "8px",
                "font-weight": "900",
            }}
    ]
```
- allowEditing (optional, default=false): boolean; set to true to allow editing (edit mode) or false to disallow (display mode)
- labelOrientation (optional, default="vertical"): whether to display the labels vertically ("vertical") or horizontally ("horizontal")
- collectLabelsFromTokens (optional, default=true): whether to add labels from existing token labels (defined in the tokens array) to the labels array if not found

## Examples
```
import streamlit as st
from streamlit_text_annotation import text_annotation

data1 = {
    "tokens": [
        {"text": "He", "labels": ["Person"]},
        {"text": "loves"},
        {"text": "his"},
        {"text": "dog", "labels": ["Animal", "Pet"]},
    ],
    "labels": [
        {"text": "Person"},
        {"text": "Action"},
        {"text": "Animal"},
    ]
}

st.subheader("Display Mode:")
left, right = st.columns(2)
with left:
    st.text("Vertical labels:")
    text_annotation(data1)
with right:
    st.text("Horizontal labels:")
    data1["labelOrientation"] = "horizontal"
    text_annotation(data1)


data2 = {
    "allowEditing": True,
    "tokens": [
        {"text": "He", "labels": ["Pronoun", "Person"]},
        {"text": "loves", "labels": ["Action"]},
        {"text": "his"},
        {"text": "dog", "labels": ["Animal"]},
    ],
    "labels": [
        {"text": "Pronoun", "style": {
            "color": "red",
            "background-color": "white",
            "font-size": "8px",
            "border": "3px dashed red",
        }},
        {"text": "Verb", "style": {
            "color": "green",
            "background-color": "white",
            "font-size": "8px",
            "font-weight": "900",
        }},
        {"text": "Noun", "style": {
            "color": "blue",
            "background-color": "white",
            "font-size": "8px",
        }},
        {"text": "Person"},
        {"text": "Animal"},
    ]
}

st.subheader("Edit Mode:")
data = text_annotation(data2)
if data:
    "Returned data:", data
```