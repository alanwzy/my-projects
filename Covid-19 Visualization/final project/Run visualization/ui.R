# load library
library(shiny)
library(leaflet)
library(tidyverse)
library(dplyr)
library(ggplot2)
library(plotly)
library(scales)

# Define UI 
shinyUI(fluidPage(
  tags$head(tags$style(
    # CSS panel settings
    HTML('
         #panel1 {
            background-color: white;
            opacity: 0.5;
            zoom: 1;
            transition: opacity 500ms 0.1s;}
        #panel1:hover {opacity: 0.95;
          transition-delay:0; 
          zoom:1}
            ')
  )),
  
  # Application title
  
  navbarPage("Covid-19 visualization",
             # first panel
             tabPanel("COVID-19 World Map",
                      mainPanel(
                        # Heading
                        h3(textOutput("caption")),
                        # Introduction
                        h5(textOutput("background")),
                        # World Map
                        leafletOutput("worldmap", width = "155%", height = "750px"),
                        # Floating panel
                        absolutePanel(id = "panel1", top=170, left = 70, draggable = TRUE, width = "360", height = "650",
                                      # Options 
                                      radioButtons("measurements"," Measurements: ", 
                                                   c("Confirmed Cases" = "Confirmed", 
                                                     "Deaths" = "Deaths", 
                                                     "Recovered" = "Recovered")),
                                      # date slider
                                      sliderInput("Dates", "Dates: ", 
                                                  min = as.Date("2020-01-22", "%Y-%m-%d"), 
                                                  max = as.Date("2020-04-20", "%Y-%m-%d"),
                                                  value = as.Date("2020-04-20"), 
                                                  timeFormat = "%Y-%m-%d"), 
                                      # Select counties
                                      selectInput("TopCountry", "Select numbers of top countries for comparison: ",
                                                  c("TOP 3" = "Top 3",
                                                  "TOP 5" = "Top 5",
                                                  "TOP 7" = "Top 7")),
                                      # Barchart
                                      plotOutput("barchart")
                                      ))),
             # Second panel
             tabPanel("COVID-19 in China",
                        sidebarPanel(width = 4, h3("What happened in China?"),
                                     "In many people's eyes, China has overact to the outbreak of coronavirus compare to other countries. However,the coronavirus still spread widely and quickly across the country from January to February. Luckily, China's overaction and regulations implement have managed to contained the outbreak by the end of April. At the same time, outbreaks start to occur in the rest of the world.",
                                     h4("Please select from below options: "),
                                     # select option
                                     selectInput("ratio","Select measurement(graph1): ", 
                                                 c("Confirmed cases" = "Confirmed cases",
                                                   "Recovery rate" = "Recovery_rate",
                                                   "Death rate" = "Death_rate")),
                                     # Checkbox option
                                     checkboxGroupInput("Countries", "Select country(graph1): ", 
                                                        c("USA" = "United States", 
                                                          "Spain" = "Spain", 
                                                          "Italy" = "Italy",
                                                          "France" = "France")),
                                     # Date range selection
                                     dateRangeInput("daterange", label = 'Select date range(graph 1 & 2): ', start = as.Date("2020-01-22"), 
                                                    end = as.Date("2020-04-20")),
                                     # Reference to data source
                                     h4(textOutput("DataSource")),
                                     "Novel-corona-virus-2019 dataset: https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv.", "\n", 
                                     "Latitude and longitude of world capitals : https://www.kaggle.com/nikitagrec/world-capitals-gps"),
                        
                        mainPanel(
                          h3("China vs Other Countries: "),
                          # Comparison plot
                          plotlyOutput("Chinaplot"),
                          h3("Inside of China: "),
                          # Provinces chart
                          plotOutput("piechart")
                        ))
    
  ) 
))

