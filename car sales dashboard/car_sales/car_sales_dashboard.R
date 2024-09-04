# Load necessary libraries
library(shiny)
library(ggplot2)
library(dplyr)
library(shinythemes)

# Load the data
car_sales_data <- read.csv("car_sales.csv")

#Data cleaning
colnames(car_sales_data) <- make.names(colnames(car_sales_data))

#coverted to numeric
car_sales_data$Price <- as.numeric(gsub(",", "", car_sales_data$Price....))

print(colnames(car_sales_data))

#UI side

ui <- fluidPage(
  theme = shinytheme("cerulean"),
  titlePanel("Enhanced Car Sales Dashboard"),
  sidebarLayout(
    sidebarPanel(
      selectInput("company", "Select Car Company:", 
                  choices = unique(car_sales_data$Company), 
                  selected = unique(car_sales_data$Company)[1]),
      selectInput("region", "Select Dealer Region:",
                  choices = unique(car_sales_data$Dealer_Region), 
                  selected = unique(car_sales_data$Dealer_Region)[1]),
      selectInput("body_style", "Select Body Style:",
                  choices = unique(car_sales_data$Body.Style), 
                  selected = unique(car_sales_data$Body.Style)[1]),
      sliderInput("price_range", "Select Price Range:",
                  min = min(car_sales_data$Price, na.rm = TRUE),
                  max = max(car_sales_data$Price, na.rm = TRUE),
                  value = c(min(car_sales_data$Price, na.rm = TRUE), max(car_sales_data$Price, na.rm = TRUE))),
      checkboxGroupInput("transmission", "Select Transmission Type:",
                         choices = unique(car_sales_data$Transmission),
                         selected = unique(car_sales_data$Transmission)),
      downloadButton("downloadData", "Download Filtered Data")
    ),
    mainPanel(
      tabsetPanel(
        tabPanel("Price Analysis",
                 plotOutput("pricePlot"),
                 plotOutput("priceBoxPlot")),
        tabPanel("Sales Distribution",
                 plotOutput("salesPlot"),
                 tableOutput("summaryTable")),
        tabPanel("Customer Demographics",
                 plotOutput("incomePlot"),
                 plotOutput("genderPlot"))
      )
    )
  )
)
# Server side
server <- function(input, output) {
  
  filtered_data <- reactive({
    car_sales_data %>%
      filter(Company == input$company, 
             Dealer_Region == input$region,
             Body.Style == input$body_style,
             Price >= input$price_range[1],
             Price <= input$price_range[2],
             Transmission %in% input$transmission)
  })
  
  output$pricePlot <- renderPlot({
    ggplot(filtered_data(), aes(x = Model, y = Price, fill = Transmission)) +
      geom_bar(stat = "identity") +
      theme_minimal() +
      labs(title = "Car Prices by Model",
           x = "Car Model", 
           y = "Price ($)") +
      scale_fill_brewer(palette = "Set1")
  })
  
  output$priceBoxPlot <- renderPlot({
    ggplot(filtered_data(), aes(x = Body.Style, y = Price, fill = Body.Style)) +
      geom_boxplot() +
      theme_minimal() +
      labs(title = "Price Distribution by Body Style",
           x = "Body Style", 
           y = "Price ($)") +
      scale_fill_brewer(palette = "Pastel1")
  })
  
  output$salesPlot <- renderPlot({
    ggplot(filtered_data(), aes(x = Model, fill = Body.Style)) +
      geom_bar() +
      theme_minimal() +
      labs(title = "Sales Distribution by Model",
           x = "Car Model", 
           y = "Count") +
      scale_fill_brewer(palette = "Dark2")
  })
  
  output$summaryTable <- renderTable({
    filtered_data() %>%
      group_by(Model) %>%
      summarise(Total_Sales = n(), 
                Average_Price = mean(Price, na.rm = TRUE)) %>%
      arrange(desc(Total_Sales))
  })
  
  output$incomePlot <- renderPlot({
    ggplot(filtered_data(), aes(x = Annual.Income, fill = Gender)) +
      geom_histogram(bins = 30, alpha = 0.7, position = "identity") +
      theme_minimal() +
      labs(title = "Annual Income Distribution",
           x = "Annual Income", 
           y = "Frequency") +
      scale_fill_brewer(palette = "Accent")
  })
  
  output$genderPlot <- renderPlot({
    ggplot(filtered_data(), aes(x = Gender, fill = Gender)) +
      geom_bar() +
      theme_minimal() +
      labs(title = "Gender Distribution",
           x = "Gender", 
           y = "Count") +
      scale_fill_brewer(palette = "Set3")
  })
  
  
  output$downloadData <- downloadHandler(
    filename = function() { paste("filtered_car_sales_data.csv") },
    content = function(file) {
      write.csv(filtered_data(), file)
    }
  )
}

shinyApp(ui = ui, server = server)
