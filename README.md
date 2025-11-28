# **matchart**

**matchart** is a simplified, high-level charting library built on top of **Matplotlib**. It streamlines data visualization by handling data preparation (pivoting, grouping, aggregations) and chart construction behind the scenes—allowing to direct focus on design and insights, not boilerplate.

## 🚀 **Features**

### Supported Chart Types

- Bar Chart
- Line Chart

## 🧱 **Core Components**

### **`Chart`**

The main entry point for creating visualizations.

- Accepts a **pandas DataFrame** and handles all required transformations internally.
- Returns a visualization object that provides:
  - Access to Matplotlib `fig` and `ax` objects.
  - Fine-grained `style` controls.
  - Chart metadata.

```python
from matchart.chart.main import Chart

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
chart = Chart(ax=ax, fig=fig)

bar_chart = chart.bar(
    df=df,
    x_axis="State",
    y_axis="Sales",
    agg_func="sum",
    legend="Year",
    limit=("top", 5),
    type="clustered",
    switch_axis=False,
)
bar_chart.style.base.legend.draw()

line_chart = chart.line(
    df=df,
    x_axis="Month",
    y_axis="Sales",
    agg_func="sum",
    legend="Year",
    area=True,
    running_total=False,
)
line_chart.style.base.legend.draw()
```

---

### **`Measures`**

A utility class designed to compute different forms of measures from any `Chart` instance.

### Supported Measures

Year over year: outputs YoY results in two useful formats:

1. **Dictionary** — suitable for attaching values to chart data labels.
2. **Pivot DataFrame** — ideal for analysis, inspection, or exporting.

```python
from matchart.utils.measures import Measures

yoy = Measures(bar).yoy(date_field="Order Date", years=[2017, 2018])
yoy.pivot
yoy.dictionary
```

---

### **`Fonts`**

Load and register custom **.ttf** fonts for use in charts.

#### Parameters:

- `path` — Directory path containing `.ttf` font files
- `fonts` — A dictionary mapping font name to font file

```python
from matchart.utils.fonts import Fonts

domine = Fonts.load(
    path="path/to/directory",
    fonts={
        "bold": "01-domine-bold.ttf",
        "semi_bold": "02-domine-semi-bold.ttf",
        "medium": "03-domine-medium.ttf",
        "regular": "04-domine-regular.ttf",
    },
)
```
