import plotly.express as px
import seaborn as sns
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from shiny import reactive

# Load the Palmer Penguins dataset
penguins_df = load_penguins()
#penguins_df.head()

# Set the page options with the title "Penguin Data Exploration"
ui.page_opts(title="Penguin Data", fillable=True)


with ui.sidebar(open="open"):
        ui.h2("Sidebar")
        ui.input_selectize("selected_attribute", "Select Attributes",  ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
            )
        #ui.input_numeric( "plotly_bin_count", "Plotly Number of Bins", 10, min=1,  max=20,)
        ui.input_numeric("n", "Number of items", 10, min=1, max=20)
        ui.input_slider("seaborn_bin_count", "Seaborn Number of Bins", min= 5, max= 50, value=25)
        ui.input_checkbox_group( "selected_species_list", "Choose Species", ["Adelie","Gentoo","Chinstrap"],  selected=["Adelie","Gentoo","Chinstrap"],
            inline=False
            )
        ui.hr()
        ui.a("GitHub",href="https://github.com/mkunta1/cintel-02-data",target="_blank")

with ui.layout_columns():

    # Data Table Using Filtered Data    
    with ui.card():
        "Penguins Data Table"
        @render.data_frame
        def data_table():
            return render.DataTable(filtered_data())

    # Data Grid Using Filtered Data    
    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def data_grid():
            return render.DataGrid(filtered_data())

@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    if selected_species:
        return penguins_df[penguins_df['species'].isin(selected_species)]
    return penguins_df

with ui.layout_columns():
    
     # Plotly Histogram    
    with ui.card():
        ui.card_header("Plotly Histogram")
        @render_plotly
        def plotlyhistogram():
            return px.histogram(
                filtered_data(),
                x=input.selected_attribute(),
                nbins=input.n(),
                color="species"
            ).update_layout(
                xaxis_title="Bill length (mm)",
                yaxis_title="Counts"
            )

 # Seaborn Histogram    
    with ui.card():
        ui.card_header("Seaborn Histogram")
        @render.plot
        def plot2():
            ax=sns.histplot(
                data=filtered_data(), 
                x=input.selected_attribute(), 
                bins=input.seaborn_bin_count(),
               )
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selected_attribute())
            ax.set_ylabel("Number")
            return ax

 # Plotly Scatterplot
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                x="body_mass_g",
                y="flipper_length_mm",
                color="species", title="Scatter Plot of Body mass vs. Flipper Length",
                labels={"body_mass_g": "Body Mass",
                "flipper_length_mm": "Flipper Length"}
                )

            



