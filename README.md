# Retail-Lens | Sales Intelligence Dashboard

A professional, enterprise-grade sales analytics dashboard built with Streamlit and Plotly, featuring a unified design system and data-dense visualizations for retail performance analysis.

---

## Features

### Sales Overview
- Total sales, net profit, profit margin, total orders, and loss product KPIs
- Sales by category (bar chart)
- Monthly sales trend (area chart)
- Top 10 products by sales (horizontal bar chart)
- Sales by region (donut chart)
- Quarterly sales trend (bar chart)

### Profit Analysis
- Sub-category profitability with margin % labels
- Margin by region with target line
- Profit vs sales scatter plot by product
- Monthly sales vs profit dual-axis trend

### Loss Intelligence
- Total loss value, loss-making SKUs, and worst product loss KPIs
- Loss-making products data table
- Loss by sub-category (horizontal bar chart)

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Streamlit |
| Data Processing | Pandas |
| Visualization | Plotly Express & Graph Objects |
| Styling | Custom CSS (design system) |
| Fonts | Google Fonts (Syne, DM Sans, DM Mono) |
| Dataset | Superstore Sample Data (CSV) |

---

## Project Structure

```
sales_dashboard/
├── applight.py          # Main application (entry point)
├── design_system.py     # Shared design tokens, components, and Plotly theme
├── data/
│   └── Sample - Superstore.csv
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sales_dashboard
   ```

2. Install dependencies:
   ```bash
   pip install streamlit pandas plotly
   ```

3. Run the application:
   ```bash
   streamlit run applight.py
   ```

4. Open your browser and navigate to `http://localhost:8501`

---

## Data

The dashboard uses the **Superstore Sample Dataset** (`data/Sample - Superstore.csv`) which includes:
- Order date, product details, region, category, sub-category
- Sales amount, profit, quantity
- Pre-computed profit margin %, year, month, quarter
