import seaborn as sns
import plotly.express as px
import palmerpenguins # This package provides palmer penguin dataset.
from shiny import reactive
from shiny.express import input, ui,render
from shinywidgets import render_plotly
import matplotlib.pyplot as plt

penguins = palmerpenguins.load_penguins()
#penguins.head()
#print(penguins.shape)
#penguins.info()
#penguins.describe()


# Load the Palmer Penguins dataset
@reactive.calc
def dat():
    return palmerpenguins.load_penguins()
    

# Define the UI for the Shiny app
ui.h2("Penguins Dashboard")
# Render plotly and seaborn histogram within the same layout column.

with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_numeric("n", "Number of items", 2, min=1, max=5)
    ui.input_selectize("sex", "Select sex below:",  {"male": "male", "female": "female"}, multiple=True, selected=['female'])
    ui.input_slider("body_mass_g", "Body Mass (g)", min=2300, max=6500, value=[2300, 6500], step=300)
    ui.input_checkbox_group( "island",  "island",    {  "Torgersen": "Torgersen",  "Dream": "Dream",  "Biscoe": "Biscoe", }, )
    ui.hr()
    ui.a("GitHub",href="https://github.com/mkunta1/cintel-02-data",target="_blank")

 
            
with ui.layout_columns():
    with ui.card(full_screen=False):    
        ui.card_header("Unique Penguin Species Count by Island and Year")     
        
        @render_plotly
        def plot():
            df=dat()
            #Species count by island and year
            species_count = df.groupby(['island'])['species'].count().reset_index()
            species_count.columns = ['Island', 'species_count']  # Rename the columns for clarity
            
            # Limit the results to the top N islands based on species count
            species_count = species_count.nlargest(input.n(), 'species_count')
            figf = px.bar(species_count, x='Island', y='species_count' ,color="species_count")
            figf.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),  # Adjust margins for better layout
            height=210,  # Set a fixed height for the figure
            width=310,  # Optionally set a fixed width
        )
            return figf

 
                 
# Card for the plot of unique species count by island and year
with ui.card(full_screen=False):
    ui.card_header("Unique Penguin Species Count by Island and Year")    
    @render_plotly
    def scatter_plot():
        df = dat()  # Get the latest dataset
        
        # Filter data based on selected sex
        bodymass_byspecies = df[df['sex'].isin(input.sex())].copy() 

        # Filter data based on selected island
        bodymass_byspecies = bodymass_byspecies[bodymass_byspecies['island'].isin(input.island())].copy() 

        # Filter data based on selected body mass g
        #bodymass_byspecies = bodymass_byspecies[bodymass_byspecies['body_mass_g'].isin(input.body_mass_g())]
        # Filter data based on selected body mass range
        bodymass_byspecies = bodymass_byspecies[
            (bodymass_byspecies['body_mass_g'] >= input.body_mass_g()[0]) &
            (bodymass_byspecies['body_mass_g'] <= input.body_mass_g()[1])        ]
        
        
        
        # Group by year and island, count unique species
        #bodymass_byspecies = bodymass_byspecies.groupby(['year', 'island'])['species'].count().reset_index()            
      
        # Create a bar plot
        fig = px.scatter(bodymass_byspecies, 
                    x='body_mass_g', 
                    y='flipper_length_mm', 
                    color='species',  # Different colors for different species
                    title="Scatter Plot of Body mass vs. Flipper Length",
                    labels={'body_mass_g': 'Body Mass', 'flipper_length_mm': 'Flipper Length'})
        
        return fig
           
with ui.layout_columns():        
        
        with ui.card(full_screen=False):
            ui.card_header("Distribution of Penguin Species")
            @render.plot
            def plot2():
             plt.figure(figsize=(1, 1))  # Adjust figure size for better layout
             sns.histplot(data=penguins, x="species", kde=True)
             plt.title("Distribution of Species")
             plt.xlabel("Species")
             plt.ylabel("Count")
             return plt.gcf()  # Return the current figure

        @render.data_frame
        def penguinsdata():
           return render.DataGrid(dat(), filters=True)

        @render.data_frame
        def penguinsdata1():
           return render.DataTable(dat(), filters=True)
     
