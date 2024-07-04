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
    elif dist_type == 'Poisson':
        return np.random.poisson(params['lam'], size)
    elif dist_type == 'Gamma':
        return np.random.gamma(params['shape'], params['scale'], size)


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
dist_type = st.sidebar.selectbox("Select Distribution", [
                                 'Uniform', 'Normal', 'Exponential', 'Poisson', 'Gamma'])

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
elif dist_type == 'Poisson':
    lam = st.sidebar.slider("Lambda (rate)", 0.1, 20.0, 5.0)
    params = {'lam': lam}
elif dist_type == 'Gamma':
    shape = st.sidebar.slider("Shape (k)", 0.1, 10.0, 2.0)
    scale = st.sidebar.slider("Scale (theta)", 0.1, 10.0, 2.0)
    params = {'shape': shape, 'scale': scale}

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

Distribution Information:
- Uniform: Models a constant probability over a range.
- Normal: The classic bell-shaped curve.
- Exponential: Models time between events in a Poisson process.
- Poisson: Models the number of events in a fixed interval.
- Gamma: Generalizes the exponential distribution.
""")
