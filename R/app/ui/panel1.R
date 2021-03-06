tabPanel(
  title = "Boxplots",
  class = "fade in",
  sidebarLayout(
    sidebarPanel(
      radioGroupButtons(
        inputId = "boxplots_metric",
        label = "Select a metric",
        choices = c("Time" = "time", "Error" = "error"),
        justified = TRUE
      ),
      
      selectizeInput(
        inputId = "boxplots_pdf",
        label = "Choose a density", 
        multiple = TRUE,
        choices = NULL
      ),
      
      selectInput(
        inputId = "boxplots_estimator", 
        label = "Estimator(s)",
        choices = c("Gaussian KDE" = "fixed_gaussian", 
                    "Adaptive Gaussian KDE" = "adaptive_gaussian", 
                    "Gaussian mixture" = "mixture"), 
        selected = "fixed_gaussian",
        multiple = TRUE
      ),
      
      selectInput(
        inputId = "boxplots_bw",
        label = "Bandwidth(s)",
        choices = choices_bw_classic,
        selected = choices_bw_classic[[1]],
        multiple = TRUE
      ),
      
      checkboxGroupButtons(
        inputId = "boxplots_size",
        label = "Sample size(s)",
        choices = as.character(choices_size_default),
        selected = as.character(choices_size_default),
        justified = TRUE,
        size = "sm"
      ),
      
      sliderInput(
        inputId = "boxplots_trim_pct",
        label = "Right tail trimming",
        min = 0,
        max = 10,
        value = 5,
        step = 0.5,
        post = "%" 
      ),
      
      h4(strong("Optional")),
      
      # Only first two variables are going to be selected
      # The order will be first row, then column.
      selectInput(
        inputId = "boxplots_facet_vars",
        label = "Facetting variables",
        choices = c("Bandwidth" = "bw", 
                    "Estimator" = "estimator",
                    "Density" = "pdf"),
        multiple = TRUE
      ),
      
      fluidRow(
        column(
          width = 6,
          checkboxInput(
            inputId = "boxplots_log10",
            label = strong("Log scale"),
            value = FALSE
          )
        ),
        column(
          width = 6,
          checkboxInput(
            inputId = "boxplots_free_y",
            label = strong("Free scale"),
            value = FALSE
          )
        )
      ),
      actionButton(
        inputId = "boxplots_plot_btn", 
        label = "Plot"
      ),
      width = 3
    ),
    mainPanel(
      uiOutput("boxplots_plot_size_UI"),
      uiOutput("boxplots_plot_UI"),
      uiOutput("boxplots_plot_title_UI"),
      uiOutput("boxplots_download_UI"),
      width = 9
    )
  )
)

