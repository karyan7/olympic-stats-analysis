# olympic-stats-analysis

Project Description: Olympics Data Analysis
This project is a data analysis application built with Streamlit that provides insights into the historical performance of athletes, countries, and sports in the Olympic Games. The application allows users to explore data through several categories, including medal tallies, overall analysis, country-wise analysis, and athlete-wise analysis.

Main Features
Medal Tally:

Users can select a specific year and country to view the medal tally.
The application displays the overall performance of countries or their performance in specific Olympics.
Overall Analysis:

Provides top statistics like the number of editions, host cities, sports, events, athletes, and participating nations.
Visualizations include:
The trend of participating nations over the years.
The number of events over time.
Athlete participation over the years.
A heatmap of the number of events per sport over time.
A table of the most successful athletes.
Country-wise Analysis:

Users can select a country to analyze its performance over time.
Visualizations include:
The country’s medal tally over the years.
Sports in which the country excels, represented by a heatmap.
The top 10 athletes from the selected country.
Athlete-wise Analysis:

Provides an analysis of athletes' performance based on age, height, and weight.
Visualizations include:
Distribution of athletes' ages for medalists.
Distribution of ages in different sports for gold medalists.
A scatter plot comparing height and weight of athletes based on the medals won.
The trend of male vs. female participation over the years.

Modules Used
Streamlit (streamlit): The main framework used to build the web application. It provides components for building user interfaces and visualizing data.

Pandas (pandas): Used for data manipulation and analysis. The CSV files containing Olympic data are loaded and processed using Pandas.

Plotly Express (plotly.express) and Plotly Figure Factory (plotly.figure_factory): Used to create interactive plots and charts, including line charts and distribution plots.

Matplotlib (matplotlib.pyplot) and Seaborn (seaborn): Used for creating static plots like scatter plots and heatmaps.

Preprocessor (preprocessor): A custom module likely used to preprocess the raw data before analysis.

Helper (helper): A custom module containing helper functions to facilitate the analysis and visualization tasks
