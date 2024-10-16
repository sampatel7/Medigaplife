# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Step 1: Load the CSV files into DataFrames
appointments_df = pd.read_csv('data/aep_appointments.csv')
events_df = pd.read_csv('data/aep_events.csv')
policies_df = pd.read_csv('data/aep_policies.csv')

# Print the column names to identify the structure of each DataFrame
print("Appointments Dataset Columns:", appointments_df.columns)
print("Events Dataset Columns:", events_df.columns)
print("Policies Dataset Columns:", policies_df.columns)

# Step 2: Inspect the 'eventstatus' column for unique values
print("Unique values in 'eventstatus':", events_df['eventstatus'].unique())

# Step 3: Data Cleaning
appointments_df['appointment_time'] = pd.to_datetime(appointments_df['appointment_time'])
events_df = events_df.dropna(subset=['eventstatus'])

# Step 4: Check for missing data in each dataset
print("\nMissing Data in Appointments:", appointments_df.isnull().sum())
print("\nMissing Data in Events:", events_df.isnull().sum())
print("\nMissing Data in Policies:", policies_df.isnull().sum())

# Step 5: Exploratory Data Analysis (EDA) with custom colors

# Custom color palette for consistent visual identity
custom_palette = sns.color_palette("coolwarm", as_cmap=True)

# Plot only if data exists for each category
if not appointments_df.empty:
    print("Data for Appointments by Event Type:")
    print(appointments_df['event'].value_counts())
    plt.figure(figsize=(12, 8))
    sns.countplot(x='event', data=appointments_df, palette="Set2")
    plt.title('Number of Appointments by Event Type', fontsize=16)
    plt.xticks(rotation=45)
    plt.savefig('appointments_by_event_type.png')
    plt.show()
    plt.close()

if not events_df.empty:
    print("Data for Events by Status:")
    print(events_df['eventstatus'].value_counts())
    plt.figure(figsize=(12, 8))
    sns.countplot(x='eventstatus', data=events_df, palette="Set1")
    plt.title('Number of Events by Status', fontsize=16)
    plt.xticks(rotation=45)
    plt.savefig('events_by_status.png')
    plt.show()
    plt.close()

if not policies_df.empty:
    print("Data for Policies by Type:")
    print(policies_df['policy_type'].value_counts())
    plt.figure(figsize=(12, 8))
    sns.countplot(x='policy_type', data=policies_df, palette="Set3")
    plt.title('Number of Policies by Type', fontsize=16)
    plt.savefig('policies_by_type.png')
    plt.show()
    plt.close()

# Step 6: Time Series Analysis for Appointments

if not appointments_df.empty:
    appointments_df['year_month'] = appointments_df['appointment_time'].dt.to_period('M')
    appointments_over_time = appointments_df.groupby('year_month').size()

    print("Data for Appointments Over Time:")
    print(appointments_over_time)

    if not appointments_over_time.empty:  # Plot only if there's data
        plt.figure(figsize=(12, 8))
        appointments_over_time.plot(kind='line', marker='o', color='coral')
        plt.title('Appointments Over Time', fontsize=16)
        plt.savefig('appointments_over_time.png')
        plt.show()
        plt.close()

# Step 7: Data Merging for Deeper Insights
merged_df = pd.merge(appointments_df, events_df, on='event_id', how='inner')
merged_df = pd.merge(merged_df, policies_df, left_on='contact_id', right_on='contactid', how='inner')

# Step 8: Conversion Rate Analysis
if not merged_df.empty:
    conversion_rate = merged_df['contactid'].nunique() / merged_df['id'].nunique()
    print(f"Conversion Rate: {conversion_rate * 100:.2f}%")

    conversion_by_event_status = merged_df.groupby('eventstatus')['contactid'].nunique()

    print("Data for Conversion by Event Status:")
    print(conversion_by_event_status)

    if not conversion_by_event_status.empty:
        plt.figure(figsize=(12, 8))
        conversion_by_event_status.plot(kind='bar', color='skyblue')
        plt.title('Policy Conversion by Event Status', fontsize=16)
        plt.ylabel('Number of Conversions')
        plt.xticks(rotation=45)
        plt.savefig('conversion_by_event_status.png')
        plt.show()
        plt.close()

# Bonus: Interactive Plotly Plot for Conversion by Event Status
if not conversion_by_event_status.empty:
    fig = px.bar(conversion_by_event_status, x=conversion_by_event_status.index, y=conversion_by_event_status.values,
                 title="Interactive Policy Conversion by Event Status",
                 labels={"x": "Event Status", "y": "Number of Conversions"},
                 color=conversion_by_event_status.index, color_continuous_scale='Viridis')

    fig.update_layout(xaxis_title="Event Status", yaxis_title="Number of Conversions")
    fig.show()
