# Function to roll a dice a specified number of times
roll_dice <- function(num_rolls) {
  sample(1:6, num_rolls, replace = TRUE)
}

# Number of experiments
num_experiments <- 4

# Number of rolls per experiment
num_rolls <- 12000

# Store results of each experiment
results <- matrix(nrow = num_rolls, ncol = num_experiments)

# Perform the experiments
for (i in 1:num_experiments) {
  results[, i] <- roll_dice(num_rolls)
}

# --- Plotting the results ---

# Create a data frame for plotting (easier with ggplot2)
library(ggplot2)
library(tidyr) # For reshaping data

plot_data <- as.data.frame(results)
colnames(plot_data) <- paste("Experiment", 1:num_experiments)

# Reshape data to long format for ggplot2
plot_data_long <- pivot_longer(plot_data, 
                               cols = starts_with("Experiment"),
                               names_to = "Experiment",
                               values_to = "DiceRoll")

# Plot histograms using ggplot2
ggplot(plot_data_long, aes(x = DiceRoll, fill = Experiment)) +
  geom_histogram(binwidth = 1, color = "black", boundary = 0.5) + # Histogram with binwidth 1
  facet_wrap(~ Experiment, ncol = 2) + # Separate plots for each experiment
  labs(title = "Histograms of 4 Dice Rolling Experiments (100 Rolls Each)",
       x = "Dice Roll Result",
       y = "Frequency (Number of Rolls)") +
  scale_x_continuous(breaks = 1:6) + # Ensure x-axis shows all dice values
  theme_minimal() + # Use a clean theme
  guides(fill = "none") # Remove the legend as it's redundant with facets
