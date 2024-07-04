import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def generate_distribution(dist_type, size, **params):
    if dist_type == 'Uniform':
        return np.random.uniform(params['low'], params['high'], size)
    elif dist_type == 'Normal':
        return np.random.normal(params['mean'], params['std'], size)
    elif dist_type == 'Exponential':
        return np.random.exponential(params['scale'], size)
    elif dist_type == 'Multinomial':
        return np.random.multinomial(params['n'], params['p'], size)


def plot_distributions(original_data, sample_means):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot original distribution
    ax1.hist(original_data, bins=30, density=True, alpha=0.7)
    ax1.set_title("Original Distribution")
    ax1.set_xlabel("Value")
    ax1.set_ylabel("Frequency")

    # Plot sample means distribution
    ax2.hist(sample_means, bins=30, density=True, alpha=0.7)
    ax2.set_title("Distribution of Sample Means")
    ax2.set_xlabel("Sample Mean")
    ax2.set_ylabel("Frequency")

    return fig


st.title("Central Limit Theorem Interactive Demonstration")

st.sidebar.header("Parameters")
dist_type = st.sidebar.selectbox(
    "Select Distribution", ['Uniform', 'Normal', 'Exponential', 'Multinomial'])

if dist_type == 'Uniform':
    low = st.sidebar.slider("Lower Bound", 0.0, 10.0, 0.0)
    high = st.sidebar.slider("Upper Bound", low + 0.1, 20.0, 10.0)
    params = {'low': low, 'high': high}
elif dist_type == 'Normal':
    mean = st.sidebar.slider("Mean", -10.0, 10.0, 0.0)
    std = st.sidebar.slider("Standard Deviation", 0.1, 10.0, 1.0)
    params = {'mean': mean, 'std': std}
elif dist_type == 'Exponential':
    scale = st.sidebar.slider("Scale", 0.1, 10.0, 1.0)
    params = {'scale': scale}
elif dist_type == 'Multinomial':
    n = st.sidebar.slider("Number of Trials", 1, 100, 10)
    p = st.sidebar.slider("Probability of Success", 0.0, 1.0, 0.5)
    params = {'n': n, 'p': p}

population_size = st.sidebar.number_input(
    "Population Size", 1000, 1000000, 10000)
sample_size = st.sidebar.slider("Sample Size", 1, 500, 30)
num_samples = st.sidebar.slider("Number of Samples", 100, 10000, 1000)

if st.button("Generate Visualization"):
    # Generate the original distribution
    original_data = generate_distribution(dist_type, population_size, **params)

    # Generate sample means
    sample_means = [np.mean(generate_distribution(
        dist_type, sample_size, **params)) for _ in range(num_samples)]

    # Create and display the plot
    fig = plot_distributions(original_data, sample_means)
    st.pyplot(fig)

    # Display statistics
    st.write(
        f"Original Distribution - Mean: {np.mean(original_data):.4f}, Std Dev: {np.std(original_data):.4f}")
    st.write(
        f"Sample Means Distribution - Mean: {np.mean(sample_means):.4f}, Std Dev: {np.std(sample_means):.4f}")

st.write("""
This application demonstrates the Central Limit Theorem:
1. Choose a distribution type and set its parameters.
2. Set the population size, sample size, and number of samples.
3. Click 'Generate Visualization' to see the results.
4. Observe how the distribution of sample means approaches a normal distribution, regardless of the original distribution's shape.
""")
