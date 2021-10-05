# load library
library(shiny)
library(leaflet)
library(dplyr)
library(tidyverse)
library(ggplot2)
library(timevis)
library(plotly)
library(scales)

# data wrangling
#covid19_country_new = covid19_country[,-3]
#colnames(covid19_country_new)[3] <- "CountryName"

## fix errors
#levels(covid19_country_new$CountryName)
#covid19_country_new$CountryName <- as.character(covid19_country_new$CountryName)
#covid19_country_new$CountryName[covid19_country_new$CountryName == "US"] <- "United States"
#covid19_country_new$CountryName[covid19_country_new$CountryName == "('St. Martin',)"] <- "Saint Martin"
#covid19_country_new$CountryName[covid19_country_new$CountryName == "St. Martin"] <- "Saint Martin"
#covid19_country_new$CountryName[covid19_country_new$CountryName == "Bahamas, The"] <- "Bahamas"
#covid19_country_new$CountryName[covid19_country_new$CountryName == "Gambia, The"] <- "Gambia"
#covid19_country_new$CountryName <- as.factor(covid19_country_new$CountryName)

# Calculate ratios
#covid19_country_new$Death_rate = (covid19_country_new$Deaths / covid19_country_new$Confirmed)
#covid19_country_new$Recovery_rate = (covid19_country_new$Recovered / covid19_country_new$Confirmed)

# merge datasets                                        
#covid19_country_new = inner_join(covid19_country_new, worldmap, by = "CountryName")

#covid19_country_new <- covid19_country_new %>% filter(covid19_country_new$CapitalLatitude != 0)

#covid19_country_new <- gather(covid19_country_new, measurements, value, Confirmed:Recovered, factor_key=TRUE)

# output into csv file
#write.csv(covid19_country_new, "covid19_worldmap_new.csv")

# data input
worldmap <- read.csv("world_map.csv")

covid19_world <- read.csv("covid19_worldmap_new.csv", stringsAsFactors = FALSE)
covid19_world$ObservationDate <- as.Date(covid19_world$ObservationDate, "%Y-%m-%d")

covid19_China <- read.csv("covid19_china_merged.csv")
covid19_China$ObservationDate <- as.Date(covid19_China$ObservationDate, "%m/%d/%Y")


# Color settings
bins = c(0,100,1000,10000,50000,100000,200000,Inf)
pal <- colorBin("Reds", domain = covid19_world$value, bins = bins)

# Shiny Server
shinyServer(function(input, output){
  
  # reactive map title text
  maptitle <- reactive({
    paste("COVID-19", input$measurements, "World Wide (Jan - Apr)")
  })
  
  # show map title text
  output$caption <- renderText({maptitle()})
  
  # Setting up introduction text
  background <- reactive({paste("In December 2019, cases of severe respiratory illness began to be reported across the city of Wuhan in China. 
     It was later identifyed as a new form of coronavirus named 2019 Novel Coronavirus (2019-nCoV) by WHO.
          The aim of this site is to visualize the spreading of COVID-19 overworld from Jan - Apr by providing several interactive features.
          Specfic visualization is provided around China, the visualizations helps to answer following questions: 
          How fast is the virus spreading? How is China performing compare to other countries? Are efforts to control the disease working?")
  })
  
  # show introduction text
  output$background <- renderText({background()})
  
  # setting up map data filtering
  mymap <- reactive({covid19_world %>% filter(measurements == input$measurements &
                                                ObservationDate == input$Dates) %>%
                      group_by(CountryName) %>% filter(value == max(value)) %>% arrange(desc(value))})
  
  # plot map
  output$worldmap <- renderLeaflet({
    leaflet(data = mymap()) %>% addProviderTiles("Stamen.Toner")})
    
  observe({
      leafletProxy("worldmap", data = mymap()) %>% 
        clearMarkers() %>%
        clearShapes() %>%
        # Circles settings on map
        addCircleMarkers(
          ~CapitalLongitude, 
          ~CapitalLatitude,
          label = ~paste(CountryName,"--", input$measurements, ":", value),
          labelOptions = labelOptions(textsize = "15px"),
          radius = ~sqrt(value/100),
          color = ~pal(value),
          fillOpacity = 0.7) %>% 
        # legend settings
        addLegend("bottomright", pal= pal, values = ~value,
                  title = "Number of cases in Country",
                  opacity = 0.9)
  })
  
  # barchart data
  chart_top3 <- reactive({mymap()[1:3,]})
  chart_top5 <- reactive({mymap()[1:5,]})
  chart_top7 <- reactive({mymap()[1:7,]})
  
  # barchart 
  output$barchart <- renderPlot({
    if(input$TopCountry == "Top 3"){
    ggplot(chart_top3(), aes(x = CountryName, y = value, fill = CountryName)) +
      geom_col() +
        ylab("cases") +
        # color settings
        scale_fill_manual(values = c("red", "green", "yellow")) +
        # title
        labs(title = "Covid-19 Cases by Country (TOP3)") +
        geom_label(aes(label = value)) +
        # text settings and legend position
        theme(
          plot.title = element_text(color = "black", size = 16, face = "bold"),
          axis.title.x = element_text(color = "black", size = 13, face = "bold"),
          axis.title.y = element_text(color = "black", size = 13, face = "bold"),
          legend.title = element_text(color = "black", size = 10, face = "bold"),
          legend.text = element_text(color = "black", size = 9, face = "bold"),
          legend.position = "bottom")
      }
    else if(input$TopCountry == "Top 5"){
      ggplot(chart_top5(), aes(x = CountryName, y = value, fill = CountryName)) +
        geom_col() +
        ylab("cases") +
        scale_fill_manual(values = c("red", "green", "yellow", "orange", "purple")) +
        labs(title = "Covid-19 Cases by Country (TOP5)") + 
        geom_label(aes(label = value)) +
        theme(
          plot.title = element_text(color = "black", size = 16, face = "bold"),
          axis.title.x = element_text(color = "black", size = 13, face = "bold"),
          axis.title.y = element_text(color = "black", size = 13, face = "bold"),
          legend.title = element_text(color = "black", size = 10, face = "bold"),
          legend.text = element_text(color = "black", size = 9, face = "bold"),
          legend.position = "bottom")
      }
    else if(input$TopCountry == "Top 7"){
      ggplot(chart_top7(), aes(x = CountryName, y = value, fill = CountryName)) +
        geom_col() +
        ylab("cases") +
        scale_fill_manual(values = c("red", "green", "yellow", "orange", "purple", "blue", "pink")) +
        labs(title = "Covid-19 Cases by Country (TOP7)") + 
        geom_label(aes(label = value)) +
        theme(
          plot.title = element_text(color = "black", size = 16, face = "bold"),
          axis.title.x = element_text(color = "black", size = 13, face = "bold"),
          axis.title.y = element_text(color = "black", size = 13, face = "bold"),
          legend.title = element_text(color = "black", size = 10, face = "bold"),
          legend.text = element_text(color = "black", size = 9, face = "bold"),
          legend.position = "bottom")
      }
  })
  
  # reactive plot data filtering
  Country_filtered <- reactive({
    if (is.null(input$Countries)){covid19_world %>% filter (CountryName == "China" & ObservationDate >= input$daterange[1] & 
                                                              ObservationDate <= input$daterange[2]) %>% 
        group_by(CountryName, ObservationDate) %>% filter(value == max(value)) %>%  distinct(value, .keep_all = TRUE)}
    
    else {covid19_world %>% filter (CountryName %in% input$Countries | CountryName == "China") %>% filter (ObservationDate >= input$daterange[1] & 
                                      ObservationDate <= input$daterange[2]) %>% 
      group_by(CountryName, ObservationDate) %>% filter(value == max(value)) %>%  distinct(value, .keep_all = TRUE)}
    })

  # plot china dot plot
  output$Chinaplot <- renderPlotly({ 
    if (input$ratio == "Confirmed cases" & is.null(input$Countries)){
      ggplotly(ggplot(data = Country_filtered(), aes(x = ObservationDate, y = value, shape = CountryName, 
                                                     color = CountryName, stroke = 0.3)) +
      geom_point() + 
      # axis name
      xlab("Date(2020)")+
      ylab("Confirmed cases") +
      # plot title
      labs(title = "Confirmed cases comparison over time") +
      # x axis scale
      scale_x_date(breaks = as.Date(c("2020-02-01","2020-02-15","2020-03-01","2020-03-15","2020-04-01","2020-04-15"))) +
        theme_bw() +
        # legend and text settings
        theme(
          panel.grid.major.y = element_line (color = "black"),
          plot.title = element_text(color = "black", size = 15, face = "bold"),
          axis.title.x = element_text(color = "black", size = 10, face = "bold"),
          axis.title.y = element_text(color = "black", size = 10, face = "bold"),
          legend.title = element_blank(),
          legend.text = element_text(color = "black", size = 9, face = "bold")) +
        # timeline labels 
        annotate("text", x = as.Date(c("2020-01-23","2020-01-26","2020-01-28","2020-02-02","2020-02-05","2020-02-09","2020-02-11","2020-02-19","2020-02-28","2020-03-02","2020-04-08")), 
                 y = c(1000,5000,10000,15000,25000,30000,35000,45000,50000,55000,62000), label = c("Lockdown","Travel Ban","Exceeds Sars","Hospital completed","Build more makeshift hospitals","Disinfect cities","Adopted health QR Code","30000 medical stuff support Wuhan","WHO raises risk to VERY HIGH","nine times more new cases reported outside China","Wuhan Lockdown lifted"), size = 3))
      
      }
    else if (input$ratio == "Confirmed cases") {
      ggplotly(ggplot(data = Country_filtered(), aes(x = ObservationDate, y = value, shape = CountryName, 
                                                     color = CountryName, stroke = 0.3)) +
                 geom_point() + 
                 xlab("Date(2020)")+
                 ylab("Confirmed cases") +
                 labs(title = "Confirmed cases comparison over time") +
                 scale_x_date(breaks = as.Date(c("2020-02-01", "2020-03-01","2020-04-01"))) +
                 theme_bw() +
                 theme(
                   panel.grid.major.y = element_line (color = "black"),
                   plot.title = element_text(color = "black", size = 15, face = "bold"),
                   axis.title.x = element_text(color = "black", size = 10, face = "bold"),
                   axis.title.y = element_text(color = "black", size = 10, face = "bold"),
                   legend.title = element_blank(),
                   legend.text = element_text(color = "black", size = 9, face = "bold"))
                )
      }
    else if (input$ratio == "Death_rate"){
        ggplotly(ggplot(data = Country_filtered(), aes(x = ObservationDate, y = Death_rate, color = CountryName, stroke = 0.3)) +
        geom_line(size = 1) + 
        xlab("Date(2020)")+
        labs(title = "Death rate comparison over time") +
        scale_x_date(breaks = as.Date(c("2020-02-01", "2020-03-01","2020-04-01")),
                     minor_breaks = as.Date(c("2020-01-28","2020-02-07", "2020-02-12", "2020-02-17","2020-02-22","2020-02-27"
                                              ,"2020-03-07","2020-03-12","2020-03-17","2020-03-22","2020-03-27","2020-04-01",
                                              "2020-04-06","2020-04-11","2020-04-16","2020-04-21"))) +
        scale_color_manual(values = c("red", "blue", "black", "yellow", "purple")) + 
          theme_bw() +
          theme(
            plot.title = element_text(color = "black", size = 15, face = "bold"),
            axis.title.x = element_text(color = "black", size = 10, face = "bold"),
            axis.title.y = element_text(color = "black", size = 10, face = "bold"),
            legend.title = element_blank(),
            legend.text = element_text(color = "black", size = 9, face = "bold")))}
    
    else if (input$ratio == "Recovery_rate"){
        ggplotly(ggplot(data = Country_filtered(), aes(x = ObservationDate, y = Recovery_rate, color = CountryName, stroke = 0.3)) +
        geom_line(size = 1) + 
        xlab("Date(2020)") +
        labs(title = "Recovery rate comparison over time") +
        scale_x_date(breaks = as.Date(c("2020-02-01", "2020-03-01","2020-04-01")),
                     minor_breaks = as.Date(c("2020-01-28","2020-02-07", "2020-02-12", "2020-02-17","2020-02-22","2020-02-27"
                                              ,"2020-03-07","2020-03-12","2020-03-17","2020-03-22","2020-03-27","2020-04-01",
                                              "2020-04-06","2020-04-11","2020-04-16","2020-04-21"))) +
        scale_color_manual(values = c("red", "blue", "black", "yellow", "purple")) + 
          theme_bw() +
          theme(
            plot.title = element_text(color = "black", size = 15, face = "bold"),
            axis.title.x = element_text(color = "black", size = 10, face = "bold"),
            axis.title.y = element_text(color = "black", size = 10, face = "bold"),
            legend.title = element_blank(),
            legend.text = element_text(color = "black", size = 9, face = "bold")))}
    })
  
  # reactive pie chart data filtering
  China_filtered <- reactive({
    covid19_China %>% filter(ObservationDate >= input$daterange[1] & 
                               ObservationDate <= input$daterange[2]) %>% 
      group_by(Province.State) %>% filter(Confirmed == max(Confirmed)) %>%
      distinct(Confirmed, .keep_all = TRUE)
  })
  
  
  # draw pie chart
  output$piechart <- renderPlot({
    ggplot(China_filtered(), aes(x = 0, y = Confirmed, fill=Province.State))+
      # from bar to pie chart
      geom_bar(stat = "identity") + coord_polar("y", start=0) + labs(title = "Confirmed Cases in Province") +
      # Text labels 
      geom_text(aes(y = Confirmed ,label = percent(Confirmed/sum(Confirmed))), size=5, check_overlap = TRUE) +
      # Legend and text settings
      theme(legend.title = element_blank(),
            legend.position = "right",
            legend.text = element_text(size = 10))
  })

  # Title of China plot
  Plottitle <- reactive({paste("China vs Other countries")})
  # show introduction 
  output$plottitle <- renderText({Plottitle()})
  
  # Datasource title
  Datasource <- reactive({paste("Data Source:")})
  # Show Datasource title
  output$DataSource <- renderText({Datasource()})
})  

  
  