import streamlit as st
import streamlit.components.v1 as components

import os

_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit-text-annotation",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component(
        "streamlit-text-annotation", path=build_dir)

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.


def text_annotation(data, key=None):
    component_value = _component_func(data=data, key=key, default={})
    return component_value


# Create an instance of our component with a constant `name` arg, and
# print its output value.

if __name__ == "__main__":
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