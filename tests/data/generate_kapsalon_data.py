import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Create sample data for 2024
# Starting from January 1, 2024 to December 31, 2024

data = {
    'date': [],
    'time': [],
    'service_id': [],
    'service_name': [],
    'price': [],
    'cost': [],  # Estimated cost (products, time)
    'stylist': []
}

# Services with realistic prices from your kapsalon
services = {
    'basic_cut': {'name': 'Snit + handdrogen', 'price': 36, 'cost': 15},
    'mens_cut': {'name': 'Herensnit', 'price': 29, 'cost': 10},
    'color_base': {'name': 'Kleuren uitgroei', 'price': 50, 'cost': 20},
    'balayage': {'name': 'Balayage', 'price': 90, 'cost': 35},
    'styling': {'name': 'Brushen All-in', 'price': 41, 'cost': 15},
    'kids_cut': {'name': 'Snit jongens -12 jaar', 'price': 29, 'cost': 10},
    'special_botox': {'name': 'Botox behandeling', 'price': 220, 'cost': 80},
    'extensions': {'name': 'Herplaatsing twee rijen', 'price': 120, 'cost': 45}
}

# Generate one year of data
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
current_date = start_date

# Belgian holidays 2024
holidays = [
    '2024-01-01',  # New Year
    '2024-04-01',  # Easter Monday
    '2024-05-01',  # Labor Day
    '2024-05-09',  # Ascension
    '2024-05-20',  # Whit Monday
    '2024-07-21',  # National Day
    '2024-08-15',  # Assumption
    '2024-11-01',  # All Saints
    '2024-11-11',  # Armistice Day
    '2024-12-25',  # Christmas
]

# Working hours
work_hours = {
    0: {'start': '09:00', 'end': '17:00'},  # Monday
    1: {'start': '08:30', 'end': '18:00'},  # Tuesday
    2: None,  # Wednesday (closed)
    3: {'start': '08:30', 'end': '18:00'},  # Thursday
    4: {'start': '08:30', 'end': '20:00'},  # Friday
    5: {'start': '07:30', 'end': '12:30'},  # Saturday
    6: None,  # Sunday (closed)
}

stylists = ['Sarah', 'Mark']  # Two stylists

while current_date <= end_date:
    # Skip closed days
    if current_date.weekday() in [2, 6]:  # Wednesday and Sunday
        current_date += timedelta(days=1)
        continue
        
    # Skip holidays
    if current_date.strftime('%Y-%m-%d') in holidays:
        current_date += timedelta(days=1)
        continue
        
    # Get working hours for current day
    hours = work_hours[current_date.weekday()]
    
    # Generate appointments for the day
    start_time = datetime.strptime(hours['start'], '%H:%M').time()
    end_time = datetime.strptime(hours['end'], '%H:%M').time()
    
    current_time = datetime.combine(current_date.date(), start_time)
    end_datetime = datetime.combine(current_date.date(), end_time)
    
    while current_time < end_datetime:
        # More appointments on busy days (Friday/Saturday)
        if current_date.weekday() in [4, 5]:  # Friday and Saturday
            if np.random.random() < 0.9:  # 90% chance of appointment
                service = np.random.choice(list(services.keys()), 
                                        p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05])  # Higher chance of basic services
            else:
                current_time += timedelta(minutes=30)
                continue
        else:
            if np.random.random() < 0.7:  # 70% chance of appointment
                service = np.random.choice(list(services.keys()),
                                        p=[0.25, 0.2, 0.15, 0.1, 0.1, 0.1, 0.05, 0.05])
            else:
                current_time += timedelta(minutes=30)
                continue
                
        # Add seasonal patterns
        month = current_date.month
        if month in [12, 1]:  # Winter holidays
            if service in ['styling', 'special_botox']:
                if np.random.random() < 0.7:  # Higher chance of styling services
                    service = 'styling'
        elif month in [6, 7]:  # Summer
            if service == 'balayage':
                if np.random.random() < 0.6:  # Higher chance of balayage
                    service = 'balayage'
                    
        # Add the appointment
        data['date'].append(current_date.strftime('%Y-%m-%d'))
        data['time'].append(current_time.strftime('%H:%M'))
        data['service_id'].append(service)
        data['service_name'].append(services[service]['name'])
        data['price'].append(services[service]['price'])
        data['cost'].append(services[service]['cost'])
        data['stylist'].append(np.random.choice(stylists))
        
        # Move time forward based on service
        if service in ['balayage', 'special_botox', 'extensions']:
            current_time += timedelta(minutes=180)  # 3 hours
        elif service == 'color_base':
            current_time += timedelta(minutes=120)  # 2 hours
        else:
            current_time += timedelta(minutes=45)  # 45 minutes
            
    current_date += timedelta(days=1)

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('kapsalon_data_2024.csv', index=False)

# Print some statistics
print(f"Total appointments: {len(df)}")
print("\nServices breakdown:")
print(df['service_name'].value_counts())
print("\nRevenue by month:")
df['month'] = pd.to_datetime(df['date']).dt.month
print(df.groupby('month')['price'].sum())
